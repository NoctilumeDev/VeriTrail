import { normalizeBundlePath, sha256Hex } from './bundle'
import type {
  BatchAnalysis,
  BatchAnalysisManifest,
  BatchAnalysisSlot,
  BatchCoverageStatus,
  BatchDimension,
  BatchExecutionPolicy,
  BatchHypothesisStatus,
  BatchOutcomeObservation,
  BatchPhase,
  BatchPlan,
  BatchPrimaryDefinition,
  BatchProfilePlan,
  BatchProfileSummary,
  BatchScheduleSlot,
  BatchSource,
  ExecutionStatus,
  LoadedBatchAnalysis,
  Verdict,
} from './types'

const MAX_FILES = 4
const MAX_FILE_BYTES = 10 * 1024 * 1024
const MAX_BUNDLE_BYTES = 30 * 1024 * 1024
const SHA256 = /^[0-9a-f]{64}$/
const ANALYSIS_ID = /^batch_[0-9a-f]{24}$/
const IDENTIFIER = /^[a-z0-9][a-z0-9._-]{1,63}$/
const PHASES = new Set<BatchPhase>(['COVERAGE', 'PERTURBATION'])
const COVERAGE_STATUSES = new Set<BatchCoverageStatus>([
  'COMPLETE',
  'INCOMPLETE',
  'INCONCLUSIVE',
])
const HYPOTHESIS_STATUSES = new Set<BatchHypothesisStatus>([
  'SUPPORTED',
  'CONTRADICTED',
  'INCONCLUSIVE',
])
const EXECUTION_STATUSES = new Set<ExecutionStatus>([
  'PLANNED',
  'RUNNING',
  'COMPLETED',
  'ABORTED',
  'ERROR',
])
const VERDICTS = new Set<Verdict>(['PASS', 'FAIL', 'INCONCLUSIVE', 'PENDING'])
const CONTAMINATION_REASONS = new Set([
  'RUN_ID_REUSED',
  'BUNDLE_REUSED',
  'CONTROL_PROJECTION_MISMATCH',
  'SOURCE_RANDOM_SEED_MISMATCH',
  'SOURCE_PLAN_KIND_MISMATCH',
  'PROFILE_PLAN_DIGEST_MISMATCH',
  'PRIMARY_VARIABLE_MISMATCH',
  'PROFILE_REALIZATION_MISMATCH',
  'STATIC_ROOT_FINGERPRINT_MISMATCH',
  'PREFLIGHT_BOUNDARY_FAILED',
  'CLEANUP_BOUNDARY_FAILED',
  'BROWSER_BOUNDARY_FAILED',
  'WAVE_ORDER_MISMATCH',
  'SOURCE_TIME_INVALID',
  'OUTCOME_MISSING',
  'UNDECLARED_OUTCOME_DRIFT',
  'PERTURBATION_OUTCOME_DRIFT',
])
const INCOMPLETE_REASONS = new Set(['SLOT_MISSING', 'RUN_NOT_COMPLETED', 'SOURCE_EVIDENCE_INCOMPLETE'])

export class BatchLoadError extends Error {
  readonly code: string

  constructor(code: string, message: string) {
    super(message)
    this.name = 'BatchLoadError'
    this.code = code
  }
}

function fail(code: string, message: string): never {
  throw new BatchLoadError(code, message)
}

function record(value: unknown, name: string): Record<string, unknown> {
  if (typeof value !== 'object' || value === null || Array.isArray(value)) {
    fail('BATCH_INVALID', `${name} 必须是对象。`)
  }
  return value as Record<string, unknown>
}

function string(value: unknown, name: string, pattern?: RegExp): string {
  if (typeof value !== 'string' || !value || (pattern && !pattern.test(value))) {
    fail('BATCH_INVALID', `${name} 不符合 M8 0.1 契约。`)
  }
  return value
}

function integer(value: unknown, name: string): number {
  if (!Number.isInteger(value)) fail('BATCH_INVALID', `${name} 必须是整数。`)
  return value as number
}

function rangedInteger(value: unknown, name: string, minimum: number, maximum: number): number {
  const parsed = integer(value, name)
  if (parsed < minimum || parsed > maximum) {
    fail('BATCH_INVALID', `${name} 必须在 ${minimum}–${maximum} 范围内。`)
  }
  return parsed
}

function boolean(value: unknown, name: string): boolean {
  if (typeof value !== 'boolean') fail('BATCH_INVALID', `${name} 必须是布尔值。`)
  return value
}

function array(value: unknown, name: string): unknown[] {
  if (!Array.isArray(value)) fail('BATCH_INVALID', `${name} 必须是数组。`)
  return value
}

function canonicalJson(value: unknown): string {
  if (value === null || typeof value !== 'object') return JSON.stringify(value)
  if (Array.isArray(value)) return `[${value.map(canonicalJson).join(',')}]`
  const source = value as Record<string, unknown>
  return `{${Object.keys(source)
    .sort()
    .map((key) => `${JSON.stringify(key)}:${canonicalJson(source[key])}`)
    .join(',')}}`
}

function same(left: unknown, right: unknown): boolean {
  return canonicalJson(left) === canonicalJson(right)
}

function exactKeys(value: Record<string, unknown>, expected: readonly string[], name: string) {
  if (!same(Object.keys(value).sort(), [...expected].sort())) {
    fail('BATCH_INVALID', `${name} 字段集合不符合冻结契约。`)
  }
}

async function parseJson(blob: Blob, name: string): Promise<unknown> {
  try {
    return JSON.parse(await blob.text()) as unknown
  } catch {
    fail('BATCH_INVALID_JSON', `${name} 不是有效 JSON。`)
  }
}

function parseStringList(value: unknown, name: string): string[] {
  const result = array(value, name).map((item, index) => string(item, `${name}[${index}]`))
  if (result.length === 0) fail('BATCH_INVALID', `${name} 不能为空。`)
  return result
}

