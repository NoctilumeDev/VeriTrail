import { describe, expect, it } from 'vitest'
import {
  buildWorkbenchUrl,
  historyStateForRoute,
  parseWorkbenchRoute,
  type WorkbenchRouteSnapshot,
  type WorkbenchRouteTarget,
} from '../src/domain/workbenchRoute'

const catalogRunId = `cr_${'a'.repeat(24)}`

function expectRoute(
  href: string,
  expected: Partial<WorkbenchRouteSnapshot>,
) {
  expect(parseWorkbenchRoute(href)).toEqual(expect.objectContaining(expected))
}

describe('Workbench URL route state', () => {
  it.each([
    ['/', { kind: 'catalog', publicView: 'runs', runSurface: 'catalog', activeSource: 'catalog' }],
    ['/?view=runs', { kind: 'catalog', publicView: 'runs', runSurface: 'catalog', activeSource: 'catalog' }],
    ['/?view=comparison', { kind: 'analysis-view', publicView: 'comparison', activeSource: 'comparison' }],
    ['/?view=pairing', { kind: 'analysis-view', publicView: 'pairing', activeSource: 'pairing' }],
    ['/?view=batch', { kind: 'analysis-view', publicView: 'batch', activeSource: 'batch' }],
    ['/?fixture=positive', { kind: 'demo', runSurface: 'detail', activeSource: 'positive', demoFixture: 'positive' }],
    ['/?fixture=negative', { kind: 'demo', runSurface: 'detail', activeSource: 'negative', demoFixture: 'negative' }],
    ['/?fixture=invalid', { kind: 'demo', runSurface: 'catalog', activeSource: 'invalid', demoFixture: 'invalid' }],
    ['/?fixture=local', { kind: 'local', runSurface: 'detail', activeSource: 'local' }],
    ['/?fixture=comparison', { kind: 'comparison', publicView: 'comparison', analysisView: 'comparison' }],
    ['/?fixture=pairing', { kind: 'pairing', publicView: 'pairing', analysisView: 'pairing' }],
    ['/?fixture=batch', { kind: 'batch', publicView: 'batch', analysisView: 'batch' }],
  ] as const)('parses canonical public route %s', (href, expected) => {
    expectRoute(href, expected)
  })

  it.each(['browser', 'assertions', 'ledger'] as const)(
    'parses the %s Run panel for Catalog, demo, and in-memory Run routes',
    (panel) => {
      expectRoute(`/?run=${catalogRunId}&panel=${panel}`, {
        kind: 'run',
        catalogRunId,
        runDetailPanel: panel,
      })
      expectRoute(`/?fixture=positive&panel=${panel}`, {
        kind: 'demo',
        demoFixture: 'positive',
        runDetailPanel: panel,
      })
      expectRoute(`/?fixture=negative&panel=${panel}`, {
        kind: 'demo',
        demoFixture: 'negative',
        runDetailPanel: panel,
      })
      expectRoute(`/?fixture=local&panel=${panel}`, {
        kind: 'local',
        runDetailPanel: panel,
      })
    },
  )

  it('parses analysis review samples together with their owned panels', () => {
    expectRoute('/?fixture=comparison&sample=drift&panel=differences', {
      kind: 'comparison',
      comparisonSample: 'drift',
      comparisonPanel: 'differences',
    })
    expectRoute('/?fixture=pairing&sample=supported&panel=sources', {
      kind: 'pairing',
      pairingSample: 'supported',
      pairingPanel: 'sources',
    })
    expectRoute('/?fixture=pairing&sample=supported&panel=outcomes', {
      kind: 'pairing',
      pairingSample: 'supported',
      pairingPanel: 'outcomes',
    })
    expectRoute('/?fixture=batch&sample=supported', {
      kind: 'batch',
      batchSample: 'supported',
    })
  })

  it('uses one deterministic authority order for conflicting managed keys', () => {
    expectRoute(`/?run=${catalogRunId}&fixture=negative&view=batch&panel=ledger`, {
      kind: 'run',
      catalogRunId,
      runDetailPanel: 'ledger',
    })
    expectRoute('/?fixture=pairing&view=comparison&sample=supported', {
      kind: 'pairing',
      publicView: 'pairing',
      pairingSample: 'supported',
    })
  })

  it.each([
    '/?run=not-a-catalog-run&fixture=positive',
    '/?run=&view=comparison',
    '/?fixture=unknown&view=pairing',
    '/?view=unknown',
    '/?unmanaged=value',
  ])('fails closed to Catalog for malformed or unknown route %s', (href) => {
    expect(parseWorkbenchRoute(href)).toMatchObject({
      kind: 'catalog',
      publicView: 'runs',
      runSurface: 'catalog',
      activeSource: 'catalog',
      catalogRunId: null,
      demoFixture: null,
    })
  })

  it('distinguishes malformed managed routes from valid Catalog aliases', () => {
    expect(parseWorkbenchRoute('/').requiresCanonicalization).toBe(false)
    expect(parseWorkbenchRoute('/?view=runs').requiresCanonicalization).toBe(false)
    expect(parseWorkbenchRoute('/?trace=keep').requiresCanonicalization).toBe(false)
    expect(parseWorkbenchRoute('/?run=bad').requiresCanonicalization).toBe(true)
    expect(parseWorkbenchRoute('/?fixture=unknown').requiresCanonicalization).toBe(true)
    expect(parseWorkbenchRoute('/?view=unknown').requiresCanonicalization).toBe(true)
  })

  it('ignores panels and samples that are outside their owning route', () => {
    expect(parseWorkbenchRoute(`/?run=${catalogRunId}&panel=sources`).runDetailPanel).toBeNull()
    expect(parseWorkbenchRoute('/?fixture=positive&panel=differences').runDetailPanel).toBeNull()
    expect(parseWorkbenchRoute('/?fixture=invalid&panel=assertions').runDetailPanel).toBeNull()
    expect(parseWorkbenchRoute('/?fixture=pairing&sample=drift&panel=assertions')).toMatchObject({
      pairingSample: null,
      pairingPanel: null,
    })
    expect(parseWorkbenchRoute('/?fixture=comparison&sample=supported&panel=sources')).toMatchObject({
      comparisonSample: null,
      comparisonPanel: null,
    })
    expect(parseWorkbenchRoute('/?fixture=batch&panel=differences')).toMatchObject({
      runDetailPanel: null,
      pairingPanel: null,
      comparisonPanel: null,
    })
  })
})

