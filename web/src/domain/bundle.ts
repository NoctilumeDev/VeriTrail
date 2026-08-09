import type {
  BundleFileEntry,
  BundleManifest,
  EvidenceArtifact,
  EvidenceDocument,
  EvidenceManifest,
  ExecutionStatus,
  LoadedBundle,
  Verdict,
  VerdictReport,
} from './types'

const MAX_FILES = 256
const MAX_FILE_BYTES = 10 * 1024 * 1024
const MAX_BUNDLE_BYTES = 64 * 1024 * 1024
const SHA256_PATTERN = /^[0-9a-f]{64}$/
const EXECUTION_STATUSES = new Set<ExecutionStatus>([
  'PLANNED',
  'RUNNING',
  'COMPLETED',
  'ABORTED',
  'ERROR',
])
const VERDICTS = new Set<Verdict>(['PASS', 'FAIL', 'INCONCLUSIVE', 'PENDING'])
const SAFE_IMAGE_TYPES = new Set(['image/png', 'image/jpeg'])
const API_ERROR_MESSAGES: Record<string, string> = {
  RUN_NOT_FOUND: 'Catalog Run 不存在。',
  BUNDLE_FILE_NOT_FOUND: 'Bundle 文件未在清单中声明。',
  BUNDLE_UNAVAILABLE: '源 Bundle 当前不可用。',
  BUNDLE_CHANGED: '源 Bundle 已在索引后发生变化。',
  UNSAFE_PATH: 'Bundle 路径不安全。',
}

export type DemoBundleId = 'positive' | 'negative' | 'invalid'

export const DEMO_BUNDLE_BASES: Record<DemoBundleId, string> = {
  positive: '/fixtures/m2-positive/',
  negative: '/fixtures/m2-negative/',
  invalid: '/fixtures/m2-invalid/',
}

export class BundleLoadError extends Error {
  readonly code: string

  constructor(code: string, message: string) {
    super(message)
    this.name = 'BundleLoadError'
    this.code = code
  }
}

function fail(code: string, message: string): never {
  throw new BundleLoadError(code, message)
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === 'object' && value !== null && !Array.isArray(value)
}

function requireRecord(value: unknown, name: string): Record<string, unknown> {
  if (!isRecord(value)) fail('INVALID_STRUCTURE', `${name} 必须是对象。`)
  return value
}

function requireString(value: unknown, name: string): string {
  if (typeof value !== 'string' || value.length === 0) {
    fail('INVALID_STRUCTURE', `${name} 必须是非空字符串。`)
  }
  return value
}

function requireNumber(value: unknown, name: string): number {
  if (typeof value !== 'number' || !Number.isFinite(value) || value < 0) {
    fail('INVALID_STRUCTURE', `${name} 必须是非负有限数值。`)
  }
  return value
}

function requireArray(value: unknown, name: string): unknown[] {
  if (!Array.isArray(value)) fail('INVALID_STRUCTURE', `${name} 必须是数组。`)
  return value
}

function requireVersion(value: unknown, name: string): '0.1' {
  if (value !== '0.1') fail('UNSUPPORTED_VERSION', `${name} 版本不受支持。`)
  return '0.1'
}

function requireSha256(value: unknown, name: string): string {
  const digest = requireString(value, name)
  if (!SHA256_PATTERN.test(digest)) fail('INVALID_STRUCTURE', `${name} 不是有效 SHA-256。`)
  return digest
}

export function normalizeBundlePath(path: string): string {
  if (
    !path ||
    path.includes('\\') ||
    path.includes('\0') ||
    path.startsWith('/') ||
    /^[a-zA-Z]:/.test(path)
  ) {
    fail('UNSAFE_PATH', '证据包包含不安全路径。')
  }
  const parts = path.split('/')
  if (parts.some((part) => part === '' || part === '.' || part === '..')) {
    fail('UNSAFE_PATH', '证据包包含不安全路径。')
  }
  return parts.join('/')
}

function parseJson(blob: Blob, name: string): Promise<unknown> {
  return blob
    .text()
    .then((text) => JSON.parse(text) as unknown)
    .catch(() => fail('INVALID_JSON', `${name} 不是有效 JSON。`))
}

