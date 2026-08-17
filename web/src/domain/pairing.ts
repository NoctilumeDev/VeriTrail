import { normalizeBundlePath, sha256Hex } from './bundle'
import { fetchSameOriginFixture, SameOriginFixtureError } from './sameOriginFixture'
import type {
  ExecutionStatus,
  LoadedPairedAnalysis,
  PairedAnalysis,
  PairedAnalysisManifest,
  PairedAnalysisStatus,
  PairedOutcome,
  PairingPlan,
  PairingRole,
  PairingSource,
  Verdict,
} from './types'

const MAX_FILES = 4
const MAX_FILE_BYTES = 10 * 1024 * 1024
const MAX_BUNDLE_BYTES = 30 * 1024 * 1024
const SHA256 = /^[0-9a-f]{64}$/
const ANALYSIS_ID = /^pair_[0-9a-f]{24}$/
const PAIRING_ID = /^[a-z0-9][a-z0-9._-]{1,63}$/
const ROLES: PairingRole[] = [
  'BASELINE',
  'TREATMENT',
  'RESTORED_BASELINE',
  'NEGATIVE_CONTROL',
]
const EXECUTION_STATUSES = new Set<ExecutionStatus>([
  'PLANNED',
  'RUNNING',
  'COMPLETED',
  'ABORTED',
  'ERROR',
])
const VERDICTS = new Set<Verdict>(['PASS', 'FAIL', 'INCONCLUSIVE', 'PENDING'])
const ANALYSIS_STATUSES = new Set<PairedAnalysisStatus>([
  'SUPPORTED',
  'CONTRADICTED',
  'INCONCLUSIVE',
])
const REVIEW_SAMPLE_BASE = '/fixtures/m7-paired-supported'
const REVIEW_SAMPLE_FILES = [
  'paired-analysis-manifest.json',
  'paired-analysis.json',
  'paired-analysis.md',
  'sealed-pairing-plan.json',
] as const

export class PairingLoadError extends Error {
  readonly code: string

  constructor(code: string, message: string) {
    super(message)
    this.name = 'PairingLoadError'
    this.code = code
  }
}

function fail(code: string, message: string): never {
  throw new PairingLoadError(code, message)
}

function record(value: unknown, name: string): Record<string, unknown> {
  if (typeof value !== 'object' || value === null || Array.isArray(value)) {
    fail('PAIRING_INVALID', `${name} 必须是对象。`)
  }
  return value as Record<string, unknown>
}

function string(value: unknown, name: string, pattern?: RegExp): string {
  if (typeof value !== 'string' || !value || (pattern && !pattern.test(value))) {
    fail('PAIRING_INVALID', `${name} 不符合 M7 0.1 契约。`)
  }
  return value
}

function integer(value: unknown, name: string): number {
  if (!Number.isInteger(value)) fail('PAIRING_INVALID', `${name} 必须是整数。`)
  return value as number
}

function array(value: unknown, name: string): unknown[] {
  if (!Array.isArray(value)) fail('PAIRING_INVALID', `${name} 必须是数组。`)
  return value
}

function boolean(value: unknown, name: string): boolean {
  if (typeof value !== 'boolean') fail('PAIRING_INVALID', `${name} 必须是布尔值。`)
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
  const observed = Object.keys(value).sort()
  const wanted = [...expected].sort()
  if (!same(observed, wanted)) fail('PAIRING_INVALID', `${name} 字段集合不符合冻结契约。`)
}

async function parseJson(blob: Blob, name: string): Promise<unknown> {
  try {
    return JSON.parse(await blob.text()) as unknown
  } catch {
    fail('PAIRING_INVALID_JSON', `${name} 不是有效 JSON。`)
  }
}

function parseStringList(value: unknown, name: string): string[] {
  const result = array(value, name).map((item, index) => string(item, `${name}[${index}]`))
  if (result.length === 0) fail('PAIRING_INVALID', `${name} 不能为空。`)
  return result
}