describe('Workbench URL construction', () => {
  const currentHref = 'https://example.test/workbench?fixture=negative&run=stale&view=batch&panel=ledger&sample=drift&trace=keep#evidence'

  const roundTrips: Array<{
    name: string
    target: WorkbenchRouteTarget
    expected: Partial<WorkbenchRouteSnapshot>
  }> = [
    {
      name: 'Catalog',
      target: { kind: 'catalog' },
      expected: { kind: 'catalog', publicView: 'runs', runSurface: 'catalog' },
    },
    {
      name: 'Runs view',
      target: { kind: 'view', view: 'runs' },
      expected: { kind: 'catalog', publicView: 'runs', runSurface: 'catalog' },
    },
    {
      name: 'Comparison entry',
      target: { kind: 'view', view: 'comparison' },
      expected: { kind: 'analysis-view', publicView: 'comparison' },
    },
    {
      name: 'positive demo assertions',
      target: { kind: 'demo', fixture: 'positive', panel: 'assertions' },
      expected: { kind: 'demo', demoFixture: 'positive', runDetailPanel: 'assertions' },
    },
    {
      name: 'negative demo browser evidence',
      target: { kind: 'demo', fixture: 'negative', panel: 'browser' },
      expected: { kind: 'demo', demoFixture: 'negative', runDetailPanel: 'browser' },
    },
    {
      name: 'invalid demo',
      target: { kind: 'demo', fixture: 'invalid' },
      expected: { kind: 'demo', demoFixture: 'invalid', runDetailPanel: null },
    },
    {
      name: 'local evidence ledger',
      target: { kind: 'local', panel: 'ledger' },
      expected: { kind: 'local', activeSource: 'local', runDetailPanel: 'ledger' },
    },
    {
      name: 'Catalog Run browser evidence',
      target: { kind: 'run', catalogRunId, panel: 'browser' },
      expected: { kind: 'run', catalogRunId, runDetailPanel: 'browser' },
    },
    {
      name: 'Comparison review differences',
      target: { kind: 'comparison', sample: 'drift', panel: 'differences' },
      expected: { kind: 'comparison', comparisonSample: 'drift', comparisonPanel: 'differences' },
    },
    {
      name: 'Pairing review sources',
      target: { kind: 'pairing', sample: 'supported', panel: 'sources' },
      expected: { kind: 'pairing', pairingSample: 'supported', pairingPanel: 'sources' },
    },
    {
      name: 'Pairing review outcomes',
      target: { kind: 'pairing', sample: 'supported', panel: 'outcomes' },
      expected: { kind: 'pairing', pairingSample: 'supported', pairingPanel: 'outcomes' },
    },
    {
      name: 'Batch import',
      target: { kind: 'batch' },
      expected: { kind: 'batch', publicView: 'batch' },
    },
    {
      name: 'Batch review sample',
      target: { kind: 'batch', sample: 'supported' },
      expected: { kind: 'batch', publicView: 'batch', batchSample: 'supported' },
    },
  ]

  it.each(roundTrips)('round-trips $name without stale managed state', ({ target, expected }) => {
    const built = buildWorkbenchUrl(currentHref, target)

    expect(built.origin).toBe('https://example.test')
    expect(built.pathname).toBe('/workbench')
    expect(built.hash).toBe('#evidence')
    expect(built.searchParams.get('trace')).toBe('keep')
    expect(parseWorkbenchRoute(built)).toEqual(expect.objectContaining(expected))
  })

  it('does not mutate a URL instance supplied as the construction base', () => {
    const original = new URL(currentHref)
    const before = original.href

    const built = buildWorkbenchUrl(original, {
      kind: 'pairing',
      sample: 'supported',
      panel: 'sources',
    })

    expect(original.href).toBe(before)
    expect(built).not.toBe(original)
    expect(built.searchParams.get('run')).toBeNull()
    expect(built.searchParams.get('view')).toBeNull()
    expect(built.searchParams.get('fixture')).toBe('pairing')
  })
})

