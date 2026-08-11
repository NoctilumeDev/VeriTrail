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

export async function createPairedAnalysisBundle(
  status: 'SUPPORTED' | 'CONTRADICTED' | 'INCONCLUSIVE' = 'SUPPORTED',
): Promise<Map<string, Blob>> {
  const roles = ['BASELINE', 'TREATMENT', 'RESTORED_BASELINE', 'NEGATIVE_CONTROL'] as const
  const planDigests = {
    BASELINE: 'a'.repeat(64),
    TREATMENT: 'b'.repeat(64),
    RESTORED_BASELINE: 'a'.repeat(64),
    NEGATIVE_CONTROL: 'c'.repeat(64),
  }
  const primaryValues = {
    BASELINE: 'nominal',
    TREATMENT: 'forced_failure',
    RESTORED_BASELINE: 'nominal',
    NEGATIVE_CONTROL: 'negative_control',
  }
  const pairingUnsigned = {
    schema_version: '0.1',
    pairing_id: 'unit-paired-analysis',
    version: 1,
    question: 'Does the treatment effect appear, restore, and remain absent in the negative control?',
    primary_variable: { name: 'experiment_condition', source: 'unit-fixture' },
    roles: Object.fromEntries(
      roles.map((role) => [
        role,
        { plan_sha256: planDigests[role], primary_value: primaryValues[role] },
      ]),
    ),
    sequence: roles,
    warmup: { mode: 'NONE', iterations: 0 },
    outcomes: [
      {
        assertion_id: 'suite-completed-successfully',
        expected_actual: {
          BASELINE: true,
          TREATMENT: false,
          RESTORED_BASELINE: true,
          NEGATIVE_CONTROL: true,
        },
      },
    ],
    limits: ['SUPPORTED 不等于来源 Run Verdict 为 PASS。'],
    reproduction_steps: ['Run all four roles in order.'],
    cleanup_steps: ['Remove only the unit fixture.'],
  }
  const pairingDigest = await sha256Hex(new Blob([canonicalJson(pairingUnsigned)]))
  const pairingPlan = {
    ...pairingUnsigned,
    seal: { algorithm: 'sha256', digest: pairingDigest },
  }
  const bundleDigests = {
    BASELINE: 'd'.repeat(64),
    TREATMENT: 'e'.repeat(64),
    RESTORED_BASELINE: 'f'.repeat(64),
    NEGATIVE_CONTROL: '1'.repeat(64),
  }
  const actuals = {
    BASELINE: true,
    TREATMENT: status === 'CONTRADICTED',
    RESTORED_BASELINE: true,
    NEGATIVE_CONTROL: status !== 'INCONCLUSIVE',
  }
  const expected = pairingUnsigned.outcomes[0].expected_actual
  const source = (role: typeof roles[number], index: number) => ({
    role,
    run_id: `unit-${role.toLowerCase()}`,
    created_at: `2026-08-09T00:00:0${index}Z`,
    execution_status: 'COMPLETED',
    verdict: role === 'TREATMENT' && status !== 'CONTRADICTED' ? 'FAIL' : role === 'NEGATIVE_CONTROL' && status === 'INCONCLUSIVE' ? 'FAIL' : 'PASS',
    plan: { id: 'unit-paired-plan', version: role === 'TREATMENT' ? 2 : role === 'NEGATIVE_CONTROL' ? 3 : 1, sha256: planDigests[role] },
    random_seed: 20260809,
    primary_variable: {
      name: 'experiment_condition',
      role: 'PRIMARY',
      value: primaryValues[role],
      source: 'unit-fixture',
    },
    bundle_sha256: bundleDigests[role],
    control_projection_sha256: '2'.repeat(64),
  })
  const orderedBundles = roles.map((role) => bundleDigests[role])
  const analysisId = `pair_${(
    await sha256Hex(
      new Blob([
        canonicalJson({
          schema_version: '0.1',
          rule_version: 'paired-counterfactual/0.1',
          pairing_plan_sha256: pairingDigest,
          ordered_bundle_sha256: orderedBundles,
        }),
      ]),
    )
  ).slice(0, 24)}`
  const analysis = {
    schema_version: '0.1',
    analysis_id: analysisId,
    analysis_type: 'FOUR_ROLE_PAIRED_COUNTERFACTUAL',
    rule_version: 'paired-counterfactual/0.1',
    analysis_status: status,
    attributable: status !== 'INCONCLUSIVE',
    pairing_plan: { id: pairingUnsigned.pairing_id, version: 1, sha256: pairingDigest },
    sequence: roles,
    warmup: { mode: 'NONE', iterations: 0 },
    primary_variable: pairingUnsigned.primary_variable,
    reasons: [
      {
        code: status === 'SUPPORTED' ? 'PAIRED_EFFECT_SUPPORTED' : status === 'CONTRADICTED' ? 'TREATMENT_EFFECT_CONTRADICTED' : 'NEGATIVE_CONTROL_EFFECT',
        message: 'Deterministic paired-analysis fixture.',
      },
    ],
    sources: Object.fromEntries(roles.map((role, index) => [role, source(role, index)])),
    outcomes: [
      {
        assertion_id: 'suite-completed-successfully',
        roles: Object.fromEntries(
          roles.map((role) => [
            role,
            {
              expected_actual: expected[role],
              actual: actuals[role],
              matches: expected[role] === actuals[role],
            },
          ]),
        ),
      },
    ],
    unplanned_differences: [],
    limits: pairingUnsigned.limits,
  }
  const pairingBlob = new Blob([JSON.stringify(pairingPlan)])
  const analysisBlob = new Blob([JSON.stringify(analysis)])
  const markdownBlob = new Blob(['# Unit Paired Analysis\n'])
  const files = [
    { path: 'sealed-pairing-plan.json', sha256: await sha256Hex(pairingBlob), size: pairingBlob.size },
    { path: 'paired-analysis.json', sha256: await sha256Hex(analysisBlob), size: analysisBlob.size },
    { path: 'paired-analysis.md', sha256: await sha256Hex(markdownBlob), size: markdownBlob.size },
  ]
  const manifestBlob = new Blob([
    JSON.stringify({ schema_version: '0.1', analysis_id: analysisId, files }),
  ])
  return new Map([
    ['paired-analysis-manifest.json', manifestBlob],
    ['sealed-pairing-plan.json', pairingBlob],
    ['paired-analysis.json', analysisBlob],
    ['paired-analysis.md', markdownBlob],
  ])
}