function parsePrimary(value: unknown, name: string): BatchPrimaryDefinition {
  const primary = record(value, name)
  exactKeys(
    primary,
    primary.unit === undefined ? ['name', 'source'] : ['name', 'source', 'unit'],
    name,
  )
  return {
    name: string(primary.name, `${name}.name`),
    source: string(primary.source, `${name}.source`),
    ...(primary.unit === undefined ? {} : { unit: string(primary.unit, `${name}.unit`) }),
  }
}

function safeRelativeDirectory(value: string): boolean {
  if (value.includes('\\') || value.startsWith('/') || /^[A-Za-z]:/.test(value)) return false
  return value.split('/').every(
    (part) =>
      Boolean(part) &&
      part !== '.' &&
      part !== '..' &&
      !part.startsWith('.') &&
      /^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$/.test(part),
  )
}

function cartesianCells(dimensions: BatchDimension[]): Array<Record<string, string>> {
  let result: Array<Record<string, string>> = [{}]
  for (const dimension of dimensions) {
    result = result.flatMap((cells) =>
      dimension.levels.map((level) => ({ ...cells, [dimension.name]: level.id })),
    )
  }
  return result
}

async function seededProfileOrder(profileIds: string[], seed: number, repetition: number) {
  const ranked = await Promise.all(
    profileIds.map(async (profileId) => ({
      profileId,
      digest: await sha256Hex(new Blob([canonicalJson([seed, repetition, profileId])])),
    })),
  )
  return ranked
    .sort((left, right) => left.digest.localeCompare(right.digest) || left.profileId.localeCompare(right.profileId))
    .map((item) => item.profileId)
}

function parseManifest(value: unknown): BatchAnalysisManifest {
  const manifest = record(value, 'batch-analysis-manifest.json')
  exactKeys(manifest, ['schema_version', 'analysis_id', 'files'], 'manifest')
  if (manifest.schema_version !== '0.1') {
    fail('BATCH_VERSION_UNSUPPORTED', 'BatchAnalysis Manifest 版本不受支持。')
  }
  const files = array(manifest.files, 'manifest.files').map((value, index) => {
    const file = record(value, `manifest.files[${index}]`)
    exactKeys(file, ['path', 'sha256', 'size'], `manifest.files[${index}]`)
    const size = rangedInteger(file.size, `manifest.files[${index}].size`, 0, MAX_FILE_BYTES)
    return {
      path: normalizeBundlePath(string(file.path, `manifest.files[${index}].path`)),
      sha256: string(file.sha256, `manifest.files[${index}].sha256`, SHA256),
      size,
    }
  })
  const expected = ['sealed-batch-plan.json', 'batch-analysis.json', 'batch-analysis.md']
  const paths = files.map((file) => file.path)
  if (files.length !== 3 || new Set(paths).size !== 3 || expected.some((path) => !paths.includes(path))) {
    fail('BATCH_FILE_SET_MISMATCH', 'Manifest 必须且只能声明 BatchPlan、JSON 与 Markdown。')
  }
  return {
    schema_version: '0.1',
    analysis_id: string(manifest.analysis_id, 'manifest.analysis_id', ANALYSIS_ID),
    files,
  }
}

function parseDimensions(value: unknown): BatchDimension[] {
  const dimensions = array(value, 'dimensions')
  if (dimensions.length < 2 || dimensions.length > 4) {
    fail('BATCH_PLAN_CONFLICT', 'BatchPlan 必须声明 2–4 个有序维度。')
  }
  const names = new Set<string>()
  return dimensions.map((value, index) => {
    const dimension = record(value, `dimensions[${index}]`)
    exactKeys(dimension, ['name', 'levels'], `dimensions[${index}]`)
    const name = string(dimension.name, `dimensions[${index}].name`, IDENTIFIER)
    if (names.has(name)) fail('BATCH_PLAN_CONFLICT', 'BatchPlan 维度名称重复。')
    names.add(name)
    const levelsValue = array(dimension.levels, `dimensions[${index}].levels`)
    if (levelsValue.length < 2 || levelsValue.length > 4) {
      fail('BATCH_PLAN_CONFLICT', '每个 BatchPlan 维度必须声明 2–4 个 level。')
    }
    const ids = new Set<string>()
    const values = new Set<string>()
    const levels = levelsValue.map((value, levelIndex) => {
      const level = record(value, `dimensions[${index}].levels[${levelIndex}]`)
      exactKeys(level, ['id', 'value'], `dimensions[${index}].levels[${levelIndex}]`)
      const id = string(level.id, `dimensions[${index}].levels[${levelIndex}].id`, IDENTIFIER)
      const encoded = canonicalJson(level.value)
      if (ids.has(id) || values.has(encoded)) {
        fail('BATCH_PLAN_CONFLICT', '同一维度不能重复 level ID 或 value。')
      }
      ids.add(id)
      values.add(encoded)
      return { id, value: level.value }
    })
    return { name, levels }
  })
}

