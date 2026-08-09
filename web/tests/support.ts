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