function parseManifest(value: unknown): PairedAnalysisManifest {
  const manifest = record(value, 'paired-analysis-manifest.json')
  exactKeys(manifest, ['schema_version', 'analysis_id', 'files'], 'manifest')
  if (manifest.schema_version !== '0.1') {
    fail('PAIRING_VERSION_UNSUPPORTED', 'PairedAnalysis Manifest 版本不受支持。')
  }
  const files = array(manifest.files, 'manifest.files').map((value, index) => {
    const file = record(value, `manifest.files[${index}]`)
    exactKeys(file, ['path', 'sha256', 'size'], `manifest.files[${index}]`)
    const size = integer(file.size, `manifest.files[${index}].size`)
    if (size < 0 || size > MAX_FILE_BYTES) {
      fail('PAIRING_FILE_SIZE_LIMIT', 'PairedAnalysis 文件超过 10 MiB 上限。')
    }
    return {
      path: normalizeBundlePath(string(file.path, `manifest.files[${index}].path`)),
      sha256: string(file.sha256, `manifest.files[${index}].sha256`, SHA256),
      size,
    }
  })
  const expected = [
    'sealed-pairing-plan.json',
    'paired-analysis.json',
    'paired-analysis.md',
  ]
  const paths = files.map((file) => file.path)
  if (files.length !== 3 || new Set(paths).size !== 3 || expected.some((path) => !paths.includes(path))) {
    fail('PAIRING_FILE_SET_MISMATCH', 'Manifest 必须且只能声明 PairingPlan、JSON 与 Markdown。')
  }
  return {
    schema_version: '0.1',
    analysis_id: string(manifest.analysis_id, 'manifest.analysis_id', ANALYSIS_ID),
    files,
  }
}

