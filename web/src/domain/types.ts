export type ExecutionStatus = 'PLANNED' | 'RUNNING' | 'COMPLETED' | 'ABORTED' | 'ERROR'
export type Verdict = 'PASS' | 'FAIL' | 'INCONCLUSIVE' | 'PENDING'
export type AssertionStatus = 'PASS' | 'FAIL' | 'PENDING' | 'INCONCLUSIVE' | string

export interface PlanReference {
  id: string
  version: number
  sha256: string
}

export interface ReportReason {
  code: string
  message: string
}

export interface ReportAssertion {
  id: string
  severity: string
  status: AssertionStatus
  expected: unknown
  actual: unknown
  explanation?: string
  evidence_type?: string
  evidence_sha256?: string[]
  operator?: string
  path?: string
}

export interface EvidenceAttachment {
  logical_name: string
  media_type: string
  path: string
  sha256: string
  size: number
}

export interface EvidenceArtifact {
  evidence_type: string
  path: string
  sha256: string
  size: number
  redacted: boolean
  redacted_fields: number
  redaction_rule_version: string
  parser_version: string
  captured_at: string
  source: string
  source_name: string
  retention: string
  attachments: EvidenceAttachment[]
  summary?: Record<string, unknown>
}

export interface VerdictReport {
  schema_version: '0.1'
  run_id: string
  created_at: string
  plan: PlanReference
  execution_status: ExecutionStatus
  verdict: Verdict
  reasons: ReportReason[]
  evidence: EvidenceArtifact[]
  assertions: ReportAssertion[]
  missing_evidence: string[]
  contamination: Array<Record<string, unknown>>
  subject?: Record<string, unknown>
  baseline?: Record<string, unknown>
  random_seed?: number
  primary_variable?: Record<string, unknown>
  load_model?: Record<string, unknown>
  resource_budget?: Record<string, unknown>
  change_scope?: Record<string, unknown>
  reproduction_steps?: string[]
  cleanup_steps?: string[]
}

export interface EvidenceDocument {
  schema_version: '0.1'
  evidence_type: string
  source: string
  captured_at: string
  facts: Record<string, unknown>
  observed_variables?: Record<string, unknown>
  metadata?: Record<string, unknown>
}

export interface EvidenceManifest {
  schema_version: '0.1'
  run_id: string
  artifacts: EvidenceArtifact[]
  duplicate_inputs_ignored: string[]
}

export interface BundleFileEntry {
  path: string
  sha256: string
  size: number
}

export interface BundleManifest {
  schema_version: '0.1'
  run_id: string
  files: BundleFileEntry[]
}

export interface BundleIntegrity {
  verified: true
  verifiedFiles: number
  totalBytes: number
}

export interface LoadedBundle {
  sourceLabel: string
  report: VerdictReport
  bundleManifest: BundleManifest
  evidenceManifest: EvidenceManifest
  evidenceByPath: Record<string, EvidenceDocument>
  imageUrls: Record<string, string>
  integrity: BundleIntegrity
  release: () => void
}

export interface BrowserStep {
  step_id: string
  action: string
  status: string
  viewport: string
  elapsed_ms: number
  error?: string | null
}

export interface BrowserConsoleEntry {
  level: string
  text: string
  viewport: string
  captured_at?: string
}

export interface BrowserNetworkEntry {
  sequence: number
  method: string
  url: string
  status: number | null
  viewport: string
  resource_type: string
  finished: boolean
  failure?: string | null
}

export interface BrowserViewportRun {
  name: string
  width: number
  height: number
  is_mobile: boolean
  status: string
  horizontal_overflow_px: number
  step_count: number
  network_request_count: number
}

export interface BrowserScreenshot {
  name: string
  path: string
  sha256: string
  size: number
  step_id: string
  viewport: string
  media_type: string
}

export interface CatalogRunSummary {
  catalog_run_id: string
  run_id: string
  created_at: string
  execution_status: ExecutionStatus
  verdict: Verdict
  plan: PlanReference
  bundle: {
    sha256: string
    file_count: number
    total_bytes: number
    duplicate_count: number
    base_url: string
  }
}

export interface CatalogIssueSummary {
  issue_id: string
  code: string
  candidate_id: string
  run_id: string | null
  bundle_digests: string[]
  occurrence_count: number
}

export interface CatalogResponse {
  schema_version: '0.1'
  catalog: {
    catalog_id: string
    build_status: 'COMPLETED' | 'COMPLETED_WITH_ISSUES'
    read_only: true
    run_count: number
    issue_count: number
    duplicate_count: number
  }
  pagination: {
    page: number
    page_size: number
    total_items: number
    total_pages: number
  }
  runs: CatalogRunSummary[]
  issues: CatalogIssueSummary[]
  issues_truncated: boolean
}

export type ComparisonStatus = 'MATCH' | 'DRIFT' | 'INCONCLUSIVE'

export interface ComparisonSource {
  role: 'BASELINE' | 'REPEAT'
  run_id: string
  created_at: string
  execution_status: ExecutionStatus
  verdict: Verdict
  plan: PlanReference
  random_seed: number
  bundle_sha256: string
  semantic_sha256: string
}

export interface ComparisonDifference {
  path: string
  baseline_present: boolean
  repeat_present: boolean
  baseline: unknown
  repeat: unknown
}

export interface RerunComparison {
  schema_version: '0.1'
  comparison_id: string
  comparison_type: 'SAME_PLAN_RERUN'
  rule_version: 'rerun-semantic/0.1'
  comparison_status: ComparisonStatus
  comparable: boolean
  reasons: ReportReason[]
  sources: {
    baseline: ComparisonSource
    repeat: ComparisonSource
  }
  differences: ComparisonDifference[]
  limits: string[]
}

export interface ComparisonManifest {
  schema_version: '0.1'
  comparison_id: string
  files: BundleFileEntry[]
}

export interface LoadedComparison {
  comparison: RerunComparison
  manifest: ComparisonManifest
  integrity: BundleIntegrity
}