export async function sha256Hex(blob: Blob): Promise<string> {
  const digest = await globalThis.crypto.subtle.digest('SHA-256', await blob.arrayBuffer())
  return Array.from(new Uint8Array(digest), (byte) => byte.toString(16).padStart(2, '0')).join('')
}

function validateBundleFile(value: unknown, index: number): BundleFileEntry {
  const entry = requireRecord(value, `bundle.files[${index}]`)
  return {
    path: normalizeBundlePath(requireString(entry.path, `bundle.files[${index}].path`)),
    sha256: requireSha256(entry.sha256, `bundle.files[${index}].sha256`),
    size: requireNumber(entry.size, `bundle.files[${index}].size`),
  }
}

function validateBundleManifest(value: unknown): BundleManifest {
  const document = requireRecord(value, 'bundle-manifest.json')
  const files = requireArray(document.files, 'bundle.files').map(validateBundleFile)
  if (files.length + 1 > MAX_FILES) fail('FILE_LIMIT', '证据包文件数量超过 256 个。')
  const paths = files.map((entry) => entry.path)
  if (new Set(paths).size !== paths.length) fail('DUPLICATE_PATH', '证据包清单包含重复路径。')
  if (!paths.includes('report.json') || !paths.includes('evidence-manifest.json')) {
    fail('MISSING_ROOT_FILE', '证据包缺少报告或 Evidence 清单。')
  }
  return {
    schema_version: requireVersion(document.schema_version, 'Bundle Manifest'),
    run_id: requireString(document.run_id, 'bundle.run_id'),
    files,
  }
}

function validateAttachment(value: unknown, name: string) {
  const attachment = requireRecord(value, name)
  const mediaType = requireString(attachment.media_type, `${name}.media_type`)
  if (!SAFE_IMAGE_TYPES.has(mediaType)) {
    fail('UNSAFE_ATTACHMENT', 'M3 只允许展示清单内的 PNG/JPEG 附件。')
  }
  return {
    logical_name: requireString(attachment.logical_name, `${name}.logical_name`),
    media_type: mediaType,
    path: normalizeBundlePath(requireString(attachment.path, `${name}.path`)),
    sha256: requireSha256(attachment.sha256, `${name}.sha256`),
    size: requireNumber(attachment.size, `${name}.size`),
  }
}

function validateArtifact(value: unknown, index: number): EvidenceArtifact {
  const artifact = requireRecord(value, `artifacts[${index}]`)
  return {
    evidence_type: requireString(artifact.evidence_type, `artifacts[${index}].evidence_type`),
    path: normalizeBundlePath(requireString(artifact.path, `artifacts[${index}].path`)),
    sha256: requireSha256(artifact.sha256, `artifacts[${index}].sha256`),
    size: requireNumber(artifact.size, `artifacts[${index}].size`),
    redacted: artifact.redacted === true,
    redacted_fields: requireNumber(artifact.redacted_fields, `artifacts[${index}].redacted_fields`),
    redaction_rule_version: requireString(
      artifact.redaction_rule_version,
      `artifacts[${index}].redaction_rule_version`,
    ),
    parser_version: requireString(artifact.parser_version, `artifacts[${index}].parser_version`),
    captured_at: requireString(artifact.captured_at, `artifacts[${index}].captured_at`),
    source: requireString(artifact.source, `artifacts[${index}].source`),
    source_name: requireString(artifact.source_name, `artifacts[${index}].source_name`),
    retention: requireString(artifact.retention, `artifacts[${index}].retention`),
    attachments: requireArray(artifact.attachments, `artifacts[${index}].attachments`).map(
      (attachment, attachmentIndex) =>
        validateAttachment(attachment, `artifacts[${index}].attachments[${attachmentIndex}]`),
    ),
    ...(isRecord(artifact.summary) ? { summary: artifact.summary } : {}),
  }
}

function validateEvidenceManifest(value: unknown): EvidenceManifest {
  const document = requireRecord(value, 'evidence-manifest.json')
  return {
    schema_version: requireVersion(document.schema_version, 'Evidence Manifest'),
    run_id: requireString(document.run_id, 'evidence-manifest.run_id'),
    artifacts: requireArray(document.artifacts, 'evidence-manifest.artifacts').map(validateArtifact),
    duplicate_inputs_ignored: requireArray(
      document.duplicate_inputs_ignored,
      'evidence-manifest.duplicate_inputs_ignored',
    ).map((value, index) => requireString(value, `duplicate_inputs_ignored[${index}]`)),
  }
}

