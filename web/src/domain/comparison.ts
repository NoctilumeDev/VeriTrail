import { normalizeBundlePath, sha256Hex } from './bundle'
import { fetchSameOriginFixture, SameOriginFixtureError } from './sameOriginFixture'
import type {
  ComparisonDifference,
  ComparisonManifest,
  ComparisonSource,
  ComparisonSourceState,
  ComparisonStatus,
  ExecutionStatus,
  LoadedComparison,
  RerunComparison,
  Verdict,
} from './types'

const MAX_FILES = 3
const MAX_FILE_BYTES = 10 * 1024 * 1024
const MAX_BUNDLE_BYTES = 20 * 1024 * 1024
const SHA256 = /^[0-9a-f]{64}$/
const COMPARISON_ID = /^cmp_[0-9a-f]{24}$/
const EXECUTION_STATUSES = new Set<ExecutionStatus>([
  'PLANNED',
  'RUNNING',
  'COMPLETED',
  'ABORTED',
  'ERROR',
])
const VERDICTS = new Set<Verdict>(['PASS', 'FAIL', 'INCONCLUSIVE', 'PENDING'])
const COMPARISON_STATUSES = new Set<ComparisonStatus>(['MATCH', 'DRIFT', 'INCONCLUSIVE'])
const REVIEW_SAMPLE_BASE = '/fixtures/m6-comparison-drift'
const REVIEW_SAMPLE_FILES = [
  'comparison-manifest.json',
  'comparison.json',
  'comparison.md',
] as const

export class ComparisonLoadError extends Error {
  readonly code: string

  constructor(code: string, message: string) {
    super(message)
    this.name = 'ComparisonLoadError'
    this.code = code
  }
}

function fail(code: string, message: string): never {
  throw new ComparisonLoadError(code, message)
}

function record(value: unknown, name: string): Record<string, unknown> {
  if (typeof value !== 'object' || value === null || Array.isArray(value)) {
    fail('COMPARISON_INVALID', `${name} 必须是对象。`)
  }
  return value as Record<string, unknown>
}

function string(value: unknown, name: string, pattern?: RegExp): string {
  if (typeof value !== 'string' || !value || (pattern && !pattern.test(value))) {
    fail('COMPARISON_INVALID', `${name} 不符合 Comparison 0.1。`)
  }
  return value
}

function integer(value: unknown, name: string): number {
  if (!Number.isInteger(value)) fail('COMPARISON_INVALID', `${name} 必须是整数。`)
  return value as number
}

function array(value: unknown, name: string): unknown[] {
  if (!Array.isArray(value)) fail('COMPARISON_INVALID', `${name} 必须是数组。`)
  return value
}

function boolean(value: unknown, name: string): boolean {
  if (typeof value !== 'boolean') fail('COMPARISON_INVALID', `${name} 必须是布尔值。`)
  return value
}

async function parseJson(blob: Blob, name: string): Promise<unknown> {
  try {
    return JSON.parse(await blob.text()) as unknown
  } catch {
    fail('COMPARISON_INVALID_JSON', `${name} 不是有效 JSON。`)
  }
}

function parseManifest(value: unknown): ComparisonManifest {
  const manifest = record(value, 'comparison-manifest.json')
  if (manifest.schema_version !== '0.1') {
    fail('COMPARISON_VERSION_UNSUPPORTED', 'Comparison Manifest 版本不受支持。')
  }
  const files = array(manifest.files, 'manifest.files').map((value, index) => {
    const file = record(value, `manifest.files[${index}]`)
    const size = integer(file.size, `manifest.files[${index}].size`)
    if (size < 0 || size > MAX_FILE_BYTES) {
      fail('COMPARISON_FILE_SIZE_LIMIT', 'Comparison 文件超过 10 MiB 上限。')
    }
    return {
      path: normalizeBundlePath(string(file.path, `manifest.files[${index}].path`)),
      sha256: string(file.sha256, `manifest.files[${index}].sha256`, SHA256),
      size,
    }
  })
  const paths = files.map((file) => file.path)
  if (
    files.length !== 2 ||
    new Set(paths).size !== 2 ||
    !paths.includes('comparison.json') ||
    !paths.includes('comparison.md')
  ) {
    fail('COMPARISON_FILE_SET_MISMATCH', 'Comparison Manifest 必须且只能声明 JSON 与 Markdown。')
  }
  return {
    schema_version: '0.1',
    comparison_id: string(manifest.comparison_id, 'manifest.comparison_id', COMPARISON_ID),
    files,
  }
}