function parseProfiles(value: unknown, dimensions: BatchDimension[]): BatchProfilePlan[] {
  const values = array(value, 'profiles')
  if (values.length < 4 || values.length > 16) {
    fail('BATCH_PLAN_CONFLICT', 'BatchPlan Profile 数量必须在 4–16 之间。')
  }
  const dimensionNames = dimensions.map((dimension) => dimension.name)
  const expectedCells = cartesianCells(dimensions)
  if (values.length !== expectedCells.length) {
    fail('BATCH_PLAN_CONFLICT', 'Profile 集合不是声明维度的完整笛卡尔积。')
  }
  const ids = new Set<string>()
  const planDigests = new Set<string>()
  const fingerprints = new Set<string>()
  const realizations = new Set<string>()
  return values.map((value, index) => {
    const profile = record(value, `profiles[${index}]`)
    exactKeys(
      profile,
      ['id', 'cells', 'plan_sha256', 'realization', 'estimated_memory_mb'],
      `profiles[${index}]`,
    )
    const id = string(profile.id, `profiles[${index}].id`, IDENTIFIER)
    const planSha256 = string(profile.plan_sha256, `profiles[${index}].plan_sha256`, SHA256)
    if (ids.has(id) || planDigests.has(planSha256)) {
      fail('BATCH_PLAN_CONFLICT', 'Profile ID 与来源 Plan digest 必须唯一。')
    }
    ids.add(id)
    planDigests.add(planSha256)
    const cellsValue = record(profile.cells, `profiles[${index}].cells`)
    exactKeys(cellsValue, dimensionNames, `profiles[${index}].cells`)
    const cells: Record<string, string> = {}
    dimensions.forEach((dimension) => {
      const levelId = string(cellsValue[dimension.name], `profiles[${index}].cells.${dimension.name}`)
      if (!dimension.levels.some((level) => level.id === levelId)) {
        fail('BATCH_PLAN_CONFLICT', 'Profile 引用了未声明的维度 level。')
      }
      cells[dimension.name] = levelId
    })
    if (!same(cells, expectedCells[index])) {
      fail('BATCH_PLAN_CONFLICT', 'Profile 没有遵循声明维度与 level 的 canonical 顺序。')
    }
    const realizationValue = record(profile.realization, `profiles[${index}].realization`)
    exactKeys(
      realizationValue,
      ['subject_version', 'subject_source_ref', 'target_root', 'static_root_fingerprint'],
      `profiles[${index}].realization`,
    )
    const realization = {
      subject_version: string(realizationValue.subject_version, 'realization.subject_version'),
      subject_source_ref: string(realizationValue.subject_source_ref, 'realization.subject_source_ref'),
      target_root: string(realizationValue.target_root, 'realization.target_root'),
      static_root_fingerprint: string(
        realizationValue.static_root_fingerprint,
        'realization.static_root_fingerprint',
        SHA256,
      ),
    }
    if (!safeRelativeDirectory(realization.subject_source_ref) || !safeRelativeDirectory(realization.target_root)) {
      fail('BATCH_PLAN_CONFLICT', 'Profile 实现映射必须使用安全相对目录。')
    }
    const encodedRealization = canonicalJson(realization)
    if (fingerprints.has(realization.static_root_fingerprint) || realizations.has(encodedRealization)) {
      fail('BATCH_PLAN_CONFLICT', '每个 Profile 必须有唯一实现映射与静态 fingerprint。')
    }
    fingerprints.add(realization.static_root_fingerprint)
    realizations.add(encodedRealization)
    return {
      id,
      cells,
      plan_sha256: planSha256,
      realization,
      estimated_memory_mb: rangedInteger(
        profile.estimated_memory_mb,
        `profiles[${index}].estimated_memory_mb`,
        1,
        8192,
      ),
    }
  })
}

function parsePolicy(value: unknown): BatchExecutionPolicy {
  const policy = record(value, 'execution_policy')
  exactKeys(
    policy,
    [
      'order_algorithm',
      'seed',
      'perturbation_repetitions',
      'max_parallel',
      'memory_budget_mb',
      'preflight_between_waves',
      'cleanup_between_waves',
    ],
    'execution_policy',
  )
  if (policy.order_algorithm !== 'SHA256_RANK_V1') {
    fail('BATCH_PLAN_CONFLICT', 'BatchPlan 顺序算法不是 SHA256_RANK_V1。')
  }
  const maxParallel = rangedInteger(policy.max_parallel, 'execution_policy.max_parallel', 1, 2)
  if (policy.preflight_between_waves !== true || policy.cleanup_between_waves !== true) {
    fail('BATCH_PLAN_CONFLICT', '每个 wave 之间必须保留 preflight 与 cleanup 边界。')
  }
  return {
    order_algorithm: 'SHA256_RANK_V1',
    seed: rangedInteger(policy.seed, 'execution_policy.seed', 0, Number.MAX_SAFE_INTEGER),
    perturbation_repetitions: rangedInteger(
      policy.perturbation_repetitions,
      'execution_policy.perturbation_repetitions',
      1,
      4,
    ),
    max_parallel: maxParallel as 1 | 2,
    memory_budget_mb: rangedInteger(policy.memory_budget_mb, 'execution_policy.memory_budget_mb', 1, 16384),
    preflight_between_waves: true,
    cleanup_between_waves: true,
  }
}