function validateReport(value: unknown): VerdictReport {
  const report = requireRecord(value, 'report.json')
  const plan = requireRecord(report.plan, 'report.plan')
  const executionStatus = requireString(report.execution_status, 'report.execution_status')
  const verdict = requireString(report.verdict, 'report.verdict')
  if (!EXECUTION_STATUSES.has(executionStatus as ExecutionStatus)) {
    fail('INVALID_STATUS', '报告包含未知 ExecutionStatus。')
  }
  if (!VERDICTS.has(verdict as Verdict)) fail('INVALID_VERDICT', '报告包含未知 Verdict。')

  const reasons = requireArray(report.reasons, 'report.reasons').map((value, index) => {
    const reason = requireRecord(value, `report.reasons[${index}]`)
    return {
      code: requireString(reason.code, `report.reasons[${index}].code`),
      message: requireString(reason.message, `report.reasons[${index}].message`),
    }
  })
  if (reasons.length === 0) fail('INVALID_STRUCTURE', '报告必须包含至少一个裁决原因。')

  const assertions = requireArray(report.assertions, 'report.assertions').map((value, index) => {
    const assertion = requireRecord(value, `report.assertions[${index}]`)
    return {
      ...assertion,
      id: requireString(assertion.id, `report.assertions[${index}].id`),
      severity: requireString(assertion.severity, `report.assertions[${index}].severity`),
      status: requireString(assertion.status, `report.assertions[${index}].status`),
      expected: assertion.expected,
      actual: assertion.actual,
    }
  })

  return {
    ...report,
    schema_version: requireVersion(report.schema_version, 'Report'),
    run_id: requireString(report.run_id, 'report.run_id'),
    created_at: requireString(report.created_at, 'report.created_at'),
    plan: {
      id: requireString(plan.id, 'report.plan.id'),
      version: requireNumber(plan.version, 'report.plan.version'),
      sha256: requireSha256(plan.sha256, 'report.plan.sha256'),
    },
    execution_status: executionStatus as ExecutionStatus,
    verdict: verdict as Verdict,
    reasons,
    evidence: requireArray(report.evidence, 'report.evidence').map(validateArtifact),
    assertions,
    missing_evidence: requireArray(report.missing_evidence, 'report.missing_evidence').map(
      (item, index) => requireString(item, `report.missing_evidence[${index}]`),
    ),
    contamination: requireArray(report.contamination, 'report.contamination').map((item, index) =>
      requireRecord(item, `report.contamination[${index}]`),
    ),
    reproduction_steps: Array.isArray(report.reproduction_steps)
      ? report.reproduction_steps.map((item, index) =>
          requireString(item, `report.reproduction_steps[${index}]`),
        )
      : [],
    cleanup_steps: Array.isArray(report.cleanup_steps)
      ? report.cleanup_steps.map((item, index) =>
          requireString(item, `report.cleanup_steps[${index}]`),
        )
      : [],
  } as VerdictReport
}

function validateEvidenceDocument(value: unknown, artifact: EvidenceArtifact): EvidenceDocument {
  const document = requireRecord(value, artifact.path)
  const evidenceType = requireString(document.evidence_type, `${artifact.path}.evidence_type`)
  if (evidenceType !== artifact.evidence_type) {
    fail('REFERENCE_MISMATCH', 'Evidence 类型与清单不一致。')
  }
  return {
    schema_version: requireVersion(document.schema_version, 'Evidence'),
    evidence_type: evidenceType,
    source: requireString(document.source, `${artifact.path}.source`),
    captured_at: requireString(document.captured_at, `${artifact.path}.captured_at`),
    facts: requireRecord(document.facts, `${artifact.path}.facts`),
    ...(isRecord(document.observed_variables)
      ? { observed_variables: document.observed_variables }
      : {}),
    ...(isRecord(document.metadata) ? { metadata: document.metadata } : {}),
  }
}

function assertEntryLimits(entries: ReadonlyMap<string, Blob>) {
  if (entries.size > MAX_FILES) fail('FILE_LIMIT', '证据包文件数量超过 256 个。')
  let totalBytes = 0
  for (const blob of entries.values()) {
    if (blob.size > MAX_FILE_BYTES) fail('FILE_SIZE_LIMIT', '证据包包含超过 10 MiB 的文件。')
    totalBytes += blob.size
    if (totalBytes > MAX_BUNDLE_BYTES) fail('BUNDLE_SIZE_LIMIT', '证据包总大小超过 64 MiB。')
  }
}

