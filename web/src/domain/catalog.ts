import type {
  CatalogIssueSummary,
  CatalogResponse,
  CatalogRunSummary,
  ExecutionStatus,
  Verdict,
} from './types'

const SHA256 = /^[0-9a-f]{64}$/
const CATALOG_ID = /^cat_[0-9a-f]{24}$/
const CATALOG_RUN_ID = /^cr_[0-9a-f]{24}$/
const ISSUE_ID = /^ci_[0-9a-f]{24}$/
const CANDIDATE_ID = /^cand_[0-9a-f]{20}$/
const EXECUTION_STATUSES = new Set<ExecutionStatus>([
  'PLANNED',
  'RUNNING',
  'COMPLETED',
  'ABORTED',
  'ERROR',
])
const VERDICTS = new Set<Verdict>(['PASS', 'FAIL', 'INCONCLUSIVE', 'PENDING'])

export class CatalogLoadError extends Error {
  readonly code: string

  constructor(code: string, message: string) {
    super(message)
    this.name = 'CatalogLoadError'
    this.code = code
  }
}

function fail(code: string, message: string): never {
  throw new CatalogLoadError(code, message)
}

function record(value: unknown, name: string): Record<string, unknown> {
  if (typeof value !== 'object' || value === null || Array.isArray(value)) {
    fail('CATALOG_INVALID', `${name} 不是有效对象。`)
  }
  return value as Record<string, unknown>
}

function string(value: unknown, name: string, pattern?: RegExp): string {
  if (typeof value !== 'string' || !value || (pattern && !pattern.test(value))) {
    fail('CATALOG_INVALID', `${name} 不符合 Catalog API 0.1。`)
  }
  return value
}

function integer(value: unknown, name: string, maximum?: number): number {
  if (!Number.isInteger(value) || (value as number) < 0 || (maximum !== undefined && (value as number) > maximum)) {
    fail('CATALOG_INVALID', `${name} 不符合 Catalog API 0.1。`)
  }
  return value as number
}

function array(value: unknown, name: string): unknown[] {
  if (!Array.isArray(value)) fail('CATALOG_INVALID', `${name} 不是数组。`)
  return value
}

function parseRun(value: unknown): CatalogRunSummary {
  const run = record(value, 'runs[]')
  const catalogRunId = string(run.catalog_run_id, 'catalog_run_id', CATALOG_RUN_ID)
  const executionStatus = string(run.execution_status, 'execution_status') as ExecutionStatus
  const verdict = string(run.verdict, 'verdict') as Verdict
  if (!EXECUTION_STATUSES.has(executionStatus) || !VERDICTS.has(verdict)) {
    fail('CATALOG_INVALID', 'Run 状态或裁决不符合冻结语义。')
  }
  const plan = record(run.plan, 'run.plan')
  const bundle = record(run.bundle, 'run.bundle')
  const expectedBase = `/api/v1/runs/${catalogRunId}/bundle/`
  if (bundle.base_url !== expectedBase) fail('CATALOG_INVALID', 'Bundle API 路径不是固定同源路径。')
  return {
    catalog_run_id: catalogRunId,
    run_id: string(run.run_id, 'run_id'),
    created_at: string(run.created_at, 'created_at'),
    execution_status: executionStatus,
    verdict,
    plan: {
      id: string(plan.id, 'plan.id'),
      version: integer(plan.version, 'plan.version'),
      sha256: string(plan.sha256, 'plan.sha256', SHA256),
    },
    bundle: {
      sha256: string(bundle.sha256, 'bundle.sha256', SHA256),
      file_count: integer(bundle.file_count, 'bundle.file_count', 256),
      total_bytes: integer(bundle.total_bytes, 'bundle.total_bytes', 64 * 1024 * 1024),
      duplicate_count: integer(bundle.duplicate_count, 'bundle.duplicate_count'),
      base_url: expectedBase,
    },
  }
}

function parseIssue(value: unknown): CatalogIssueSummary {
  const issue = record(value, 'issues[]')
  return {
    issue_id: string(issue.issue_id, 'issue_id', ISSUE_ID),
    code: string(issue.code, 'issue.code'),
    candidate_id: string(issue.candidate_id, 'candidate_id', CANDIDATE_ID),
    run_id: issue.run_id === null ? null : string(issue.run_id, 'issue.run_id'),
    bundle_digests: array(issue.bundle_digests, 'bundle_digests').map((digest) =>
      string(digest, 'bundle_digest', SHA256),
    ),
    occurrence_count: integer(issue.occurrence_count, 'occurrence_count'),
  }
}

export function validateCatalog(value: unknown): CatalogResponse {
  const response = record(value, 'Catalog response')
  if (response.schema_version !== '0.1') fail('CATALOG_VERSION_UNSUPPORTED', 'Catalog API 版本不受支持。')
  const catalog = record(response.catalog, 'catalog')
  const pagination = record(response.pagination, 'pagination')
  const buildStatus = string(catalog.build_status, 'catalog.build_status')
  if (!['COMPLETED', 'COMPLETED_WITH_ISSUES'].includes(buildStatus) || catalog.read_only !== true) {
    fail('CATALOG_INVALID', 'Catalog 状态或只读标记无效。')
  }
  const page = integer(pagination.page, 'pagination.page')
  const pageSize = integer(pagination.page_size, 'pagination.page_size', 100)
  if (page < 1 || pageSize < 1) fail('CATALOG_INVALID', 'Catalog 分页无效。')
  const runs = array(response.runs, 'runs').map(parseRun)
  if (runs.length > 100) fail('CATALOG_INVALID', 'Catalog 单页超过 100 个 Run。')
  const issues = array(response.issues, 'issues').map(parseIssue)
  if (issues.length > 100) fail('CATALOG_INVALID', 'Catalog 问题摘要超过 100 项。')
  if (typeof response.issues_truncated !== 'boolean') fail('CATALOG_INVALID', 'Catalog 问题截断标记无效。')
  return {
    schema_version: '0.1',
    catalog: {
      catalog_id: string(catalog.catalog_id, 'catalog_id', CATALOG_ID),
      build_status: buildStatus as CatalogResponse['catalog']['build_status'],
      read_only: true,
      run_count: integer(catalog.run_count, 'run_count'),
      issue_count: integer(catalog.issue_count, 'issue_count'),
      duplicate_count: integer(catalog.duplicate_count, 'duplicate_count'),
    },
    pagination: {
      page,
      page_size: pageSize,
      total_items: integer(pagination.total_items, 'total_items'),
      total_pages: integer(pagination.total_pages, 'total_pages'),
    },
    runs,
    issues,
    issues_truncated: response.issues_truncated,
  }
}

export async function fetchCatalog(): Promise<CatalogResponse | null> {
  let response: Response
  try {
    response = await fetch('/api/v1/catalog', {
      credentials: 'same-origin',
      cache: 'no-store',
      headers: { Accept: 'application/json' },
    })
  } catch {
    return null
  }
  if (response.status === 404) return null
  const text = await response.blob().then((blob) => blob.text())
  if (response.ok && /^\s*<!doctype html/i.test(text)) return null
  if (!response.ok) fail('CATALOG_API_UNAVAILABLE', '本地 Run 目录暂时不可用。')
  try {
    return validateCatalog(JSON.parse(text) as unknown)
  } catch (cause) {
    if (cause instanceof CatalogLoadError) throw cause
    fail('CATALOG_INVALID', 'Catalog API 返回了无效 JSON。')
  }
}

export function parseCatalogRunId(value: string | null): string | null {
  return value && CATALOG_RUN_ID.test(value) ? value : null
}