async function parseSchedule(
  value: unknown,
  profiles: BatchProfilePlan[],
  policy: BatchExecutionPolicy,
): Promise<BatchScheduleSlot[]> {
  const values = array(value, 'schedule')
  const expectedCount = profiles.length * (1 + policy.perturbation_repetitions)
  if (values.length !== expectedCount) {
    fail('BATCH_PLAN_CONFLICT', 'Schedule 没有且仅有全部 coverage 与 perturbation slot。')
  }
  const profileIds = profiles.map((profile) => profile.id)
  const profileMemory = new Map(profiles.map((profile) => [profile.id, profile.estimated_memory_mb]))
  const slotIds = new Set<string>()
  const schedule = values.map((value, index) => {
    const slot = record(value, `schedule[${index}]`)
    exactKeys(slot, ['slot_id', 'phase', 'repetition', 'wave', 'position', 'profile_id'], `schedule[${index}]`)
    const slotId = string(slot.slot_id, `schedule[${index}].slot_id`, IDENTIFIER)
    const phase = string(slot.phase, `schedule[${index}].phase`) as BatchPhase
    const profileId = string(slot.profile_id, `schedule[${index}].profile_id`, IDENTIFIER)
    if (slotIds.has(slotId) || !PHASES.has(phase) || !profileIds.includes(profileId)) {
      fail('BATCH_PLAN_CONFLICT', 'Schedule slot ID、phase 或 Profile 引用无效。')
    }
    slotIds.add(slotId)
    return {
      slot_id: slotId,
      phase,
      repetition: rangedInteger(slot.repetition, `schedule[${index}].repetition`, 0, 4),
      wave: rangedInteger(slot.wave, `schedule[${index}].wave`, 1, Number.MAX_SAFE_INTEGER),
      position: rangedInteger(slot.position, `schedule[${index}].position`, 1, 2),
      profile_id: profileId,
    }
  })
  const coverage = schedule.filter((slot) => slot.phase === 'COVERAGE')
  if (
    !same(coverage.map((slot) => slot.profile_id), profileIds) ||
    coverage.some((slot, index) => slot.repetition !== 0 || slot.wave !== index + 1 || slot.position !== 1)
  ) {
    fail('BATCH_PLAN_CONFLICT', 'Coverage 必须按 canonical Profile 顺序严格串行。')
  }
  if (!same(schedule, [...coverage, ...schedule.filter((slot) => slot.phase === 'PERTURBATION')])) {
    fail('BATCH_PLAN_CONFLICT', '全部 coverage slot 必须先于 perturbation。')
  }
  for (let repetition = 1; repetition <= policy.perturbation_repetitions; repetition += 1) {
    const slots = schedule.filter((slot) => slot.phase === 'PERTURBATION' && slot.repetition === repetition)
    const expectedOrder = await seededProfileOrder(profileIds, policy.seed, repetition)
    if (!same(slots.map((slot) => slot.profile_id), expectedOrder)) {
      fail('BATCH_PLAN_CONFLICT', `Perturbation ${repetition} 没有遵循 SHA256_RANK_V1。`)
    }
    const waves = [...new Set(slots.map((slot) => slot.wave))]
    if (!same(waves, waves.map((_, index) => index + 1))) {
      fail('BATCH_PLAN_CONFLICT', `Perturbation ${repetition} wave 不连续。`)
    }
    for (const wave of waves) {
      const members = slots.filter((slot) => slot.wave === wave)
      if (
        members.length > policy.max_parallel ||
        !same(members.map((slot) => slot.position), members.map((_, index) => index + 1)) ||
        members.reduce((total, slot) => total + (profileMemory.get(slot.profile_id) ?? 0), 0) >
          policy.memory_budget_mb
      ) {
        fail('BATCH_PLAN_CONFLICT', `Perturbation ${repetition} wave ${wave} 越过并行或内存预算。`)
      }
    }
  }
  if (schedule.some((slot) => slot.phase === 'PERTURBATION' && (slot.repetition < 1 || slot.repetition > policy.perturbation_repetitions))) {
    fail('BATCH_PLAN_CONFLICT', 'Perturbation repetition 不连续或越界。')
  }
  return schedule
}

async function parseBatchPlan(value: unknown): Promise<BatchPlan> {
  const plan = record(value, 'sealed-batch-plan.json')
  exactKeys(
    plan,
    [
      'schema_version',
      'batch_id',
      'version',
      'question',
      'primary_variable',
      'dimensions',
      'profiles',
      'execution_policy',
      'schedule',
      'outcomes',
      'limits',
      'reproduction_steps',
      'cleanup_steps',
      'seal',
    ],
    'BatchPlan',
  )
  if (plan.schema_version !== '0.1') fail('BATCH_VERSION_UNSUPPORTED', 'BatchPlan 版本不受支持。')
  const dimensions = parseDimensions(plan.dimensions)
  const profiles = parseProfiles(plan.profiles, dimensions)
  const policy = parsePolicy(plan.execution_policy)
  const schedule = await parseSchedule(plan.schedule, profiles, policy)
  const profileIds = profiles.map((profile) => profile.id)
  const outcomeIds = new Set<string>()
  const outcomes = array(plan.outcomes, 'outcomes').map((value, index) => {
    const outcome = record(value, `outcomes[${index}]`)
    exactKeys(outcome, ['assertion_id', 'expected_actual'], `outcomes[${index}]`)
    const assertionId = string(outcome.assertion_id, `outcomes[${index}].assertion_id`)
    if (outcomeIds.has(assertionId)) fail('BATCH_PLAN_CONFLICT', 'BatchPlan outcome ID 重复。')
    outcomeIds.add(assertionId)
    const expected = record(outcome.expected_actual, `outcomes[${index}].expected_actual`)
    exactKeys(expected, profileIds, `outcomes[${index}].expected_actual`)
    return { assertion_id: assertionId, expected_actual: { ...expected } }
  })
  if (outcomes.length < 1 || outcomes.length > 64) {
    fail('BATCH_PLAN_CONFLICT', 'BatchPlan 必须声明 1–64 个 outcome。')
  }
  const seal = record(plan.seal, 'seal')
  exactKeys(seal, ['algorithm', 'digest'], 'seal')
  if (seal.algorithm !== 'sha256') fail('BATCH_PLAN_SEAL_MISMATCH', 'BatchPlan seal 算法无效。')
  const digest = string(seal.digest, 'seal.digest', SHA256)
  const unsigned = { ...plan }
  delete unsigned.seal
  if ((await sha256Hex(new Blob([canonicalJson(unsigned)]))) !== digest) {
    fail('BATCH_PLAN_SEAL_MISMATCH', 'BatchPlan seal 与规范内容不一致。')
  }
  return {
    schema_version: '0.1',
    batch_id: string(plan.batch_id, 'batch_id', IDENTIFIER),
    version: rangedInteger(plan.version, 'version', 1, Number.MAX_SAFE_INTEGER),
    question: string(plan.question, 'question'),
    primary_variable: parsePrimary(plan.primary_variable, 'primary_variable'),
    dimensions,
    profiles,
    execution_policy: policy,
    schedule,
    outcomes,
    limits: parseStringList(plan.limits, 'limits'),
    reproduction_steps: parseStringList(plan.reproduction_steps, 'reproduction_steps'),
    cleanup_steps: parseStringList(plan.cleanup_steps, 'cleanup_steps'),
    seal: { algorithm: 'sha256', digest },
  }
}