function parseSourceState(value: unknown): ComparisonSourceState {
  const state = record(value, 'source.source_state')
  const qualification = string(state.qualification, 'source.source_state.qualification')
  if (qualification === 'NOT_APPLICABLE' || qualification === 'UNAVAILABLE') {
    return { qualification }
  }
  if (qualification !== 'APPROVED' && qualification !== 'OBSERVED_ONLY') {
    fail('COMPARISON_INVALID', 'Source state qualification 不受支持。')
  }
  if (state.policy_version !== 'subject-tree-sha256/0.1') {
    fail('COMPARISON_INVALID', 'Source snapshot policy 不受支持。')
  }
  const watchRoots = array(state.watch_roots, 'source.source_state.watch_roots').map(
    (item, index) => string(item, `source.source_state.watch_roots[${index}]`),
  )
  if (watchRoots.length === 0 || new Set(watchRoots).size !== watchRoots.length) {
    fail('COMPARISON_INVALID', 'Source snapshot watch roots 无效。')
  }
  return {
    qualification,
    policy_version: 'subject-tree-sha256/0.1',
    watch_roots: watchRoots,
    fingerprint: string(state.fingerprint, 'source.source_state.fingerprint', SHA256),
  }
}

function parseSource(
  value: unknown,
  role: 'BASELINE' | 'REPEAT',
  schemaVersion: '0.1' | '0.2',
): ComparisonSource {
  const source = record(value, `sources.${role.toLowerCase()}`)
  const plan = record(source.plan, 'source.plan')
  const executionStatus = string(source.execution_status, 'source.execution_status') as ExecutionStatus
  const verdict = string(source.verdict, 'source.verdict') as Verdict
  if (!EXECUTION_STATUSES.has(executionStatus) || !VERDICTS.has(verdict)) {
    fail('COMPARISON_INVALID', '来源 Run 的状态或裁决不受支持。')
  }
  if (source.role !== role) fail('COMPARISON_REFERENCE_MISMATCH', 'Comparison 来源角色错位。')
  const parsed: ComparisonSource = {
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
    bundle_sha256: string(source.bundle_sha256, 'source.bundle_sha256', SHA256),
    semantic_sha256: string(source.semantic_sha256, 'source.semantic_sha256', SHA256),
  }
  if (typeof source.project_profile_sha256 === 'string') {
    parsed.project_profile_sha256 = string(
      source.project_profile_sha256,
      'source.project_profile_sha256',
      SHA256,
    )
  }
  if (schemaVersion === '0.2') parsed.source_state = parseSourceState(source.source_state)
  return parsed
}

