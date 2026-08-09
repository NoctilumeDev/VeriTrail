import { sha256Hex } from '../src/domain/bundle'
import { vi } from 'vitest'

export function minimalReport(overrides: Record<string, unknown> = {}) {
  return {
    schema_version: '0.1',
    run_id: 'unit-run',
    created_at: '2026-08-09T00:00:00Z',
    plan: {
      id: 'unit-plan',
      version: 1,
      sha256: 'a'.repeat(64),
    },
    execution_status: 'COMPLETED',
    verdict: 'PASS',
    reasons: [{ code: 'UNIT_REASON', message: 'Deterministic fixture reason.' }],
    evidence: [],
    assertions: [
      {
        id: 'unit-assertion',
        severity: 'HARD',
        status: 'PASS',
        expected: true,
        actual: true,
      },
    ],
    missing_evidence: [],
    contamination: [],
    baseline: { id: 'unit-baseline', status: 'VALID' },
    primary_variable: { name: 'fixture_variant', role: 'PRIMARY', value: 'positive' },
    load_model: { virtual_users: 1 },
    resource_budget: { max_artifact_bytes: 1024 },
    change_scope: { level: 'L2_CONTRACT', owner: 'Vue Workbench' },
    reproduction_steps: ['Open the fixture.'],
    cleanup_steps: ['Close the page.'],
    ...overrides,
  }
}

export async function createMinimalBundle(
  reportOverrides: Record<string, unknown> = {},
): Promise<Map<string, Blob>> {
  const reportBlob = new Blob([JSON.stringify(minimalReport(reportOverrides))], {
    type: 'application/json',
  })
  const evidenceManifestBlob = new Blob([
    JSON.stringify({
      schema_version: '0.1',
      run_id: (reportOverrides.run_id as string | undefined) ?? 'unit-run',
      artifacts: [],
      duplicate_inputs_ignored: [],
    }),
  ])
  const files = [
    {
      path: 'evidence-manifest.json',
      sha256: await sha256Hex(evidenceManifestBlob),
      size: evidenceManifestBlob.size,
    },
    {
      path: 'report.json',
      sha256: await sha256Hex(reportBlob),
      size: reportBlob.size,
    },
  ]
  const manifestBlob = new Blob([
    JSON.stringify({ schema_version: '0.1', run_id: files.length ? ((reportOverrides.run_id as string | undefined) ?? 'unit-run') : 'unit-run', files }),
  ])
  return new Map([
    ['bundle-manifest.json', manifestBlob],
    ['evidence-manifest.json', evidenceManifestBlob],
    ['report.json', reportBlob],
  ])
}

export function installFetchForBundles(bundles: Record<string, Map<string, Blob>>) {
  return vi.spyOn(globalThis, 'fetch').mockImplementation(async (input) => {
    const url = new URL(typeof input === 'string' ? input : input instanceof URL ? input.href : input.url)
    const fixture = Object.keys(bundles).find((name) => url.pathname.includes(`/fixtures/${name}/`))
    const path = url.pathname.split(`/fixtures/${fixture}/`)[1]
    const blob = fixture && path ? bundles[fixture]?.get(path) : undefined
    return (blob
      ? { ok: true, status: 200, blob: async () => blob }
      : { ok: false, status: 404, blob: async () => new Blob(['missing']) }) as Response
  })
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

export async function createComparisonBundle(
  status: 'MATCH' | 'DRIFT' | 'INCONCLUSIVE' = 'MATCH',
): Promise<Map<string, Blob>> {
  const baselineBundle = 'b'.repeat(64)
  const repeatBundle = 'c'.repeat(64)
  const comparisonId = `cmp_${(
    await sha256Hex(
      new Blob([
        canonicalJson({
          schema_version: '0.1',
          rule_version: 'rerun-semantic/0.1',
          baseline_bundle_sha256: baselineBundle,
          repeat_bundle_sha256: repeatBundle,
        }),
      ]),
    )
  ).slice(0, 24)}`
  const source = (role: 'BASELINE' | 'REPEAT') => ({
    role,
    run_id: role === 'BASELINE' ? 'unit-baseline' : 'unit-repeat',
    created_at: '2026-08-09T00:00:00Z',
    execution_status: status === 'INCONCLUSIVE' && role === 'REPEAT' ? 'ABORTED' : 'COMPLETED',
    verdict: status === 'DRIFT' && role === 'REPEAT' ? 'FAIL' : status === 'INCONCLUSIVE' && role === 'REPEAT' ? 'PENDING' : 'PASS',
    plan: { id: 'unit-plan', version: 1, sha256: 'a'.repeat(64) },
    random_seed: 20260809,
    bundle_sha256: role === 'BASELINE' ? baselineBundle : repeatBundle,
    semantic_sha256: role === 'BASELINE' ? 'd'.repeat(64) : status === 'MATCH' ? 'd'.repeat(64) : 'e'.repeat(64),
  })
  const differences = status === 'MATCH' ? [] : [{
    path: '/verdict',
    baseline_present: true,
    repeat_present: true,
    baseline: 'PASS',
    repeat: status === 'DRIFT' ? 'FAIL' : 'PENDING',
  }]
  const comparison = {
    schema_version: '0.1',
    comparison_id: comparisonId,
    comparison_type: 'SAME_PLAN_RERUN',
    rule_version: 'rerun-semantic/0.1',
    comparison_status: status,
    comparable: status !== 'INCONCLUSIVE',
    reasons: [{
      code: status === 'MATCH' ? 'RERUN_SEMANTICS_MATCH' : status === 'DRIFT' ? 'RERUN_SEMANTIC_DRIFT' : 'RUN_NOT_COMPLETED',
      message: 'Deterministic comparison fixture.',
    }],
    sources: { baseline: source('BASELINE'), repeat: source('REPEAT') },
    differences,
    limits: ['MATCH 不等于任一来源 Run 的 Verdict 为 PASS。'],
  }
  const comparisonBlob = new Blob([JSON.stringify(comparison)])
  const markdownBlob = new Blob(['# Unit Comparison\n'])
  const files = [
    { path: 'comparison.json', sha256: await sha256Hex(comparisonBlob), size: comparisonBlob.size },
    { path: 'comparison.md', sha256: await sha256Hex(markdownBlob), size: markdownBlob.size },
  ]
  const manifestBlob = new Blob([
    JSON.stringify({ schema_version: '0.1', comparison_id: comparisonId, files }),
  ])
  return new Map([
    ['comparison-manifest.json', manifestBlob],
    ['comparison.json', comparisonBlob],
    ['comparison.md', markdownBlob],
  ])
}