function parseSource(value: unknown, name: string): BatchSource | null {
  if (value === null) return null
  const source = record(value, name)
  exactKeys(
    source,
    [
      'run_id',
      'created_at',
      'execution_status',
      'verdict',
      'plan',
      'random_seed',
      'primary_variable',
      'bundle_sha256',
      'control_projection_sha256',
      'preflight_complete',
      'cleanup_complete',
      'browser_complete',
      'static_root_fingerprint',
    ],
    name,
  )
  const executionStatus = string(source.execution_status, `${name}.execution_status`) as ExecutionStatus
  const verdict = string(source.verdict, `${name}.verdict`) as Verdict
  if (!EXECUTION_STATUSES.has(executionStatus) || !VERDICTS.has(verdict)) {
    fail('BATCH_INVALID', '来源 Run 状态或 Verdict 不受支持。')
  }
  const plan = record(source.plan, `${name}.plan`)
  exactKeys(plan, ['id', 'version', 'sha256'], `${name}.plan`)
  const primary = record(source.primary_variable, `${name}.primary_variable`)
  exactKeys(
    primary,
    primary.unit === undefined
      ? ['name', 'role', 'value', 'source']
      : ['name', 'role', 'value', 'source', 'unit'],
    `${name}.primary_variable`,
  )
  if (primary.role !== 'PRIMARY') fail('BATCH_REFERENCE_MISMATCH', '来源主要变量角色无效。')
  const fingerprint =
    source.static_root_fingerprint === null
      ? null
      : string(source.static_root_fingerprint, `${name}.static_root_fingerprint`, SHA256)
  return {
    run_id: string(source.run_id, `${name}.run_id`),
    created_at: string(source.created_at, `${name}.created_at`),
    execution_status: executionStatus,
    verdict,
    plan: {
      id: string(plan.id, `${name}.plan.id`),
      version: rangedInteger(plan.version, `${name}.plan.version`, 0, Number.MAX_SAFE_INTEGER),
      sha256: string(plan.sha256, `${name}.plan.sha256`, SHA256),
    },
    random_seed: integer(source.random_seed, `${name}.random_seed`),
    primary_variable: {
      name: string(primary.name, `${name}.primary_variable.name`),
      role: 'PRIMARY',
      value: primary.value,
      source: string(primary.source, `${name}.primary_variable.source`),
      ...(primary.unit === undefined ? {} : { unit: string(primary.unit, `${name}.primary_variable.unit`) }),
    },
    bundle_sha256: string(source.bundle_sha256, `${name}.bundle_sha256`, SHA256),
    control_projection_sha256: string(
      source.control_projection_sha256,
      `${name}.control_projection_sha256`,
      SHA256,
    ),
    preflight_complete: boolean(source.preflight_complete, `${name}.preflight_complete`),
    cleanup_complete: boolean(source.cleanup_complete, `${name}.cleanup_complete`),
    browser_complete: boolean(source.browser_complete, `${name}.browser_complete`),
    static_root_fingerprint: fingerprint,
  }
}

function parseTimestamp(value: string): number | null {
  if (!/(Z|[+-]\d{2}:\d{2})$/.test(value)) return null
  const parsed = Date.parse(value)
  return Number.isFinite(parsed) ? parsed : null
}

function waveKey(slot: BatchScheduleSlot): string {
  return `${slot.phase === 'COVERAGE' ? 0 : 1}:${slot.repetition}:${slot.wave}`
}