export async function createBatchAnalysisBundle(
  mode: 'SUPPORTED' | 'CONTRADICTED' | 'INCOMPLETE' | 'INCONCLUSIVE' = 'SUPPORTED',
): Promise<Map<string, Blob>> {
  const profiles = [
    {
      id: 'baseline',
      cells: { 'cache-mode': 'off', 'queue-mode': 'off' },
      plan_sha256: 'a'.repeat(64),
      realization: {
        subject_version: 'profile-baseline',
        subject_source_ref: 'fixtures/profile-baseline',
        target_root: 'fixtures/profile-baseline',
        static_root_fingerprint: '1'.repeat(64),
      },
      estimated_memory_mb: 256,
    },
    {
      id: 'queue-only',
      cells: { 'cache-mode': 'off', 'queue-mode': 'on' },
      plan_sha256: 'b'.repeat(64),
      realization: {
        subject_version: 'profile-queue-only',
        subject_source_ref: 'fixtures/profile-queue-only',
        target_root: 'fixtures/profile-queue-only',
        static_root_fingerprint: '2'.repeat(64),
      },
      estimated_memory_mb: 256,
    },
    {
      id: 'cache-only',
      cells: { 'cache-mode': 'on', 'queue-mode': 'off' },
      plan_sha256: 'c'.repeat(64),
      realization: {
        subject_version: 'profile-cache-only',
        subject_source_ref: 'fixtures/profile-cache-only',
        target_root: 'fixtures/profile-cache-only',
        static_root_fingerprint: '3'.repeat(64),
      },
      estimated_memory_mb: 256,
    },
    {
      id: 'combined',
      cells: { 'cache-mode': 'on', 'queue-mode': 'on' },
      plan_sha256: 'd'.repeat(64),
      realization: {
        subject_version: 'profile-combined',
        subject_source_ref: 'fixtures/profile-combined',
        target_root: 'fixtures/profile-combined',
        static_root_fingerprint: '4'.repeat(64),
      },
      estimated_memory_mb: 256,
    },
  ]
  const seed = 20260811
  const ranked = await Promise.all(
    profiles.map(async (profile) => ({
      id: profile.id,
      digest: await sha256Hex(new Blob([canonicalJson([seed, 1, profile.id])])),
    })),
  )
  const perturbationOrder = ranked
    .sort((left, right) => left.digest.localeCompare(right.digest) || left.id.localeCompare(right.id))
    .map((item) => item.id)
  const coverage = profiles.map((profile, index) => ({
    slot_id: `coverage-0${index + 1}`,
    phase: 'COVERAGE',
    repetition: 0,
    wave: index + 1,
    position: 1,
    profile_id: profile.id,
  }))
  const perturbation = perturbationOrder.map((profileId, index) => ({
    slot_id: `perturbation-0${index + 1}`,
    phase: 'PERTURBATION',
    repetition: 1,
    wave: Math.floor(index / 2) + 1,
    position: (index % 2) + 1,
    profile_id: profileId,
  }))
  const schedule = [...coverage, ...perturbation]
  const unsignedPlan = {
    schema_version: '0.1',
    batch_id: 'unit-batch-analysis',
    version: 1,
    question: 'Does every preregistered Profile retain its outcome across coverage and perturbation?',
    primary_variable: { name: 'batch_profile', source: 'unit-fixture', unit: 'profile' },
    dimensions: [
      { name: 'cache-mode', levels: [{ id: 'off', value: false }, { id: 'on', value: true }] },
      { name: 'queue-mode', levels: [{ id: 'off', value: false }, { id: 'on', value: true }] },
    ],
    profiles,
    execution_policy: {
      order_algorithm: 'SHA256_RANK_V1',
      seed,
      perturbation_repetitions: 1,
      max_parallel: 2,
      memory_budget_mb: 512,
      preflight_between_waves: true,
      cleanup_between_waves: true,
    },
    schedule,
    outcomes: [
      {
        assertion_id: 'console-errors-zero',
        expected_actual: {
          baseline: 0,
          'queue-only': 0,
          'cache-only': 0,
          combined: 1,
        },
      },
    ],
    limits: [
      'Profile-level observations do not prove component-level causality or statistical interaction.',
      'A wave is a sealed resource envelope and does not prove real runtime overlap.',
    ],
    reproduction_steps: ['Run every slot in the sealed order.'],
    cleanup_steps: ['Verify every wave cleanup boundary.'],
  }
  const planDigest = await sha256Hex(new Blob([canonicalJson(unsignedPlan)]))
  const batchPlan = { ...unsignedPlan, seal: { algorithm: 'sha256', digest: planDigest } }
  const profileMap = new Map(profiles.map((profile) => [profile.id, profile]))
  const missingSlotId = mode === 'INCOMPLETE' ? schedule.at(-1)!.slot_id : null
  const waveOrder = new Map<string, number>()
  let waveSequence = 0
  schedule.forEach((slot) => {
    const key = `${slot.phase}:${slot.repetition}:${slot.wave}`
    if (!waveOrder.has(key)) waveOrder.set(key, waveSequence++)
  })
  const slots = schedule.map((slot, index) => {
    const profile = profileMap.get(slot.profile_id)!
    const expected = slot.profile_id === 'combined' ? 1 : 0
    const actual =
      slot.slot_id === missingSlotId
        ? null
        : mode === 'CONTRADICTED' && slot.profile_id === 'combined'
          ? 0
          : expected
    const source =
      slot.slot_id === missingSlotId
        ? null
        : {
            run_id: `unit-batch-run-${index + 1}`,
            created_at: `2026-08-11T00:00:${String(waveOrder.get(`${slot.phase}:${slot.repetition}:${slot.wave}`)!).padStart(2, '0')}Z`,
            execution_status: 'COMPLETED',
            verdict: slot.profile_id === 'combined' ? 'FAIL' : 'PASS',
            plan: { id: `unit-plan-${slot.profile_id}`, version: 4, sha256: profile.plan_sha256 },
            random_seed: seed,
            primary_variable: {
              name: 'batch_profile',
              role: 'PRIMARY',
              value: slot.profile_id,
              source: 'unit-fixture',
              unit: 'profile',
            },
            bundle_sha256: (index + 5).toString(16).repeat(64),
            control_projection_sha256: 'e'.repeat(64),
            preflight_complete: true,
            cleanup_complete: true,
            browser_complete: true,
            static_root_fingerprint: profile.realization.static_root_fingerprint,
          }
    return {
      ...slot,
      source,
      outcomes: [
        {
          assertion_id: 'console-errors-zero',
          expected_actual: expected,
          actual,
          matches: actual === expected,
        },
      ],
    }
  })
  const orderedBundles = slots.map((slot) => slot.source?.bundle_sha256 ?? 'MISSING')
  const analysisId = `batch_${(
    await sha256Hex(
      new Blob([
        canonicalJson({
          schema_version: '0.1',
          rule_version: 'full-factorial-batch/0.1',
          batch_plan_sha256: planDigest,
          ordered_bundle_sha256: orderedBundles,
        }),
      ]),
    )
  ).slice(0, 24)}`
  const profileSummaries = profiles.map((profile) => {
    const profileSlots = slots.filter((slot) => slot.profile_id === profile.id)
    return {
      id: profile.id,
      cells: profile.cells,
      occurrence_count: profileSlots.length,
      completed_count: profileSlots.filter((slot) => slot.source?.execution_status === 'COMPLETED').length,
      mismatch_count: profileSlots.flatMap((slot) => slot.outcomes).filter((outcome) => !outcome.matches).length,
    }
  })
  const state = {
    SUPPORTED: {
      coverage: 'COMPLETE',
      hypothesis: 'SUPPORTED',
      code: 'BATCH_HYPOTHESIS_SUPPORTED',
    },
    CONTRADICTED: {
      coverage: 'COMPLETE',
      hypothesis: 'CONTRADICTED',
      code: 'BATCH_HYPOTHESIS_CONTRADICTED',
    },
    INCOMPLETE: {
      coverage: 'INCOMPLETE',
      hypothesis: 'INCONCLUSIVE',
      code: 'SLOT_MISSING',
    },
    INCONCLUSIVE: {
      coverage: 'INCONCLUSIVE',
      hypothesis: 'INCONCLUSIVE',
      code: 'UNDECLARED_OUTCOME_DRIFT',
    },
  }[mode]
  const unplannedDifferences =
    mode === 'INCONCLUSIVE'
      ? [
          {
            slot_id: 'perturbation-01',
            assertion_id: 'unplanned-observation',
            baseline: { status: 'PASS' },
            observed: { status: 'FAIL' },
          },
        ]
      : []
  const analysis = {
    schema_version: '0.1',
    analysis_id: analysisId,
    analysis_type: 'PREREGISTERED_FULL_FACTORIAL_BATCH',
    rule_version: 'full-factorial-batch/0.1',
    coverage_status: state.coverage,
    hypothesis_status: state.hypothesis,
    runtime_overlap_claim: 'NOT_PROVEN',
    batch_plan: { id: unsignedPlan.batch_id, version: 1, sha256: planDigest },
    primary_variable: unsignedPlan.primary_variable,
    execution_policy: unsignedPlan.execution_policy,
    reasons: [{ code: state.code, message: 'Deterministic batch-analysis fixture.' }],
    slots,
    profiles: profileSummaries,
    unplanned_differences: unplannedDifferences,
    limits: unsignedPlan.limits,
  }
  const planBlob = new Blob([JSON.stringify(batchPlan)])
  const analysisBlob = new Blob([JSON.stringify(analysis)])
  const markdownBlob = new Blob(['# Unit Batch Analysis\n'])
  const files = [
    { path: 'sealed-batch-plan.json', sha256: await sha256Hex(planBlob), size: planBlob.size },
    { path: 'batch-analysis.json', sha256: await sha256Hex(analysisBlob), size: analysisBlob.size },
    { path: 'batch-analysis.md', sha256: await sha256Hex(markdownBlob), size: markdownBlob.size },
  ]
  const manifestBlob = new Blob([
    JSON.stringify({ schema_version: '0.1', analysis_id: analysisId, files }),
  ])
  return new Map([
    ['batch-analysis-manifest.json', manifestBlob],
    ['sealed-batch-plan.json', planBlob],
    ['batch-analysis.json', analysisBlob],
    ['batch-analysis.md', markdownBlob],
  ])
}