async function parsePairingPlan(value: unknown): Promise<PairingPlan> {
  const plan = record(value, 'sealed-pairing-plan.json')
  exactKeys(
    plan,
    [
      'schema_version',
      'pairing_id',
      'version',
      'question',
      'primary_variable',
      'roles',
      'sequence',
      'warmup',
      'outcomes',
      'limits',
      'reproduction_steps',
      'cleanup_steps',
      'seal',
    ],
    'PairingPlan',
  )
  if (plan.schema_version !== '0.1') fail('PAIRING_VERSION_UNSUPPORTED', 'PairingPlan 版本不受支持。')
  const primary = record(plan.primary_variable, 'primary_variable')
  exactKeys(
    primary,
    primary.unit === undefined ? ['name', 'source'] : ['name', 'source', 'unit'],
    'primary_variable',
  )
  const primaryDefinition = {
    name: string(primary.name, 'primary_variable.name'),
    source: string(primary.source, 'primary_variable.source'),
    ...(primary.unit === undefined ? {} : { unit: string(primary.unit, 'primary_variable.unit') }),
  }
  const rolesValue = record(plan.roles, 'roles')
  exactKeys(rolesValue, ROLES, 'roles')
  const roles = {} as PairingPlan['roles']
  for (const role of ROLES) {
    const item = record(rolesValue[role], `roles.${role}`)
    exactKeys(item, ['plan_sha256', 'primary_value'], `roles.${role}`)
    roles[role] = {
      plan_sha256: string(item.plan_sha256, `roles.${role}.plan_sha256`, SHA256),
      primary_value: item.primary_value,
    }
  }
  if (
    same(roles.BASELINE.primary_value, roles.TREATMENT.primary_value) ||
    !same(roles.BASELINE.primary_value, roles.RESTORED_BASELINE.primary_value) ||
    same(roles.NEGATIVE_CONTROL.primary_value, roles.BASELINE.primary_value) ||
    same(roles.NEGATIVE_CONTROL.primary_value, roles.TREATMENT.primary_value) ||
    roles.BASELINE.plan_sha256 !== roles.RESTORED_BASELINE.plan_sha256
  ) {
    fail('PAIRING_PLAN_CONFLICT', '四角色主要变量或恢复基线 Plan 违反 PairingPlan 约束。')
  }
  const sequence = array(plan.sequence, 'sequence').map((item, index) =>
    string(item, `sequence[${index}]`),
  )
  if (!same(sequence, ROLES)) fail('PAIRING_PLAN_CONFLICT', '四角色顺序不是 M7 固定顺序。')
  const warmup = record(plan.warmup, 'warmup')
  if (warmup.mode !== 'NONE' || warmup.iterations !== 0) {
    fail('PAIRING_PLAN_CONFLICT', 'PairingPlan 0.1 只支持 NONE / 0 预热事实。')
  }
  let treatmentEffect = false
  const outcomeIds = new Set<string>()
  const outcomes = array(plan.outcomes, 'outcomes').map((value, index) => {
    const outcome = record(value, `outcomes[${index}]`)
    const assertionId = string(outcome.assertion_id, `outcomes[${index}].assertion_id`)
    if (outcomeIds.has(assertionId)) fail('PAIRING_PLAN_CONFLICT', 'PairingPlan outcome ID 重复。')
    outcomeIds.add(assertionId)
    const expectedValue = record(outcome.expected_actual, `outcomes[${index}].expected_actual`)
    exactKeys(expectedValue, ROLES, `outcomes[${index}].expected_actual`)
    const expected = {} as Record<PairingRole, unknown>
    for (const role of ROLES) expected[role] = expectedValue[role]
    if (
      !same(expected.BASELINE, expected.RESTORED_BASELINE) ||
      !same(expected.BASELINE, expected.NEGATIVE_CONTROL)
    ) {
      fail('PAIRING_PLAN_CONFLICT', '恢复与负对照 outcome 预期必须等于基线。')
    }
    if (!same(expected.BASELINE, expected.TREATMENT)) treatmentEffect = true
    return { assertion_id: assertionId, expected_actual: expected }
  })
  if (outcomes.length === 0 || !treatmentEffect) {
    fail('PAIRING_PLAN_CONFLICT', 'PairingPlan 必须预注册至少一个处理效果。')
  }
  const seal = record(plan.seal, 'seal')
  exactKeys(seal, ['algorithm', 'digest'], 'seal')
  if (seal.algorithm !== 'sha256') fail('PAIRING_PLAN_SEAL_MISMATCH', 'PairingPlan seal 算法无效。')
  const digest = string(seal.digest, 'seal.digest', SHA256)
  const unsigned = { ...plan }
  delete unsigned.seal
  const rebuilt = await sha256Hex(new Blob([canonicalJson(unsigned)]))
  if (rebuilt !== digest) fail('PAIRING_PLAN_SEAL_MISMATCH', 'PairingPlan seal 与规范内容不一致。')
  return {
    schema_version: '0.1',
    pairing_id: string(plan.pairing_id, 'pairing_id', PAIRING_ID),
    version: integer(plan.version, 'version'),
    question: string(plan.question, 'question'),
    primary_variable: primaryDefinition,
    roles,
    sequence: [...ROLES],
    warmup: { mode: 'NONE', iterations: 0 },
    outcomes,
    limits: parseStringList(plan.limits, 'limits'),
    reproduction_steps: parseStringList(plan.reproduction_steps, 'reproduction_steps'),
    cleanup_steps: parseStringList(plan.cleanup_steps, 'cleanup_steps'),
    seal: { algorithm: 'sha256', digest },
  }
}