function sameArtifact(left: EvidenceArtifact, right: EvidenceArtifact): boolean {
  return (
    left.evidence_type === right.evidence_type &&
    left.path === right.path &&
    left.sha256 === right.sha256 &&
    left.size === right.size
  )
}

export async function loadBundleFromBlobs(
  entries: ReadonlyMap<string, Blob>,
  sourceLabel: string,
): Promise<LoadedBundle> {
  assertEntryLimits(entries)
  const manifestBlob = entries.get('bundle-manifest.json')
  if (!manifestBlob) fail('MISSING_ROOT_FILE', '证据包缺少 bundle-manifest.json。')
  const bundleManifest = validateBundleManifest(await parseJson(manifestBlob, 'bundle-manifest.json'))
  const declaredPaths = new Set(bundleManifest.files.map((entry) => entry.path))
  const allowedPaths = new Set([...declaredPaths, 'bundle-manifest.json'])
  for (const path of entries.keys()) {
    normalizeBundlePath(path)
    if (!allowedPaths.has(path)) fail('UNDECLARED_FILE', '证据包包含未进入 Bundle 清单的文件。')
  }

  let totalBytes = 0
  const bundleByPath = new Map<string, BundleFileEntry>()
  for (const file of bundleManifest.files) {
    const blob = entries.get(file.path)
    if (!blob) fail('MISSING_REFERENCE', 'Bundle 清单引用了缺失文件。')
    if (blob.size !== file.size) fail('SIZE_MISMATCH', '文件大小与 Bundle 清单不一致。')
    if ((await sha256Hex(blob)) !== file.sha256) {
      fail('HASH_MISMATCH', '文件 SHA-256 与 Bundle 清单不一致。')
    }
    totalBytes += blob.size
    bundleByPath.set(file.path, file)
  }

  const report = validateReport(await parseJson(entries.get('report.json')!, 'report.json'))
  const evidenceManifest = validateEvidenceManifest(
    await parseJson(entries.get('evidence-manifest.json')!, 'evidence-manifest.json'),
  )
  if (
    report.run_id !== bundleManifest.run_id ||
    evidenceManifest.run_id !== bundleManifest.run_id
  ) {
    fail('RUN_ID_MISMATCH', 'Report、Evidence Manifest 与 Bundle Manifest 的 Run ID 不一致。')
  }
  if (
    report.evidence.length !== evidenceManifest.artifacts.length ||
    !report.evidence.every((artifact, index) =>
      sameArtifact(artifact, evidenceManifest.artifacts[index]!),
    )
  ) {
    fail('REFERENCE_MISMATCH', 'Report 与 Evidence Manifest 的证据索引不一致。')
  }

  const evidenceByPath: Record<string, EvidenceDocument> = {}
  const imageUrls: Record<string, string> = {}
  const createdUrls: string[] = []
  try {
    for (const artifact of evidenceManifest.artifacts) {
      const manifestEntry = bundleByPath.get(artifact.path)
      if (
        !manifestEntry ||
        manifestEntry.sha256 !== artifact.sha256 ||
        manifestEntry.size !== artifact.size
      ) {
        fail('REFERENCE_MISMATCH', 'Evidence 文件与清单索引不一致。')
      }
      evidenceByPath[artifact.path] = validateEvidenceDocument(
        await parseJson(entries.get(artifact.path)!, artifact.path),
        artifact,
      )
      for (const attachment of artifact.attachments) {
        const attachmentEntry = bundleByPath.get(attachment.path)
        const attachmentBlob = entries.get(attachment.path)
        if (
          !attachmentEntry ||
          !attachmentBlob ||
          attachmentEntry.sha256 !== attachment.sha256 ||
          attachmentEntry.size !== attachment.size
        ) {
          fail('REFERENCE_MISMATCH', '附件与清单索引不一致。')
        }
        const objectUrl = URL.createObjectURL(
          new Blob([attachmentBlob], { type: attachment.media_type }),
        )
        imageUrls[attachment.path] = objectUrl
        createdUrls.push(objectUrl)
      }
    }
  } catch (error) {
    for (const url of createdUrls) URL.revokeObjectURL(url)
    throw error
  }

  let released = false
  return {
    sourceLabel,
    report,
    bundleManifest,
    evidenceManifest,
    evidenceByPath,
    imageUrls,
    integrity: {
      verified: true,
      verifiedFiles: bundleManifest.files.length,
      totalBytes,
    },
    release: () => {
      if (released) return
      released = true
      for (const url of createdUrls) URL.revokeObjectURL(url)
    },
  }
}