function parseDifference(value: unknown, index: number): ComparisonDifference {
  const difference = record(value, `differences[${index}]`)
  const path = string(difference.path, `differences[${index}].path`)
  if (!path.startsWith('/')) fail('COMPARISON_INVALID', 'Difference 必须使用 JSON Pointer 路径。')
  return {
    path,
    baseline_present: boolean(difference.baseline_present, 'difference.baseline_present'),
    repeat_present: boolean(difference.repeat_present, 'difference.repeat_present'),
    baseline: difference.baseline,
    repeat: difference.repeat,
  }
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

async function validateComparison(value: unknown, manifest: ComparisonManifest): Promise<RerunComparison> {
  const comparison = record(value, 'comparison.json')
  if (
    !['0.1', '0.2'].includes(String(comparison.schema_version)) ||
    comparison.comparison_type !== 'SAME_PLAN_RERUN'
  ) {
    fail('COMPARISON_VERSION_UNSUPPORTED', 'Comparison 类型或版本不受支持。')
  }
  const schemaVersion = comparison.schema_version as '0.1' | '0.2'
  const expectedRule = schemaVersion === '0.2' ? 'rerun-semantic/0.2' : 'rerun-semantic/0.1'
  if (comparison.rule_version !== expectedRule) {
    fail('COMPARISON_RULE_UNSUPPORTED', 'Comparison 规则版本不受支持。')
  }
  const comparisonId = string(comparison.comparison_id, 'comparison_id', COMPARISON_ID)
  if (comparisonId !== manifest.comparison_id) {
    fail('COMPARISON_REFERENCE_MISMATCH', 'Comparison ID 与 Manifest 不一致。')
  }
  const status = string(comparison.comparison_status, 'comparison_status') as ComparisonStatus
  if (!COMPARISON_STATUSES.has(status)) fail('COMPARISON_INVALID', 'Comparison 状态不受支持。')
  const comparable = boolean(comparison.comparable, 'comparable')
  const sources = record(comparison.sources, 'sources')
  const baseline = parseSource(sources.baseline, 'BASELINE', schemaVersion)
  const repeat = parseSource(sources.repeat, 'REPEAT', schemaVersion)
  const expectedId = `cmp_${(
    await sha256Hex(
      new Blob([
        canonicalJson({
          schema_version: schemaVersion,
          rule_version: expectedRule,
          baseline_bundle_sha256: baseline.bundle_sha256,
          repeat_bundle_sha256: repeat.bundle_sha256,
        }),
      ]),
    )
  ).slice(0, 24)}`
  if (comparisonId !== expectedId) {
    fail('COMPARISON_REFERENCE_MISMATCH', 'Comparison ID 不能由来源 Bundle 摘要重建。')
  }
  const reasons = array(comparison.reasons, 'reasons').map((value, index) => {
    const reason = record(value, `reasons[${index}]`)
    return {
      code: string(reason.code, `reasons[${index}].code`),
      message: string(reason.message, `reasons[${index}].message`),
    }
  })
  if (reasons.length === 0) fail('COMPARISON_INVALID', 'Comparison 至少需要一个稳定原因。')
  const differences = array(comparison.differences, 'differences').map(parseDifference)
  const limits = array(comparison.limits, 'limits').map((value, index) =>
    string(value, `limits[${index}]`),
  )
  if (limits.length === 0) fail('COMPARISON_INVALID', 'Comparison 必须声明适用边界。')
  if (
    (status === 'MATCH' && (!comparable || differences.length !== 0)) ||
    (status === 'DRIFT' && (!comparable || differences.length === 0)) ||
    (status === 'INCONCLUSIVE' && comparable)
  ) {
    fail('COMPARISON_STATE_CONFLICT', 'Comparison 状态、可比较性与差异数量互相冲突。')
  }
  if (
    comparable &&
    (baseline.run_id === repeat.run_id ||
      baseline.plan.sha256 !== repeat.plan.sha256 ||
      baseline.random_seed !== repeat.random_seed ||
      baseline.execution_status !== 'COMPLETED' ||
      repeat.execution_status !== 'COMPLETED')
  ) {
    fail('COMPARISON_STATE_CONFLICT', '可比较标记绕过了同 Plan 独立完整 Run 门禁。')
  }
  if (schemaVersion === '0.2') {
    const baselineState = baseline.source_state!
    const repeatState = repeat.source_state!
    const statesComparable =
      (baselineState.qualification === 'NOT_APPLICABLE' &&
        repeatState.qualification === 'NOT_APPLICABLE') ||
      (baselineState.qualification === 'APPROVED' &&
        repeatState.qualification === 'APPROVED' &&
        canonicalJson(baselineState) === canonicalJson(repeatState))
    if ((comparable && !statesComparable) || (!statesComparable && differences.length !== 0)) {
      fail('COMPARISON_STATE_CONFLICT', '可比较标记绕过了获批源码状态门禁。')
    }
  }
  return {
    schema_version: schemaVersion,
    comparison_id: comparisonId,
    comparison_type: 'SAME_PLAN_RERUN',
    rule_version: expectedRule,
    comparison_status: status,
    comparable,
    reasons,
    sources: { baseline, repeat },
    differences,
    limits,
  }
}

export async function loadComparisonFromBlobs(
  entries: ReadonlyMap<string, Blob>,
): Promise<LoadedComparison> {
  if (entries.size !== MAX_FILES) {
    fail('COMPARISON_FILE_SET_MISMATCH', 'Comparison 目录必须且只能包含三个冻结文件。')
  }
  let selectedBytes = 0
  for (const [path, blob] of entries) {
    normalizeBundlePath(path)
    if (blob.size > MAX_FILE_BYTES) fail('COMPARISON_FILE_SIZE_LIMIT', 'Comparison 文件超过 10 MiB。')
    selectedBytes += blob.size
    if (selectedBytes > MAX_BUNDLE_BYTES) fail('COMPARISON_BUNDLE_SIZE_LIMIT', 'Comparison 包超过 20 MiB。')
  }
  const manifestBlob = entries.get('comparison-manifest.json')
  if (!manifestBlob) fail('COMPARISON_ROOT_MISSING', 'Comparison 缺少 Manifest。')
  const manifest = parseManifest(await parseJson(manifestBlob, 'comparison-manifest.json'))
  const allowed = new Set(['comparison-manifest.json', ...manifest.files.map((file) => file.path)])
  if ([...entries.keys()].some((path) => !allowed.has(path))) {
    fail('COMPARISON_FILE_SET_MISMATCH', 'Comparison 包含未声明文件。')
  }
  let verifiedBytes = 0
  for (const file of manifest.files) {
    const blob = entries.get(file.path)
    if (!blob) fail('COMPARISON_REFERENCE_MISSING', 'Comparison Manifest 引用了缺失文件。')
    if (blob.size !== file.size) fail('COMPARISON_SIZE_MISMATCH', 'Comparison 文件大小与 Manifest 不一致。')
    if ((await sha256Hex(blob)) !== file.sha256) {
      fail('COMPARISON_HASH_MISMATCH', 'Comparison 文件 SHA-256 与 Manifest 不一致。')
    }
    verifiedBytes += blob.size
  }
  const comparison = await validateComparison(
    await parseJson(entries.get('comparison.json')!, 'comparison.json'),
    manifest,
  )
  return {
    comparison,
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

export async function loadLocalComparison(input: FileList | File[]): Promise<LoadedComparison> {
  const files = Array.from(input)
  if (files.length === 0) fail('COMPARISON_EMPTY_SELECTION', '没有选择任何 Comparison 文件。')
  if (files.length > MAX_FILES) fail('COMPARISON_FILE_SET_MISMATCH', 'Comparison 文件数量超过三个。')
  const paths = localPaths(files)
  if (new Set(paths).size !== paths.length) fail('COMPARISON_DUPLICATE_PATH', 'Comparison 包含重复路径。')
  const entries = new Map<string, Blob>()
  files.forEach((file, index) => entries.set(paths[index]!, file))
  return loadComparisonFromBlobs(entries)
}

export async function loadComparisonReviewSample(): Promise<LoadedComparison> {
  try {
    return await loadComparisonFromBlobs(
      await fetchSameOriginFixture(REVIEW_SAMPLE_BASE, REVIEW_SAMPLE_FILES),
    )
  } catch (cause) {
    if (cause instanceof ComparisonLoadError) throw cause
    if (cause instanceof SameOriginFixtureError) {
      fail('COMPARISON_SAMPLE_FETCH_FAILED', cause.message)
    }
    fail('COMPARISON_SAMPLE_FETCH_FAILED', '复跑比较审阅夹具读取失败。')
  }
}