function parseSource(value: unknown, role: PairingRole): PairingSource {
  const source = record(value, `sources.${role}`)
  exactKeys(
    source,
    [
      'role',
      'run_id',
      'created_at',
      'execution_status',
      'verdict',
      'plan',
      'random_seed',
      'primary_variable',
      'bundle_sha256',
      'control_projection_sha256',
    ],
    `sources.${role}`,
  )
  if (source.role !== role) fail('PAIRING_REFERENCE_MISMATCH', 'PairedAnalysis 来源角色错位。')
  const executionStatus = string(source.execution_status, 'source.execution_status') as ExecutionStatus
  const verdict = string(source.verdict, 'source.verdict') as Verdict
  if (!EXECUTION_STATUSES.has(executionStatus) || !VERDICTS.has(verdict)) {
    fail('PAIRING_INVALID', '来源 Run 状态或 Verdict 不受支持。')
  }
  const plan = record(source.plan, 'source.plan')
  exactKeys(plan, ['id', 'version', 'sha256'], 'source.plan')
  const primary = record(source.primary_variable, 'source.primary_variable')
  exactKeys(
    primary,
    primary.unit === undefined
      ? ['name', 'role', 'value', 'source']
      : ['name', 'role', 'value', 'source', 'unit'],
    'source.primary_variable',
  )
  if (primary.role !== 'PRIMARY') fail('PAIRING_REFERENCE_MISMATCH', '来源主要变量角色无效。')
  return {
    role,
    run_id: string(source.run_id, 'source.run_id'),
    created_at: string(source.created_at, 'source.created_at'),
    execution_status: executionStatus,
    verdict,
    plan: {
      id: string(plan.id, 'source.plan.id'),
      version: integer(plan.version, 'source.plan.version'),
      sha256: string(plan.sha256, 'source.plan.sha256', SHA256),
    },
    random_seed: integer(source.random_seed, 'source.random_seed'),
    primary_variable: {
      name: string(primary.name, 'source.primary_variable.name'),
      source: string(primary.source, 'source.primary_variable.source'),
      role: 'PRIMARY',
      value: primary.value,
      ...(primary.unit === undefined ? {} : { unit: string(primary.unit, 'source.primary_variable.unit') }),
    },
    bundle_sha256: string(source.bundle_sha256, 'source.bundle_sha256', SHA256),
    control_projection_sha256: string(
      source.control_projection_sha256,
      'source.control_projection_sha256',
      SHA256,
    ),
  }
}

