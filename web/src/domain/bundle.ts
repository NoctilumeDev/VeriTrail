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
import { ImageGeometryError, validateImageGeometry } from './image-geometry'

const MAX_FILES = 256
const MAX_FILE_BYTES = 10 * 1024 * 1024
const MAX_BUNDLE_BYTES = 64 * 1024 * 1024
// Account for the decoded RGBA surface plus one renderer/compositor copy. This
// is an aggregate budget across unique attachment paths, not a per-file limit.
export const MAX_BUNDLE_IMAGE_WORKING_SET_BYTES = 128 * 1024 * 1024
const IMAGE_RENDER_SURFACE_MULTIPLIER = 2
const SHA256_PATTERN = /^[0-9a-f]{64}$/
const EXECUTION_STATUSES = new Set<ExecutionStatus>([
  'PLANNED',
  'RUNNING',
  'COMPLETED',
  'ABORTED',
  'ERROR',
])
const VERDICTS = new Set<Verdict>(['PASS', 'FAIL', 'INCONCLUSIVE', 'PENDING'])
const SAFE_ATTACHMENT_TYPES = new Set([
  'image/png',
  'image/jpeg',
  'text/plain; charset=utf-8',
])
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
  if (
    !paths.includes('report.json') ||
    !paths.includes('evidence-manifest.json') ||
    !paths.includes('sealed-plan.json')
  ) {
    fail('MISSING_ROOT_FILE', '证据包缺少报告、Evidence 清单或 Sealed Plan。')
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
  if (!SAFE_ATTACHMENT_TYPES.has(mediaType)) {
    fail('UNSAFE_ATTACHMENT', '只允许读取清单内的 PNG、JPEG 或 UTF-8 文本附件。')
  }
  const path = normalizeBundlePath(requireString(attachment.path, `${name}.path`))
  const lowerPath = path.toLowerCase()
  const suffixMatches =
    (mediaType === 'image/png' && lowerPath.endsWith('.png')) ||
    (mediaType === 'image/jpeg' &&
      (lowerPath.endsWith('.jpg') || lowerPath.endsWith('.jpeg'))) ||
    (mediaType === 'text/plain; charset=utf-8' && lowerPath.endsWith('.txt'))
  if (!suffixMatches) fail('UNSAFE_ATTACHMENT', '附件类型与固定扩展名不一致。')
  return {
    logical_name: requireString(attachment.logical_name, `${name}.logical_name`),
    media_type: mediaType,
    path,
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
  const facts = requireRecord(document.facts, `${artifact.path}.facts`)
  if (evidenceType === 'browser.session') validateBrowserEvidenceBounds(facts, artifact.path)
  return {
    schema_version: requireVersion(document.schema_version, 'Evidence'),
    evidence_type: evidenceType,
    source: requireString(document.source, `${artifact.path}.source`),
    captured_at: requireString(document.captured_at, `${artifact.path}.captured_at`),
    facts,
    ...(isRecord(document.observed_variables)
      ? { observed_variables: document.observed_variables }
      : {}),
    ...(isRecord(document.metadata) ? { metadata: document.metadata } : {}),
  }
}

const BROWSER_ARRAY_LIMITS: Record<string, number> = {
  viewport_runs: 8,
  steps: 520,
  console: 500,
  page_errors: 100,
  network: 1000,
  screenshots: 512,
}

function validateBrowserEvidenceBounds(facts: Record<string, unknown>, path: string) {
  for (const [field, limit] of Object.entries(BROWSER_ARRAY_LIMITS)) {
    const values = requireArray(facts[field], `${path}.facts.${field}`)
    if (values.length > limit) {
      fail('EVIDENCE_LIMIT', `browser.session 的 ${field} 超过冻结上限。`)
    }
    values.forEach((value, index) => requireRecord(value, `${path}.facts.${field}[${index}]`))
  }
  const derivedCounts: Record<string, string> = {
    viewport_count: 'viewport_runs',
    screenshot_count: 'screenshots',
  }
  for (const [countField, arrayField] of Object.entries(derivedCounts)) {
    if (requireNumber(facts[countField], `${path}.facts.${countField}`) !== (facts[arrayField] as unknown[]).length) {
      fail('REFERENCE_MISMATCH', `browser.session 的 ${countField} 与事实数组不一致。`)
    }
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

async function validateSealedPlan(blob: Blob, report: VerdictReport) {
  const plan = requireRecord(await parseJson(blob, 'sealed-plan.json'), 'sealed-plan.json')
  const seal = requireRecord(plan.seal, 'sealed-plan.json.seal')
  if (seal.algorithm !== 'sha256') fail('INVALID_AUTHORITY', 'Sealed Plan 使用了未知摘要算法。')
  const digest = requireSha256(seal.digest, 'sealed-plan.json.seal.digest')
  const unsigned = { ...plan }
  delete unsigned.seal
  if ((await sha256Hex(new Blob([canonicalJson(unsigned)]))) !== digest) {
    fail('INVALID_AUTHORITY', 'Sealed Plan 的自封存摘要不一致。')
  }
  if (
    report.plan.id !== requireString(plan.plan_id, 'sealed-plan.json.plan_id') ||
    report.plan.version !== requireNumber(plan.version, 'sealed-plan.json.version') ||
    report.plan.sha256 !== digest
  ) {
    fail('AUTHORITY_MISMATCH', 'Report 没有绑定当前 Sealed Plan。')
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
  authorityVerified = false,
): Promise<LoadedBundle> {
  assertEntryLimits(entries)
  const manifestBlob = entries.get('bundle-manifest.json')
  if (!manifestBlob && entries.has('acceptance-bundle-manifest.json')) {
    fail('UNSUPPORTED_BUNDLE_KIND', '当前 Workbench 尚不支持 Acceptance Bundle。')
  }
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
  await validateSealedPlan(entries.get('sealed-plan.json')!, report)
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
  const validatedImages = new Map<string, { blob: Blob; mediaType: string }>()
  const createdUrls: string[] = []
  let imageWorkingSetBytes = 0
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
        if (attachment.media_type === 'image/png' || attachment.media_type === 'image/jpeg') {
          const existingImage = validatedImages.get(attachment.path)
          if (existingImage) {
            if (existingImage.mediaType !== attachment.media_type) {
              fail('REFERENCE_MISMATCH', '同一路径的图片附件声明了不同媒体类型。')
            }
            continue
          }
          try {
            const geometry = await validateImageGeometry(attachmentBlob, attachment.media_type)
            const estimatedWorkingSet = geometry.decodedBytes * IMAGE_RENDER_SURFACE_MULTIPLIER
            if (
              estimatedWorkingSet >
              MAX_BUNDLE_IMAGE_WORKING_SET_BYTES - imageWorkingSetBytes
            ) {
              fail('IMAGE_BUDGET_LIMIT', '图片附件的合计解码工作集超过 128 MiB。')
            }
            imageWorkingSetBytes += estimatedWorkingSet
          } catch (error) {
            if (error instanceof ImageGeometryError) fail(error.code, error.message)
            throw error
          }
          validatedImages.set(attachment.path, {
            blob: attachmentBlob,
            mediaType: attachment.media_type,
          })
        }
      }
    }
    // URL creation is deliberately a second phase. No browser-decodable handle
    // is exposed until every evidence document and the aggregate image budget
    // have passed validation.
    for (const [path, image] of validatedImages) {
      const objectUrl = URL.createObjectURL(
        new Blob([image.blob], { type: image.mediaType }),
      )
      imageUrls[path] = objectUrl
      createdUrls.push(objectUrl)
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
      authorityVerified,
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
  authorityVerified = false,
): Promise<LoadedBundle> {
  const entries = new Map<string, Blob>()
  const manifestUrl = safeSameOriginUrl(base, 'bundle-manifest.json')
  const manifestBlob = await fetchBlob(manifestUrl, 'Bundle Manifest')
  entries.set('bundle-manifest.json', manifestBlob)
  const manifest = validateBundleManifest(await parseJson(manifestBlob, 'bundle-manifest.json'))
  for (const file of manifest.files) {
    entries.set(file.path, await fetchBlob(safeSameOriginUrl(base, file.path), file.path))
  }
  return loadBundleFromBlobs(entries, sourceLabel, authorityVerified)
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