describe('Workbench History state', () => {
  it.each([
    [{ kind: 'catalog' }, {}],
    [{ kind: 'view', view: 'runs' }, { view: 'runs' }],
    [{ kind: 'view', view: 'comparison' }, { view: 'comparison' }],
    [{ kind: 'demo', fixture: 'positive' }, { fixture: 'positive' }],
    [{ kind: 'demo', fixture: 'negative', panel: 'browser' }, { fixture: 'negative', panel: 'browser' }],
    [{ kind: 'local', panel: 'ledger' }, { fixture: 'local', panel: 'ledger' }],
    [{ kind: 'run', catalogRunId, panel: 'assertions' }, { run: catalogRunId, panel: 'assertions' }],
    [
      { kind: 'comparison', sample: 'drift', panel: 'differences' },
      { fixture: 'comparison', sample: 'drift', panel: 'differences' },
    ],
    [
      { kind: 'pairing', sample: 'supported', panel: 'outcomes' },
      { fixture: 'pairing', sample: 'supported', panel: 'outcomes' },
    ],
    [{ kind: 'batch' }, { fixture: 'batch' }],
    [
      { kind: 'batch', sample: 'supported' },
      { fixture: 'batch', sample: 'supported' },
    ],
  ] as Array<[WorkbenchRouteTarget, Record<string, string>]>) (
    'keeps History state aligned with canonical route %#',
    (target, expected) => {
      expect(historyStateForRoute(target)).toEqual(expected)
    },
  )
})