async function parseAnalysis(
  value: unknown,
  manifest: PairedAnalysisManifest,
  pairingPlan: PairingPlan,
): Promise<PairedAnalysis> {
  const analysis = record(value, 'paired-analysis.json')
  exactKeys(
    analysis,
    [
      'schema_version',
      'analysis_id',
      'analysis_type',
      'rule_version',
      'analysis_status',
      'attributable',
      'pairing_plan',
      'sequence',
      'warmup',
      'primary_variable',
      'reasons',
      'sources',
      'outcomes',
      'unplanned_differences',
      'limits',
    ],
    'paired-analysis.json',
  )
  if (
    analysis.schema_version !== '0.1' ||
    analysis.analysis_type !== 'FOUR_ROLE_PAIRED_COUNTERFACTUAL'
  ) {
    fail('PAIRING_VERSION_UNSUPPORTED', 'PairedAnalysis 类型或版本不受支持。')
  }
  if (analysis.rule_version !== 'paired-counterfactual/0.1') {
    fail('PAIRING_RULE_UNSUPPORTED', 'PairedAnalysis 规则版本不受支持。')
  }
  const analysisId = string(analysis.analysis_id, 'analysis_id', ANALYSIS_ID)
  if (analysisId !== manifest.analysis_id) {
    fail('PAIRING_REFERENCE_MISMATCH', 'Analysis ID 与 Manifest 不一致。')
  }
  const planReference = record(analysis.pairing_plan, 'analysis.pairing_plan')
  exactKeys(planReference, ['id', 'version', 'sha256'], 'analysis.pairing_plan')
  if (
    planReference.id !== pairingPlan.pairing_id ||
    planReference.version !== pairingPlan.version ||
    planReference.sha256 !== pairingPlan.seal.digest
  ) {
    fail('PAIRING_REFERENCE_MISMATCH', 'Analysis 与 sealed PairingPlan 不一致。')
  }
  if (!same(analysis.sequence, ROLES) || !same(analysis.warmup, pairingPlan.warmup)) {
    fail('PAIRING_REFERENCE_MISMATCH', 'Analysis 顺序或预热事实与 PairingPlan 不一致。')
  }
  if (!same(analysis.primary_variable, pairingPlan.primary_variable)) {
    fail('PAIRING_REFERENCE_MISMATCH', 'Analysis 主要变量定义与 PairingPlan 不一致。')
  }
  const sourcesValue = record(analysis.sources, 'sources')
  exactKeys(sourcesValue, ROLES, 'sources')
  const sources = {} as Record<PairingRole, PairingSource>
  for (const role of ROLES) {
    const source = parseSource(sourcesValue[role], role)
    const expectedPlan = pairingPlan.roles[role]
    if (
      source.plan.sha256 !== expectedPlan.plan_sha256 ||
      source.primary_variable.name !== pairingPlan.primary_variable.name ||
      source.primary_variable.source !== pairingPlan.primary_variable.source ||
      source.primary_variable.unit !== pairingPlan.primary_variable.unit ||
      !same(source.primary_variable.value, expectedPlan.primary_value)
    ) {
      fail('PAIRING_REFERENCE_MISMATCH', `${role} 与 PairingPlan 角色绑定不一致。`)
    }
    sources[role] = source
  }
  const orderedBundles = ROLES.map((role) => sources[role].bundle_sha256)
  const expectedId = `pair_${(
    await sha256Hex(
      new Blob([
        canonicalJson({
          schema_version: '0.1',
          rule_version: 'paired-counterfactual/0.1',
          pairing_plan_sha256: pairingPlan.seal.digest,
          ordered_bundle_sha256: orderedBundles,
        }),
      ]),
    )
  ).slice(0, 24)}`
  if (analysisId !== expectedId) {
    fail('PAIRING_REFERENCE_MISMATCH', 'Analysis ID 不能由 PairingPlan 与来源 Bundle 重建。')
  }
  const status = string(analysis.analysis_status, 'analysis_status') as PairedAnalysisStatus
  if (!ANALYSIS_STATUSES.has(status)) fail('PAIRING_INVALID', 'PairedAnalysis 状态不受支持。')
  const attributable = boolean(analysis.attributable, 'attributable')
  const reasons = array(analysis.reasons, 'reasons').map((value, index) => {
    const reason = record(value, `reasons[${index}]`)
    exactKeys(reason, ['code', 'message'], `reasons[${index}]`)
    return {
      code: string(reason.code, `reasons[${index}].code`),
      message: string(reason.message, `reasons[${index}].message`),
    }
  })
  if (reasons.length === 0) fail('PAIRING_INVALID', 'PairedAnalysis 至少需要一个稳定原因。')
  const outcomeDefinitions = new Map(
    pairingPlan.outcomes.map((outcome) => [outcome.assertion_id, outcome] as const),
  )
  const outcomes = array(analysis.outcomes, 'outcomes').map((value, index): PairedOutcome => {
    const outcome = record(value, `outcomes[${index}]`)
    exactKeys(outcome, ['assertion_id', 'roles'], `outcomes[${index}]`)
    const assertionId = string(outcome.assertion_id, `outcomes[${index}].assertion_id`)
    const definition = outcomeDefinitions.get(assertionId)
    if (!definition) fail('PAIRING_REFERENCE_MISMATCH', 'Analysis 包含未预注册 outcome。')
    const roleValues = record(outcome.roles, `outcomes[${index}].roles`)
    exactKeys(roleValues, ROLES, `outcomes[${index}].roles`)
    const roles = {} as PairedOutcome['roles']
    for (const role of ROLES) {
      const observation = record(roleValues[role], `outcomes[${index}].roles.${role}`)
      exactKeys(
        observation,
        ['expected_actual', 'actual', 'matches'],
        `outcomes[${index}].roles.${role}`,
      )
      const expectedActual = observation.expected_actual
      if (!same(expectedActual, definition.expected_actual[role])) {
        fail('PAIRING_REFERENCE_MISMATCH', 'Outcome 预期与 PairingPlan 不一致。')
      }
      const actual = observation.actual
      const matches = boolean(observation.matches, 'outcome.matches')
      if (matches !== same(expectedActual, actual)) {
        fail('PAIRING_STATE_CONFLICT', 'Outcome matches 与预期/实际值冲突。')
      }
      roles[role] = { expected_actual: expectedActual, actual, matches }
    }
    return { assertion_id: assertionId, roles }
  })
  if (
    outcomes.length !== outcomeDefinitions.size ||
    new Set(outcomes.map((outcome) => outcome.assertion_id)).size !== outcomes.length
  ) {
    fail('PAIRING_REFERENCE_MISMATCH', 'Analysis outcome 集合与 PairingPlan 不一致。')
  }
  const unplannedDifferences = array(
    analysis.unplanned_differences,
    'unplanned_differences',
  ).map((value, index) => {
    const difference = record(value, `unplanned_differences[${index}]`)
    exactKeys(
      difference,
      ['role', 'assertion_id', 'baseline', 'observed'],
      `unplanned_differences[${index}]`,
    )
    const role = string(difference.role, 'difference.role') as PairingRole
    if (!ROLES.includes(role)) fail('PAIRING_INVALID', '未声明漂移角色无效。')
    return {
      role,
      assertion_id: string(difference.assertion_id, 'difference.assertion_id'),
      baseline: difference.baseline,
      observed: difference.observed,
    }
  })
  const observations = outcomes.flatMap((outcome) =>
    ROLES.map((role) => ({ role, matches: outcome.roles[role].matches })),
  )
  const controlsMatch = observations
    .filter((item) => item.role !== 'TREATMENT')
    .every((item) => item.matches)
  const treatmentMatches = observations
    .filter((item) => item.role === 'TREATMENT')
    .every((item) => item.matches)
  const createdTimes = ROLES.map((role) => Date.parse(sources[role].created_at))
  const orderedTimesValid =
    createdTimes.every(Number.isFinite) &&
    createdTimes.slice(1).every((value, index) => createdTimes[index]! < value)
  if (
    (status === 'SUPPORTED' && (!attributable || !controlsMatch || !treatmentMatches)) ||
    (status === 'CONTRADICTED' && (!attributable || !controlsMatch || treatmentMatches)) ||
    (status === 'INCONCLUSIVE' && attributable) ||
    (attributable &&
      (unplannedDifferences.length > 0 ||
        new Set(orderedBundles).size !== ROLES.length ||
        new Set(ROLES.map((role) => sources[role].run_id)).size !== ROLES.length ||
        new Set(ROLES.map((role) => sources[role].control_projection_sha256)).size !== 1 ||
        new Set(ROLES.map((role) => sources[role].random_seed)).size !== 1 ||
        !orderedTimesValid ||
        ROLES.some((role) => sources[role].execution_status !== 'COMPLETED')))
  ) {
    fail('PAIRING_STATE_CONFLICT', 'Analysis 状态绕过了四角色归因门禁。')
  }
  return {
    schema_version: '0.1',
    analysis_id: analysisId,
    analysis_type: 'FOUR_ROLE_PAIRED_COUNTERFACTUAL',
    rule_version: 'paired-counterfactual/0.1',
    analysis_status: status,
    attributable,
    pairing_plan: {
      id: pairingPlan.pairing_id,
      version: pairingPlan.version,
      sha256: pairingPlan.seal.digest,
    },
    sequence: [...ROLES],
    warmup: { mode: 'NONE', iterations: 0 },
    primary_variable: pairingPlan.primary_variable,
    reasons,
    sources,
    outcomes,
    unplanned_differences: unplannedDifferences,
    limits: parseStringList(analysis.limits, 'limits'),
  }
}

