import type { DemoBundleId } from './bundle'
import { parseCatalogRunId } from './catalog'

export type PublicView = 'runs' | 'comparison' | 'pairing' | 'batch'
export type RunSurface = 'catalog' | 'detail'
export type RunDetailPanel = 'browser' | 'assertions' | 'ledger'
export type PairingPanel = 'sources' | 'outcomes'
export type ComparisonPanel = 'differences'
export type AnalysisView = Exclude<PublicView, 'runs'>
export type WorkbenchFixture = DemoBundleId | 'local' | AnalysisView
export type ActiveSource = WorkbenchFixture | 'catalog'
export type ComparisonSample = 'drift'
export type PairingSample = 'supported'
export type BatchSample = 'supported'

export type WorkbenchRouteKind =
  | 'catalog'
  | 'run'
  | 'demo'
  | 'local'
  | 'analysis-view'
  | 'comparison'
  | 'pairing'
  | 'batch'

export interface WorkbenchRouteSnapshot {
  kind: WorkbenchRouteKind
  requiresCanonicalization: boolean
  publicView: PublicView
  runSurface: RunSurface
  activeSource: ActiveSource
  catalogRunId: string | null
  demoFixture: DemoBundleId | null
  analysisView: AnalysisView | null
  runDetailPanel: RunDetailPanel | null
  pairingPanel: PairingPanel | null
  comparisonPanel: ComparisonPanel | null
  pairingSample: PairingSample | null
  comparisonSample: ComparisonSample | null
  batchSample: BatchSample | null
}

export type WorkbenchRouteTarget =
  | { kind: 'catalog' }
  | { kind: 'view'; view: PublicView }
  | { kind: 'demo'; fixture: DemoBundleId; panel?: RunDetailPanel | null }
  | { kind: 'local'; panel?: RunDetailPanel | null }
  | { kind: 'run'; catalogRunId: string; panel?: RunDetailPanel | null }
  | { kind: 'comparison'; panel?: ComparisonPanel | null; sample?: ComparisonSample | null }
  | { kind: 'pairing'; panel?: PairingPanel | null; sample?: PairingSample | null }
  | { kind: 'batch'; sample?: BatchSample | null }

const MANAGED_QUERY_KEYS = ['fixture', 'run', 'view', 'panel', 'sample'] as const

function runDetailPanel(params: URLSearchParams): RunDetailPanel | null {
  const panel = params.get('panel')
  return panel === 'browser' || panel === 'assertions' || panel === 'ledger' ? panel : null
}

function pairingPanel(params: URLSearchParams): PairingPanel | null {
  const panel = params.get('panel')
  return panel === 'sources' || panel === 'outcomes' ? panel : null
}

function comparisonPanel(params: URLSearchParams): ComparisonPanel | null {
  return params.get('panel') === 'differences' ? 'differences' : null
}

function snapshot(overrides: Partial<WorkbenchRouteSnapshot>): WorkbenchRouteSnapshot {
  return {
    kind: 'catalog',
    requiresCanonicalization: false,
    publicView: 'runs',
    runSurface: 'catalog',
    activeSource: 'catalog',
    catalogRunId: null,
    demoFixture: null,
    analysisView: null,
    runDetailPanel: null,
    pairingPanel: null,
    comparisonPanel: null,
    pairingSample: null,
    comparisonSample: null,
    batchSample: null,
    ...overrides,
  }
}