async function parseAnalysis(
  value: unknown,
  manifest: BatchAnalysisManifest,
  batchPlan: BatchPlan,
): Promise<BatchAnalysis> {
  const analysis = record(value, 'batch-analysis.json')
  exactKeys(
    analysis,
    [
      'schema_version',
      'analysis_id',
      'analysis_type',
      'rule_version',
      'coverage_status',
      'hypothesis_status',
      'runtime_overlap_claim',
      'batch_plan',
      'primary_variable',
      'execution_policy',
      'reasons',
      'slots',
      'profiles',
      'unplanned_differences',
      'limits',
    ],
    'batch-analysis.json',
  )
  if (
    analysis.schema_version !== '0.1' ||
    analysis.analysis_type !== 'PREREGISTERED_FULL_FACTORIAL_BATCH'
  ) {
    fail('BATCH_VERSION_UNSUPPORTED', 'BatchAnalysis 类型或版本不受支持。')
  }
  if (analysis.rule_version !== 'full-factorial-batch/0.1') {
    fail('BATCH_RULE_UNSUPPORTED', 'BatchAnalysis 规则版本不受支持。')
  }
  if (analysis.runtime_overlap_claim !== 'NOT_PROVEN') {
    fail('BATCH_STATE_CONFLICT', 'M8 不能宣称 wave 已证明真实并行。')
  }
  const analysisId = string(analysis.analysis_id, 'analysis_id', ANALYSIS_ID)
  if (analysisId !== manifest.analysis_id) {
    fail('BATCH_REFERENCE_MISMATCH', 'Analysis ID 与 Manifest 不一致。')
  }
  const planReference = record(analysis.batch_plan, 'analysis.batch_plan')
  exactKeys(planReference, ['id', 'version', 'sha256'], 'analysis.batch_plan')
  if (
    planReference.id !== batchPlan.batch_id ||
    planReference.version !== batchPlan.version ||
    planReference.sha256 !== batchPlan.seal.digest ||
    !same(analysis.primary_variable, batchPlan.primary_variable) ||
    !same(analysis.execution_policy, batchPlan.execution_policy) ||
    !same(analysis.limits, batchPlan.limits)
  ) {
    fail('BATCH_REFERENCE_MISMATCH', 'BatchAnalysis 与 sealed BatchPlan 不一致。')
  }
  const reasons = array(analysis.reasons, 'reasons').map((value, index) => {
    const reason = record(value, `reasons[${index}]`)
    exactKeys(reason, ['code', 'message'], `reasons[${index}]`)
    return {
      code: string(reason.code, `reasons[${index}].code`),
      message: string(reason.message, `reasons[${index}].message`),
    }
  })
  if (reasons.length === 0 || new Set(reasons.map((reason) => reason.code)).size !== reasons.length) {
    fail('BATCH_INVALID', 'BatchAnalysis 必须提供不重复的稳定 reason。')
  }
  const profilePlans = new Map(batchPlan.profiles.map((profile) => [profile.id, profile]))
  const outcomePlans = new Map(batchPlan.outcomes.map((outcome) => [outcome.assertion_id, outcome]))
  const slots = array(analysis.slots, 'slots').map((value, index): BatchAnalysisSlot => {
    const slot = record(value, `slots[${index}]`)
    exactKeys(
      slot,
      ['slot_id', 'phase', 'repetition', 'wave', 'position', 'profile_id', 'source', 'outcomes'],
      `slots[${index}]`,
    )
    const scheduleSlot = batchPlan.schedule[index]
    if (!scheduleSlot) fail('BATCH_REFERENCE_MISMATCH', 'Analysis 包含计划外 slot。')
    const identity = {
      slot_id: string(slot.slot_id, `slots[${index}].slot_id`, IDENTIFIER),
      phase: string(slot.phase, `slots[${index}].phase`) as BatchPhase,
      repetition: integer(slot.repetition, `slots[${index}].repetition`),
      wave: integer(slot.wave, `slots[${index}].wave`),
      position: integer(slot.position, `slots[${index}].position`),
      profile_id: string(slot.profile_id, `slots[${index}].profile_id`, IDENTIFIER),
    }
    if (!same(identity, scheduleSlot)) {
      fail('BATCH_REFERENCE_MISMATCH', 'Analysis slot 顺序或 Profile 与 BatchPlan 不一致。')
    }
    const source = parseSource(slot.source, `slots[${index}].source`)
    const profile = profilePlans.get(identity.profile_id)!
    if (
      source &&
      (source.plan.sha256 !== profile.plan_sha256 ||
        source.primary_variable.name !== batchPlan.primary_variable.name ||
        source.primary_variable.source !== batchPlan.primary_variable.source ||
        source.primary_variable.unit !== batchPlan.primary_variable.unit ||
        !same(source.primary_variable.value, identity.profile_id))
    ) {
      fail('BATCH_REFERENCE_MISMATCH', '来源 Run 与 slot/Profile 绑定不一致。')
    }
    const seenOutcomes = new Set<string>()
    const outcomes = array(slot.outcomes, `slots[${index}].outcomes`).map(
      (value, outcomeIndex): BatchOutcomeObservation => {
        const outcome = record(value, `slots[${index}].outcomes[${outcomeIndex}]`)
        exactKeys(
          outcome,
          ['assertion_id', 'expected_actual', 'actual', 'matches'],
          `slots[${index}].outcomes[${outcomeIndex}]`,
        )
        const assertionId = string(outcome.assertion_id, 'outcome.assertion_id')
        const definition = outcomePlans.get(assertionId)
        if (!definition || seenOutcomes.has(assertionId)) {
          fail('BATCH_REFERENCE_MISMATCH', 'Analysis outcome 集合与 BatchPlan 不一致。')
        }
        seenOutcomes.add(assertionId)
        const expected = definition.expected_actual[identity.profile_id]
        const matches = boolean(outcome.matches, 'outcome.matches')
        if (!same(outcome.expected_actual, expected) || matches !== same(expected, outcome.actual)) {
          fail('BATCH_STATE_CONFLICT', 'Outcome matches 与预期/实际值冲突。')
        }
        return {
          assertion_id: assertionId,
          expected_actual: outcome.expected_actual,
          actual: outcome.actual,
          matches,
        }
      },
    )
    if (outcomes.length !== outcomePlans.size) {
      fail('BATCH_REFERENCE_MISMATCH', 'Analysis slot 缺少预注册 outcome。')
    }
    return { ...identity, source, outcomes }
  })
  if (slots.length !== batchPlan.schedule.length) {
    fail('BATCH_REFERENCE_MISMATCH', 'Analysis slot 数量与 BatchPlan 不一致。')
  }
  const orderedDigests = slots.map((slot) => slot.source?.bundle_sha256 ?? 'MISSING')
  const expectedId = `batch_${(
    await sha256Hex(
      new Blob([
        canonicalJson({
          schema_version: '0.1',
          rule_version: 'full-factorial-batch/0.1',
          batch_plan_sha256: batchPlan.seal.digest,
          ordered_bundle_sha256: orderedDigests,
        }),
      ]),
    )
  ).slice(0, 24)}`
  if (analysisId !== expectedId) {
    fail('BATCH_REFERENCE_MISMATCH', 'Analysis ID 不能由 BatchPlan 与有序来源 Bundle 重建。')
  }
  const profileSummaries = array(analysis.profiles, 'profiles').map(
    (value, index): BatchProfileSummary => {
      const summary = record(value, `profiles[${index}]`)
      exactKeys(
        summary,
        ['id', 'cells', 'occurrence_count', 'completed_count', 'mismatch_count'],
        `profiles[${index}]`,
      )
      const planProfile = batchPlan.profiles[index]
      if (!planProfile || summary.id !== planProfile.id || !same(summary.cells, planProfile.cells)) {
        fail('BATCH_REFERENCE_MISMATCH', 'Analysis Profile 摘要与 BatchPlan 不一致。')
      }
      const profileSlots = slots.filter((slot) => slot.profile_id === planProfile.id)
      const expected = {
        id: planProfile.id,
        cells: planProfile.cells,
        occurrence_count: profileSlots.length,
        completed_count: profileSlots.filter((slot) => slot.source?.execution_status === 'COMPLETED').length,
        mismatch_count: profileSlots.flatMap((slot) => slot.outcomes).filter((outcome) => !outcome.matches).length,
      }
      const observed = {
        id: summary.id,
        cells: summary.cells,
        occurrence_count: integer(summary.occurrence_count, `profiles[${index}].occurrence_count`),
        completed_count: integer(summary.completed_count, `profiles[${index}].completed_count`),
        mismatch_count: integer(summary.mismatch_count, `profiles[${index}].mismatch_count`),
      }
      if (!same(observed, expected)) {
        fail('BATCH_STATE_CONFLICT', 'Profile 计数不能由 slot 事实重建。')
      }
      return expected
    },
  )
  if (profileSummaries.length !== batchPlan.profiles.length) {
    fail('BATCH_REFERENCE_MISMATCH', 'Analysis Profile 集合与 BatchPlan 不一致。')
  }
  const unplannedDifferences = array(analysis.unplanned_differences, 'unplanned_differences').map(
    (value, index) => {
      const difference = record(value, `unplanned_differences[${index}]`)
      exactKeys(
        difference,
        ['slot_id', 'assertion_id', 'baseline', 'observed'],
        `unplanned_differences[${index}]`,
      )
      const slotId = string(difference.slot_id, 'difference.slot_id', IDENTIFIER)
      const assertionId = string(difference.assertion_id, 'difference.assertion_id')
      if (!slots.some((slot) => slot.slot_id === slotId) || outcomePlans.has(assertionId)) {
        fail('BATCH_REFERENCE_MISMATCH', '未声明差异引用了无效 slot 或预注册 outcome。')
      }
      return { slot_id: slotId, assertion_id: assertionId, baseline: difference.baseline, observed: difference.observed }
    },
  )
  const reasonCodes = new Set(reasons.map((reason) => reason.code))
  const requiredReasonCodes = new Set<string>()
  let incomplete = false
  let contaminated = false
  if (slots.some((slot) => slot.source === null)) {
    incomplete = true
    requiredReasonCodes.add('SLOT_MISSING')
  }
  const sources = slots.flatMap((slot) => (slot.source ? [slot.source] : []))
  if (sources.some((source) => source.execution_status !== 'COMPLETED')) {
    incomplete = true
    requiredReasonCodes.add('RUN_NOT_COMPLETED')
  }
  const contaminationCheck = (condition: boolean, code: string) => {
    if (!condition) return
    contaminated = true
    requiredReasonCodes.add(code)
  }
  contaminationCheck(new Set(sources.map((source) => source.run_id)).size !== sources.length, 'RUN_ID_REUSED')
  contaminationCheck(new Set(sources.map((source) => source.bundle_sha256)).size !== sources.length, 'BUNDLE_REUSED')
  contaminationCheck(
    new Set(sources.map((source) => source.control_projection_sha256)).size > 1,
    'CONTROL_PROJECTION_MISMATCH',
  )
  contaminationCheck(new Set(sources.map((source) => source.random_seed)).size > 1, 'SOURCE_RANDOM_SEED_MISMATCH')
  const sourceEvidenceIncomplete = reasonCodes.has('SOURCE_EVIDENCE_INCOMPLETE')
  if (!sourceEvidenceIncomplete) {
    contaminationCheck(sources.some((source) => !source.preflight_complete), 'PREFLIGHT_BOUNDARY_FAILED')
    contaminationCheck(sources.some((source) => !source.cleanup_complete), 'CLEANUP_BOUNDARY_FAILED')
    contaminationCheck(sources.some((source) => !source.browser_complete), 'BROWSER_BOUNDARY_FAILED')
  }
  contaminationCheck(
    slots.some((slot) => {
      const profile = profilePlans.get(slot.profile_id)!
      return Boolean(slot.source && slot.source.static_root_fingerprint !== profile.realization.static_root_fingerprint)
    }),
    'STATIC_ROOT_FINGERPRINT_MISMATCH',
  )
  const timeBySlot = new Map(slots.map((slot) => [slot.slot_id, slot.source ? parseTimestamp(slot.source.created_at) : null]))
  contaminationCheck(sources.some((source) => parseTimestamp(source.created_at) === null), 'SOURCE_TIME_INVALID')
  const waves: BatchAnalysisSlot[][] = []
  slots.forEach((slot) => {
    if (!waves.length || waveKey(waves.at(-1)![0]!) !== waveKey(slot)) waves.push([])
    waves.at(-1)!.push(slot)
  })
  let waveOrderMismatch = false
  for (let index = 1; index < waves.length; index += 1) {
    const earlier = waves[index - 1]!.flatMap((slot) => {
      const value = timeBySlot.get(slot.slot_id)
      return value === null || value === undefined ? [] : [value]
    })
    const later = waves[index]!.flatMap((slot) => {
      const value = timeBySlot.get(slot.slot_id)
      return value === null || value === undefined ? [] : [value]
    })
    if (earlier.length && later.length && Math.max(...earlier) >= Math.min(...later)) {
      waveOrderMismatch = true
      break
    }
  }
  contaminationCheck(waveOrderMismatch, 'WAVE_ORDER_MISMATCH')
  contaminationCheck(unplannedDifferences.length > 0, 'UNDECLARED_OUTCOME_DRIFT')
  const observedByProfile = new Map<string, unknown[]>()
  slots.forEach((slot) => {
    if (!slot.source) return
    slot.outcomes.forEach((outcome) => {
      const key = `${slot.profile_id}\u0000${outcome.assertion_id}`
      const values = observedByProfile.get(key) ?? []
      values.push(outcome.actual)
      observedByProfile.set(key, values)
    })
  })
  contaminationCheck(
    [...observedByProfile.values()].some((values) => values.slice(1).some((value) => !same(values[0], value))),
    'PERTURBATION_OUTCOME_DRIFT',
  )
  if ([...reasonCodes].some((code) => CONTAMINATION_REASONS.has(code))) contaminated = true
  if ([...reasonCodes].some((code) => INCOMPLETE_REASONS.has(code))) incomplete = true
  for (const code of requiredReasonCodes) {
    if (!reasonCodes.has(code)) fail('BATCH_STATE_CONFLICT', `BatchAnalysis 缺少可重算 reason：${code}。`)
  }
  const mismatchCount = slots.flatMap((slot) => slot.outcomes).filter((outcome) => !outcome.matches).length
  let expectedCoverage: BatchCoverageStatus
  let expectedHypothesis: BatchHypothesisStatus
  let terminalReason: string | null = null
  if (contaminated) {
    expectedCoverage = 'INCONCLUSIVE'
    expectedHypothesis = 'INCONCLUSIVE'
  } else if (incomplete) {
    expectedCoverage = 'INCOMPLETE'
    expectedHypothesis = 'INCONCLUSIVE'
  } else if (mismatchCount > 0) {
    expectedCoverage = 'COMPLETE'
    expectedHypothesis = 'CONTRADICTED'
    terminalReason = 'BATCH_HYPOTHESIS_CONTRADICTED'
  } else {
    expectedCoverage = 'COMPLETE'
    expectedHypothesis = 'SUPPORTED'
    terminalReason = 'BATCH_HYPOTHESIS_SUPPORTED'
  }
  const coverageStatus = string(analysis.coverage_status, 'coverage_status') as BatchCoverageStatus
  const hypothesisStatus = string(analysis.hypothesis_status, 'hypothesis_status') as BatchHypothesisStatus
  if (
    !COVERAGE_STATUSES.has(coverageStatus) ||
    !HYPOTHESIS_STATUSES.has(hypothesisStatus) ||
    coverageStatus !== expectedCoverage ||
    hypothesisStatus !== expectedHypothesis ||
    (terminalReason !== null && !reasonCodes.has(terminalReason))
  ) {
    fail('BATCH_STATE_CONFLICT', 'CoverageStatus、HypothesisStatus 与 slot/reason 事实冲突。')
  }
  return {
    schema_version: '0.1',
    analysis_id: analysisId,
    analysis_type: 'PREREGISTERED_FULL_FACTORIAL_BATCH',
    rule_version: 'full-factorial-batch/0.1',
    coverage_status: coverageStatus,
    hypothesis_status: hypothesisStatus,
    runtime_overlap_claim: 'NOT_PROVEN',
    batch_plan: { id: batchPlan.batch_id, version: batchPlan.version, sha256: batchPlan.seal.digest },
    primary_variable: batchPlan.primary_variable,
    execution_policy: batchPlan.execution_policy,
    reasons,
    slots,
    profiles: profileSummaries,
    unplanned_differences: unplannedDifferences,
    limits: batchPlan.limits,
  }
}