export async function loadPairedAnalysisFromBlobs(
  entries: ReadonlyMap<string, Blob>,
): Promise<LoadedPairedAnalysis> {
  if (entries.size !== MAX_FILES) {
    fail('PAIRING_FILE_SET_MISMATCH', 'PairedAnalysis 目录必须且只能包含四个冻结文件。')
  }
  let selectedBytes = 0
  for (const [path, blob] of entries) {
    normalizeBundlePath(path)
    if (blob.size > MAX_FILE_BYTES) fail('PAIRING_FILE_SIZE_LIMIT', 'PairedAnalysis 文件超过 10 MiB。')
    selectedBytes += blob.size
    if (selectedBytes > MAX_BUNDLE_BYTES) fail('PAIRING_BUNDLE_SIZE_LIMIT', 'PairedAnalysis 包超过 30 MiB。')
  }
  const manifestBlob = entries.get('paired-analysis-manifest.json')
  if (!manifestBlob) fail('PAIRING_ROOT_MISSING', 'PairedAnalysis 缺少 Manifest。')
  const manifest = parseManifest(await parseJson(manifestBlob, 'paired-analysis-manifest.json'))
  const allowed = new Set(['paired-analysis-manifest.json', ...manifest.files.map((file) => file.path)])
  if ([...entries.keys()].some((path) => !allowed.has(path))) {
    fail('PAIRING_FILE_SET_MISMATCH', 'PairedAnalysis 包含未声明文件。')
  }
  let verifiedBytes = 0
  for (const file of manifest.files) {
    const blob = entries.get(file.path)
    if (!blob) fail('PAIRING_REFERENCE_MISSING', 'Manifest 引用了缺失文件。')
    if (blob.size !== file.size) fail('PAIRING_SIZE_MISMATCH', '文件大小与 Manifest 不一致。')
    if ((await sha256Hex(blob)) !== file.sha256) {
      fail('PAIRING_HASH_MISMATCH', '文件 SHA-256 与 Manifest 不一致。')
    }
    verifiedBytes += blob.size
  }
  const pairingPlan = await parsePairingPlan(
    await parseJson(entries.get('sealed-pairing-plan.json')!, 'sealed-pairing-plan.json'),
  )
  const analysis = await parseAnalysis(
    await parseJson(entries.get('paired-analysis.json')!, 'paired-analysis.json'),
    manifest,
    pairingPlan,
  )
  return {
    analysis,
    pairingPlan,
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

export async function loadLocalPairedAnalysis(
  input: FileList | File[],
): Promise<LoadedPairedAnalysis> {
  const files = Array.from(input)
  if (files.length === 0) fail('PAIRING_EMPTY_SELECTION', '没有选择任何 PairedAnalysis 文件。')
  if (files.length > MAX_FILES) fail('PAIRING_FILE_SET_MISMATCH', 'PairedAnalysis 文件数量超过四个。')
  const paths = localPaths(files)
  if (new Set(paths).size !== paths.length) fail('PAIRING_DUPLICATE_PATH', 'PairedAnalysis 包含重复路径。')
  const entries = new Map<string, Blob>()
  files.forEach((file, index) => entries.set(paths[index]!, file))
  return loadPairedAnalysisFromBlobs(entries)
}

export async function loadPairedAnalysisReviewSample(): Promise<LoadedPairedAnalysis> {
  try {
    return await loadPairedAnalysisFromBlobs(
      await fetchSameOriginFixture(REVIEW_SAMPLE_BASE, REVIEW_SAMPLE_FILES),
    )
  } catch (cause) {
    if (cause instanceof PairingLoadError) throw cause
    if (cause instanceof SameOriginFixtureError) {
      fail('PAIRING_SAMPLE_FETCH_FAILED', cause.message)
    }
    fail('PAIRING_SAMPLE_FETCH_FAILED', '配对分析审阅夹具读取失败。')
  }
}