export function parseWorkbenchRoute(href: string | URL): WorkbenchRouteSnapshot {
  const url = href instanceof URL ? href : new URL(href, 'http://localhost')
  const params = url.searchParams
  const requestedRunId = params.get('run')
  const catalogRunId = parseCatalogRunId(requestedRunId)
  if (catalogRunId) {
    return snapshot({
      kind: 'run',
      runSurface: 'detail',
      activeSource: 'catalog',
      catalogRunId,
      runDetailPanel: runDetailPanel(params),
    })
  }

  // A malformed explicit Run must never fall through to an unrelated demo.
  if (requestedRunId !== null) return snapshot({ requiresCanonicalization: true })

  const fixture = params.get('fixture')
  if (fixture === 'positive' || fixture === 'negative' || fixture === 'invalid') {
    return snapshot({
      kind: 'demo',
      runSurface: fixture === 'invalid' ? 'catalog' : 'detail',
      activeSource: fixture,
      demoFixture: fixture,
      runDetailPanel: fixture === 'invalid' ? null : runDetailPanel(params),
    })
  }
  if (fixture === 'local') {
    return snapshot({
      kind: 'local',
      runSurface: 'detail',
      activeSource: 'local',
      runDetailPanel: runDetailPanel(params),
    })
  }
  if (fixture === 'comparison') {
    return snapshot({
      kind: 'comparison',
      publicView: 'comparison',
      activeSource: 'comparison',
      analysisView: 'comparison',
      comparisonPanel: comparisonPanel(params),
      comparisonSample: params.get('sample') === 'drift' ? 'drift' : null,
    })
  }
  if (fixture === 'pairing') {
    return snapshot({
      kind: 'pairing',
      publicView: 'pairing',
      activeSource: 'pairing',
      analysisView: 'pairing',
      pairingPanel: pairingPanel(params),
      pairingSample: params.get('sample') === 'supported' ? 'supported' : null,
    })
  }
  if (fixture === 'batch') {
    return snapshot({
      kind: 'batch',
      publicView: 'batch',
      activeSource: 'batch',
      analysisView: 'batch',
      batchSample: params.get('sample') === 'supported' ? 'supported' : null,
    })
  }

  // Unknown fixtures and views are intentionally fail-closed to Catalog.
  if (fixture !== null) return snapshot({ requiresCanonicalization: true })

  const view = params.get('view')
  if (view === 'comparison' || view === 'pairing' || view === 'batch') {
    return snapshot({
      kind: 'analysis-view',
      publicView: view,
      activeSource: view,
      analysisView: view,
    })
  }
  if (view !== null && view !== 'runs') {
    return snapshot({ requiresCanonicalization: true })
  }
  return snapshot({})
}

export function buildWorkbenchUrl(currentHref: string | URL, target: WorkbenchRouteTarget): URL {
  const url = currentHref instanceof URL ? new URL(currentHref) : new URL(currentHref, 'http://localhost')
  for (const key of MANAGED_QUERY_KEYS) url.searchParams.delete(key)

  if (target.kind === 'view') {
    url.searchParams.set('view', target.view)
  } else if (target.kind === 'demo') {
    url.searchParams.set('fixture', target.fixture)
    if (target.panel) url.searchParams.set('panel', target.panel)
  } else if (target.kind === 'local') {
    url.searchParams.set('fixture', 'local')
    if (target.panel) url.searchParams.set('panel', target.panel)
  } else if (target.kind === 'run') {
    url.searchParams.set('run', target.catalogRunId)
    if (target.panel) url.searchParams.set('panel', target.panel)
  } else if (target.kind === 'comparison') {
    url.searchParams.set('fixture', 'comparison')
    if (target.sample) url.searchParams.set('sample', target.sample)
    if (target.panel) url.searchParams.set('panel', target.panel)
  } else if (target.kind === 'pairing') {
    url.searchParams.set('fixture', 'pairing')
    if (target.sample) url.searchParams.set('sample', target.sample)
    if (target.panel) url.searchParams.set('panel', target.panel)
  } else if (target.kind === 'batch') {
    url.searchParams.set('fixture', 'batch')
    if (target.sample) url.searchParams.set('sample', target.sample)
  }

  return url
}

export function historyStateForRoute(target: WorkbenchRouteTarget): Record<string, string> {
  if (target.kind === 'view') return { view: target.view }
  if (target.kind === 'demo') {
    return target.panel
      ? { fixture: target.fixture, panel: target.panel }
      : { fixture: target.fixture }
  }
  if (target.kind === 'local') {
    return target.panel
      ? { fixture: 'local', panel: target.panel }
      : { fixture: 'local' }
  }
  if (target.kind === 'run') {
    return target.panel
      ? { run: target.catalogRunId, panel: target.panel }
      : { run: target.catalogRunId }
  }
  if (target.kind === 'comparison' || target.kind === 'pairing') {
    const state: Record<string, string> = { fixture: target.kind }
    if (target.sample) state.sample = target.sample
    if (target.panel) state.panel = target.panel
    return state
  }
  if (target.kind === 'batch') {
    return target.sample
      ? { fixture: 'batch', sample: target.sample }
      : { fixture: 'batch' }
  }
  return {}
}