function safeSameOriginUrl(basePath: string, relativePath: string): URL {
  const base = new URL(basePath, window.location.href)
  if (base.origin !== window.location.origin) fail('REMOTE_URL', '演示包必须来自同源地址。')
  const normalized = normalizeBundlePath(relativePath)
  const target = new URL(normalized, base)
  if (target.origin !== base.origin || !target.pathname.startsWith(base.pathname)) {
    fail('REMOTE_URL', '演示包路径越过允许的同源目录。')
  }
  return target
}

async function fetchBlob(url: URL, label: string): Promise<Blob> {
  let response: Response
  try {
    response = await fetch(url, {
      credentials: 'same-origin',
      cache: 'no-store',
      headers: { Accept: 'application/json, image/png, image/jpeg, text/plain' },
    })
  } catch {
    fail('FETCH_FAILED', `${label} 读取失败。`)
  }
  if (!response.ok) {
    try {
      const payload = JSON.parse(await response.blob().then((blob) => blob.text())) as unknown
      if (isRecord(payload) && isRecord(payload.error) && typeof payload.error.code === 'string') {
        const message = API_ERROR_MESSAGES[payload.error.code]
        if (message) fail(payload.error.code, message)
      }
    } catch (cause) {
      if (cause instanceof BundleLoadError) throw cause
    }
    fail('FETCH_FAILED', `${label} 读取失败。`)
  }
  return response.blob()
}

export async function loadDemoBundle(id: DemoBundleId): Promise<LoadedBundle> {
  const base = DEMO_BUNDLE_BASES[id]
  return loadSameOriginBundle(base, `内置脱敏夹具 · ${id}`)
}

export async function loadSameOriginBundle(
  base: string,
  sourceLabel: string,
): Promise<LoadedBundle> {
  const entries = new Map<string, Blob>()
  const manifestUrl = safeSameOriginUrl(base, 'bundle-manifest.json')
  const manifestBlob = await fetchBlob(manifestUrl, 'Bundle Manifest')
  entries.set('bundle-manifest.json', manifestBlob)
  const manifest = validateBundleManifest(await parseJson(manifestBlob, 'bundle-manifest.json'))
  for (const file of manifest.files) {
    entries.set(file.path, await fetchBlob(safeSameOriginUrl(base, file.path), file.path))
  }
  return loadBundleFromBlobs(entries, sourceLabel)
}

function localRelativePaths(files: File[]): string[] {
  const rawPaths = files.map(
    (file) => (file as File & { webkitRelativePath?: string }).webkitRelativePath || file.name,
  )
  const parts = rawPaths.map((path) => path.split('/'))
  const stripRoot =
    parts.every((segments) => segments.length > 1) &&
    new Set(parts.map((segments) => segments[0])).size === 1
  return parts.map((segments) => normalizeBundlePath((stripRoot ? segments.slice(1) : segments).join('/')))
}

export async function loadLocalBundle(input: FileList | File[]): Promise<LoadedBundle> {
  const files = Array.from(input)
  if (files.length === 0) fail('EMPTY_SELECTION', '没有选择任何证据文件。')
  if (files.length > MAX_FILES) fail('FILE_LIMIT', '证据包文件数量超过 256 个。')
  const paths = localRelativePaths(files)
  if (new Set(paths).size !== paths.length) fail('DUPLICATE_PATH', '本地证据包包含重复规范路径。')
  const entries = new Map<string, Blob>()
  files.forEach((file, index) => entries.set(paths[index]!, file))
  return loadBundleFromBlobs(entries, '本地目录 · 仅内存读取')
}

export function browserEvidence(bundle: LoadedBundle): EvidenceDocument | null {
  const artifact = bundle.evidenceManifest.artifacts.find(
    (candidate) => candidate.evidence_type === 'browser.session',
  )
  return artifact ? bundle.evidenceByPath[artifact.path] ?? null : null
}