export async function loadBatchAnalysisFromBlobs(
  entries: ReadonlyMap<string, Blob>,
): Promise<LoadedBatchAnalysis> {
  if (entries.size !== MAX_FILES) {
    fail('BATCH_FILE_SET_MISMATCH', 'BatchAnalysis 必须且只能包含四个冻结文件。')
  }
  let selectedBytes = 0
  for (const [path, blob] of entries) {
    normalizeBundlePath(path)
    if (blob.size > MAX_FILE_BYTES) fail('BATCH_FILE_SIZE_LIMIT', 'BatchAnalysis 文件超过 10 MiB。')
    selectedBytes += blob.size
    if (selectedBytes > MAX_BUNDLE_BYTES) fail('BATCH_BUNDLE_SIZE_LIMIT', 'BatchAnalysis 包超过 30 MiB。')
  }
  const manifestBlob = entries.get('batch-analysis-manifest.json')
  if (!manifestBlob) fail('BATCH_ROOT_MISSING', 'BatchAnalysis 缺少 Manifest。')
  const manifest = parseManifest(await parseJson(manifestBlob, 'batch-analysis-manifest.json'))
  const allowed = new Set(['batch-analysis-manifest.json', ...manifest.files.map((file) => file.path)])
  if ([...entries.keys()].some((path) => !allowed.has(path))) {
    fail('BATCH_FILE_SET_MISMATCH', 'BatchAnalysis 包含未声明文件。')
  }
  let verifiedBytes = 0
  for (const file of manifest.files) {
    const blob = entries.get(file.path)
    if (!blob) fail('BATCH_REFERENCE_MISSING', 'Manifest 引用了缺失文件。')
    if (blob.size !== file.size) fail('BATCH_SIZE_MISMATCH', '文件大小与 Manifest 不一致。')
    if ((await sha256Hex(blob)) !== file.sha256) {
      fail('BATCH_HASH_MISMATCH', '文件 SHA-256 与 Manifest 不一致。')
    }
    verifiedBytes += blob.size
  }
  const batchPlan = await parseBatchPlan(
    await parseJson(entries.get('sealed-batch-plan.json')!, 'sealed-batch-plan.json'),
  )
  const analysis = await parseAnalysis(
    await parseJson(entries.get('batch-analysis.json')!, 'batch-analysis.json'),
    manifest,
    batchPlan,
  )
  return {
    analysis,
    batchPlan,
    manifest,
    integrity: {
      verified: true,
      authorityVerified: false,
      verifiedFiles: manifest.files.length,
      totalBytes: verifiedBytes,
    },
  }
}

function localPaths(files: File[]): string[] {
  const raw = files.map(
    (file) => (file as File & { webkitRelativePath?: string }).webkitRelativePath || file.name,
  )
  const parts = raw.map((path) => path.split('/'))
  const stripRoot =
    parts.every((segments) => segments.length > 1) &&
    new Set(parts.map((segments) => segments[0])).size === 1
  return parts.map((segments) =>
    normalizeBundlePath((stripRoot ? segments.slice(1) : segments).join('/')),
  )
}

export async function loadLocalBatchAnalysis(
  input: FileList | File[],
): Promise<LoadedBatchAnalysis> {
  const files = Array.from(input)
  if (files.length === 0) fail('BATCH_EMPTY_SELECTION', '没有选择任何 BatchAnalysis 文件。')
  if (files.length > MAX_FILES) fail('BATCH_FILE_SET_MISMATCH', 'BatchAnalysis 文件数量超过四个。')
  const paths = localPaths(files)
  if (new Set(paths).size !== paths.length) fail('BATCH_DUPLICATE_PATH', 'BatchAnalysis 包含重复路径。')
  const entries = new Map<string, Blob>()
  files.forEach((file, index) => entries.set(paths[index]!, file))
  return loadBatchAnalysisFromBlobs(entries)
}
