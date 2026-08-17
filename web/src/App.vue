<script setup lang="ts">
import { computed, nextTick, onBeforeUnmount, onMounted, ref, shallowRef } from 'vue'
import BatchAnalysisView from './components/BatchAnalysisView.vue'
import BatchEntryState from './components/BatchEntryState.vue'
import BrowserEvidence from './components/BrowserEvidence.vue'
import ComparisonEntryState from './components/ComparisonEntryState.vue'
import ComparisonView from './components/ComparisonView.vue'
import CrossAxisNavigation from './components/CrossAxisNavigation.vue'
import PairedAnalysisView from './components/PairedAnalysisView.vue'
import PairingEntryState from './components/PairingEntryState.vue'
import RunCatalog from './components/RunCatalog.vue'
import RunBoundary from './components/RunBoundary.vue'
import RunAssertions from './components/RunAssertions.vue'
import RunEvidenceLedger from './components/RunEvidenceLedger.vue'
import RunErrorState from './components/RunErrorState.vue'
import RunOverview from './components/RunOverview.vue'
import SectionFrame from './components/SectionFrame.vue'
import StatusBadge from './components/StatusBadge.vue'
import {
  browserEvidence,
  BundleLoadError,
  loadDemoBundle,
  loadLocalBundle,
  loadSameOriginBundle,
  type DemoBundleId,
} from './domain/bundle'
import {
  CatalogLoadError,
  fetchCatalog,
} from './domain/catalog'
import { BatchLoadError, loadLocalBatchAnalysis } from './domain/batch'
import {
  ComparisonLoadError,
  loadComparisonReviewSample,
  loadLocalComparison,
} from './domain/comparison'
import {
  loadLocalPairedAnalysis,
  loadPairedAnalysisReviewSample,
  PairingLoadError,
} from './domain/pairing'
import {
  type ActiveSource,
  type ComparisonPanel,
  type PairingPanel,
  type PublicView,
  type RunDetailPanel,
  type RunSurface,
  type WorkbenchRouteTarget,
} from './domain/workbenchRoute'
import { createWorkbenchHistory } from './navigation/workbenchHistory'
import type {
  CatalogResponse,
  CatalogRunSummary,
  LoadedBatchAnalysis,
  LoadedBundle,
  LoadedComparison,
  LoadedPairedAnalysis,
} from './domain/types'

const workbenchHistory = createWorkbenchHistory()
const initialRoute = workbenchHistory.current()
const bundle = shallowRef<LoadedBundle | null>(null)
const comparison = shallowRef<LoadedComparison | null>(null)
const pairedAnalysis = shallowRef<LoadedPairedAnalysis | null>(null)
const batchAnalysis = shallowRef<LoadedBatchAnalysis | null>(null)
const loading = ref(true)
const error = ref<{ code: string; message: string } | null>(null)
const activeSource = ref<ActiveSource>(initialRoute.activeSource)
const publicView = ref<PublicView>(initialRoute.publicView)
const runSurface = ref<RunSurface>(initialRoute.runSurface)
const liveMessage = ref('正在读取正向证据包。')
const catalog = shallowRef<CatalogResponse | null>(null)
const catalogLoading = ref(true)
const catalogError = ref<{ code: string; message: string } | null>(null)
const selectedCatalogRunId = ref<string | null>(initialRoute.catalogRunId)
const runDetailPanel = ref<RunDetailPanel | null>(initialRoute.runDetailPanel)
const pairingPanel = ref<PairingPanel | null>(initialRoute.pairingPanel)
const comparisonPanel = ref<ComparisonPanel | null>(initialRoute.comparisonPanel)
let lastCatalogTriggerId: string | null = null
let loadSequence = 0
let pendingPointerClickCleanup: (() => void) | null = null
let unsubscribeHistory: (() => void) | null = null
let appMounted = false

const report = computed(() => bundle.value?.report ?? null)
const browserSession = computed(() => (bundle.value ? browserEvidence(bundle.value) : null))
const runLocationLabel = computed(() => {
  if (report.value) return report.value.run_id
  if (selectedCatalogRunId.value) return selectedCatalogRunId.value
  if (activeSource.value === 'local') return '本地证据包'
  if (activeSource.value === 'positive' || activeSource.value === 'negative' || activeSource.value === 'invalid') {
    return sourceLabel(activeSource.value)
  }
  return '正在核验'
})
const isRunDetail = computed(
  () => publicView.value === 'runs' && runSurface.value === 'detail',
)

function currentRoute() {
  return workbenchHistory.current()
}

function pushRoute(target: WorkbenchRouteTarget) {
  workbenchHistory.push(target)
}

function runDetailPanelLabel(panel: RunDetailPanel): string {
  if (panel === 'browser') return '浏览器事实'
  if (panel === 'assertions') return '确定性断言'
  return '证据账册'
}

function runDetailRouteTarget(panel: RunDetailPanel | null): WorkbenchRouteTarget | null {
  const route = currentRoute()
  if (route.kind === 'run' && route.catalogRunId) {
    return { kind: 'run', catalogRunId: route.catalogRunId, panel }
  }
  if (
    route.kind === 'demo' &&
    (route.demoFixture === 'positive' || route.demoFixture === 'negative')
  ) {
    return { kind: 'demo', fixture: route.demoFixture, panel }
  }
  if (route.kind === 'local') return { kind: 'local', panel }
  return null
}

function pairingPanelLabel(panel: PairingPanel): string {
  return panel === 'sources' ? '四角色来源账册' : '预注册断言全貌'
}

function openComparisonPanel(panel: ComparisonPanel) {
  comparisonPanel.value = panel
  const sample = currentRoute().comparisonSample
  pushRoute({ kind: 'comparison', panel, sample })
  liveMessage.value = '已进入完整语义差异账册。'
  void nextTick(() => {
    document.getElementById('view-comparison-title')?.focus()
    document.documentElement.scrollTop = 0
    document.body.scrollTop = 0
  })
}

function closeComparisonPanel() {
  const panel = comparisonPanel.value
  comparisonPanel.value = null
  const sample = currentRoute().comparisonSample
  pushRoute({ kind: 'comparison', sample })
  liveMessage.value = '已返回复跑比较总览。'
  void nextTick(() => {
    if (panel) document.querySelector<HTMLElement>(`[data-open-comparison-panel="${panel}"]`)?.focus()
  })
}

function openPairingPanel(panel: PairingPanel) {
  pairingPanel.value = panel
  const sample = currentRoute().pairingSample
  pushRoute({ kind: 'pairing', panel, sample })
  liveMessage.value = `已进入${pairingPanelLabel(panel)}。`
  void nextTick(() => {
    document.getElementById('paired-title')?.focus()
    document.documentElement.scrollTop = 0
    document.body.scrollTop = 0
  })
}

function closePairingPanel() {
  const panel = pairingPanel.value
  pairingPanel.value = null
  const sample = currentRoute().pairingSample
  pushRoute({ kind: 'pairing', sample })
  liveMessage.value = '已返回配对实验总览。'
  void nextTick(() => {
    if (panel) document.querySelector<HTMLElement>(`[data-open-pairing-panel="${panel}"]`)?.focus()
  })
}

function openRunDetailPanel(panel: RunDetailPanel) {
  const target = runDetailRouteTarget(panel)
  if (!target) return
  runDetailPanel.value = panel
  pushRoute(target)
  liveMessage.value = `已进入${runDetailPanelLabel(panel)}完整视图。`
  void nextTick(() => {
    document.getElementById('run-detail-panel-title')?.focus()
    document.documentElement.scrollTop = 0
    document.body.scrollTop = 0
  })
}

function closeRunDetailPanel() {
  const panel = runDetailPanel.value
  const target = runDetailRouteTarget(null)
  if (!target) return
  runDetailPanel.value = null
  pushRoute(target)
  liveMessage.value = '已返回 Run 详情总览。'
  void nextTick(() => {
    if (panel) document.querySelector<HTMLElement>(`[data-open-run-panel="${panel}"]`)?.focus()
  })
}

function clearLoadedAnalysis() {
  comparison.value = null
  pairedAnalysis.value = null
  batchAnalysis.value = null
}

function resetPublicView(view: PublicView) {
  ++loadSequence
  releaseCurrentBundle()
  clearLoadedAnalysis()
  publicView.value = view
  runSurface.value = 'catalog'
  activeSource.value = view === 'runs' ? 'catalog' : view
  selectedCatalogRunId.value = null
  runDetailPanel.value = null
  pairingPanel.value = null
  comparisonPanel.value = null
  loading.value = false
  error.value = null
  catalogError.value = null
  liveMessage.value = view === 'runs'
    ? '本地 Run 目录已加载，请选择一项 Run。'
    : `已进入${publicViewLabel(view)}，请选择本地分析文件。`
}

function publicViewLabel(view: PublicView): string {
  if (view === 'runs') return 'Runs / Catalog'
  if (view === 'comparison') return 'Rerun Comparison'
  if (view === 'pairing') return 'Paired Analysis'
  return 'Batch Analysis'
}

function focusPublicViewTitle(view: PublicView) {
  void nextTick(() => {
    document.getElementById(`view-${view}-title`)?.focus()
  })
}

function selectPublicView(view: PublicView) {
  if (view === 'runs' && isRunDetail.value) {
    returnToCatalog()
    return
  }
  if (publicView.value !== view) {
    pushRoute({ kind: 'view', view })
    resetPublicView(view)
  }
  focusPublicViewTitle(view)
}

function releaseCurrentBundle() {
  bundle.value?.release()
  bundle.value = null
}

function describeError(cause: unknown) {
  if (cause instanceof BundleLoadError) return { code: cause.code, message: cause.message }
  return { code: 'UNEXPECTED', message: '工作台无法读取该证据包，请返回有效夹具重试。' }
}

function describeCatalogError(cause: unknown) {
  if (cause instanceof CatalogLoadError || cause instanceof BundleLoadError) {
    return { code: cause.code, message: cause.message }
  }
  return { code: 'CATALOG_UNEXPECTED', message: '本地 Run 目录暂时无法读取。' }
}

function describeComparisonError(cause: unknown) {
  if (cause instanceof ComparisonLoadError) return { code: cause.code, message: cause.message }
  return { code: 'COMPARISON_UNEXPECTED', message: '工作台无法核验该复跑比较包。' }
}

function describePairingError(cause: unknown) {
  if (cause instanceof PairingLoadError) return { code: cause.code, message: cause.message }
  return { code: 'PAIRING_UNEXPECTED', message: '工作台无法核验该四角色配对分析包。' }
}

function describeBatchError(cause: unknown) {
  if (cause instanceof BatchLoadError) return { code: cause.code, message: cause.message }
  return { code: 'BATCH_UNEXPECTED', message: '工作台无法核验该全因子批次分析包。' }
}

type StateCourtKind = 'invalid' | 'operational' | 'privacy'

function stateCourtKind(code: string): StateCourtKind {
  if (code.endsWith('_RESELECT_REQUIRED')) return 'privacy'
  if (['RUN_NOT_FOUND', 'BUNDLE_UNAVAILABLE', 'CATALOG_API_UNAVAILABLE', 'CATALOG_UNEXPECTED'].includes(code)) {
    return 'operational'
  }
  return 'invalid'
}

async function refreshCatalog() {
  catalogLoading.value = true
  catalogError.value = null
  try {
    catalog.value = await fetchCatalog()
  } catch (cause) {
    catalog.value = null
    catalogError.value = describeCatalogError(cause)
  } finally {
    catalogLoading.value = false
  }
}

async function selectDemo(
  id: DemoBundleId,
  pushHistory = true,
  panel: RunDetailPanel | null = null,
): Promise<boolean> {
  const sequence = ++loadSequence
  loading.value = true
  error.value = null
  activeSource.value = id
  publicView.value = 'runs'
  runSurface.value = id === 'invalid' ? 'catalog' : 'detail'
  selectedCatalogRunId.value = null
  runDetailPanel.value = id === 'invalid' ? null : panel
  clearLoadedAnalysis()
  liveMessage.value = `正在读取${sourceLabel(id)}。`
  if (pushHistory) {
    pushRoute({ kind: 'demo', fixture: id, panel: runDetailPanel.value })
  }
  releaseCurrentBundle()
  try {
    const loaded = await loadDemoBundle(id)
    if (sequence !== loadSequence) {
      loaded.release()
      return false
    }
    bundle.value = loaded
    liveMessage.value = `${sourceLabel(id)}已加载，完整性核验通过。`
    return true
  } catch (cause) {
    if (sequence !== loadSequence) return false
    error.value = describeError(cause)
    liveMessage.value = `证据包读取失败：${error.value.message}`
    return true
  } finally {
    if (sequence === loadSequence) loading.value = false
  }
}

function dismissRunError(restoreFocus = false) {
  ++loadSequence
  loading.value = false
  error.value = null
  activeSource.value = 'catalog'
  publicView.value = 'runs'
  runSurface.value = 'catalog'
  releaseCurrentBundle()
  pushRoute({ kind: 'view', view: 'runs' })
  liveMessage.value = '已收起损坏证据提示，返回本地 Run 目录。'
  if (restoreFocus) {
    void nextTick(() => document.querySelector<HTMLElement>('[data-testid="fixture-invalid"]')?.focus())
  }
}

function toggleInvalidDemo() {
  if (activeSource.value === 'invalid' && (loading.value || error.value)) {
    dismissRunError()
    return
  }
  void selectDemo('invalid')
}

async function importLocal(event: Event) {
  const input = event.currentTarget as HTMLInputElement
  if (!input.files?.length) return
  const sequence = ++loadSequence
  loading.value = true
  error.value = null
  activeSource.value = 'local'
  publicView.value = 'runs'
  runSurface.value = 'detail'
  selectedCatalogRunId.value = null
  clearLoadedAnalysis()
  liveMessage.value = '正在本地内存中核验所选证据包。'
  pushRoute({ kind: 'local' })
  releaseCurrentBundle()
  try {
    const loaded = await loadLocalBundle(input.files)
    if (sequence !== loadSequence) {
      loaded.release()
      return
    }
    bundle.value = loaded
    liveMessage.value = '本地证据包已加载；文件未上传。'
  } catch (cause) {
    if (sequence !== loadSequence) return
    error.value = describeError(cause)
    liveMessage.value = `本地证据包读取失败：${error.value.message}`
  } finally {
    input.value = ''
    if (sequence === loadSequence) loading.value = false
  }
}

function beginAnalysisLoad(view: Exclude<PublicView, 'runs'>): number {
  const sequence = ++loadSequence
  loading.value = true
  error.value = null
  activeSource.value = view
  publicView.value = view
  runSurface.value = 'catalog'
  selectedCatalogRunId.value = null
  runDetailPanel.value = null
  comparisonPanel.value = null
  pairingPanel.value = null
  releaseCurrentBundle()
  clearLoadedAnalysis()
  return sequence
}

async function importComparison(event: Event) {
  const input = event.currentTarget as HTMLInputElement
  if (!input.files?.length) return
  const sequence = beginAnalysisLoad('comparison')
  liveMessage.value = '正在本地内存中核验复跑 Comparison Manifest。'
  pushRoute({ kind: 'comparison' })
  try {
    const loaded = await loadLocalComparison(input.files)
    if (sequence !== loadSequence) return
    comparison.value = loaded
    liveMessage.value = `复跑比较 ${loaded.comparison.comparison_status} 已加载；文件未上传。`
  } catch (cause) {
    if (sequence !== loadSequence) return
    error.value = describeComparisonError(cause)
    liveMessage.value = `复跑比较包读取失败：${error.value.message}`
  } finally {
    input.value = ''
    if (sequence === loadSequence) loading.value = false
  }
}

async function importPairedAnalysis(event: Event) {
  const input = event.currentTarget as HTMLInputElement
  if (!input.files?.length) return
  const sequence = beginAnalysisLoad('pairing')
  liveMessage.value = '正在本地内存中核验 PairedAnalysis Manifest 与 PairingPlan seal。'
  pushRoute({ kind: 'pairing' })
  try {
    const loaded = await loadLocalPairedAnalysis(input.files)
    if (sequence !== loadSequence) return
    pairedAnalysis.value = loaded
    liveMessage.value = `配对分析 ${loaded.analysis.analysis_status} 已加载；文件未上传。`
  } catch (cause) {
    if (sequence !== loadSequence) return
    error.value = describePairingError(cause)
    liveMessage.value = `配对分析包读取失败：${error.value.message}`
  } finally {
    input.value = ''
    if (sequence === loadSequence) loading.value = false
  }
}

async function openComparisonReviewSample(): Promise<boolean> {
  const sequence = beginAnalysisLoad('comparison')
  liveMessage.value = '正在核验内置复跑比较审阅数据。'
  try {
    const loaded = await loadComparisonReviewSample()
    if (sequence !== loadSequence) return false
    comparison.value = loaded
    liveMessage.value = `复跑比较 ${loaded.comparison.comparison_status} 审阅数据已加载。`
    return true
  } catch (cause) {
    if (sequence !== loadSequence) return false
    error.value = describeComparisonError(cause)
    liveMessage.value = `复跑比较审阅数据读取失败：${error.value.message}`
    return true
  } finally {
    if (sequence === loadSequence) loading.value = false
  }
}

async function openPairingReviewSample(): Promise<boolean> {
  const sequence = beginAnalysisLoad('pairing')
  liveMessage.value = '正在核验内置四角色配对审阅数据。'
  try {
    const loaded = await loadPairedAnalysisReviewSample()
    if (sequence !== loadSequence) return false
    pairedAnalysis.value = loaded
    liveMessage.value = `配对分析 ${loaded.analysis.analysis_status} 审阅数据已加载。`
    return true
  } catch (cause) {
    if (sequence !== loadSequence) return false
    error.value = describePairingError(cause)
    liveMessage.value = `配对分析审阅数据读取失败：${error.value.message}`
    return true
  } finally {
    if (sequence === loadSequence) loading.value = false
  }
}

async function importBatchAnalysis(event: Event) {
  const input = event.currentTarget as HTMLInputElement
  if (!input.files?.length) return
  const sequence = beginAnalysisLoad('batch')
  liveMessage.value = '正在本地内存中核验 BatchAnalysis Manifest、BatchPlan seal 与完整矩阵。'
  pushRoute({ kind: 'batch' })
  try {
    const loaded = await loadLocalBatchAnalysis(input.files)
    if (sequence !== loadSequence) return
    batchAnalysis.value = loaded
    liveMessage.value = `批次分析 ${loaded.analysis.coverage_status} / ${loaded.analysis.hypothesis_status} 已加载；文件未上传。`
  } catch (cause) {
    if (sequence !== loadSequence) return
    error.value = describeBatchError(cause)
    liveMessage.value = `批次分析包读取失败：${error.value.message}`
  } finally {
    input.value = ''
    if (sequence === loadSequence) loading.value = false
  }
}

async function selectCatalogRun(
  run: CatalogRunSummary,
  trigger?: HTMLElement,
  pushHistory = true,
): Promise<boolean> {
  const sequence = ++loadSequence
  loading.value = true
  error.value = null
  catalogError.value = null
  activeSource.value = 'catalog'
  publicView.value = 'runs'
  runSurface.value = 'detail'
  selectedCatalogRunId.value = run.catalog_run_id
  runDetailPanel.value = null
  clearLoadedAnalysis()
  lastCatalogTriggerId = trigger ? run.catalog_run_id : lastCatalogTriggerId
  liveMessage.value = `正在从只读目录核验 ${run.run_id}。`
  if (pushHistory) {
    pushRoute({ kind: 'run', catalogRunId: run.catalog_run_id })
  }
  releaseCurrentBundle()
  try {
    const loaded = await loadSameOriginBundle(
      run.bundle.base_url,
      `本地目录 · ${run.run_id}`,
      true,
    )
    if (
      loaded.report.run_id !== run.run_id ||
      loaded.report.execution_status !== run.execution_status ||
      loaded.report.verdict !== run.verdict ||
      loaded.report.plan.id !== run.plan.id ||
      loaded.report.plan.version !== run.plan.version ||
      loaded.report.plan.sha256 !== run.plan.sha256
    ) {
      loaded.release()
      throw new BundleLoadError('CATALOG_SUMMARY_MISMATCH', '目录摘要与完整 Bundle 校验结果不一致。')
    }
    if (sequence !== loadSequence) {
      loaded.release()
      return false
    }
    bundle.value = loaded
    liveMessage.value = `${run.run_id} 已从目录加载，完整性核验通过。`
    if (trigger) {
      void nextTick(() => {
        document.documentElement.scrollTop = 0
        document.body.scrollTop = 0
        document.getElementById('run-detail-title')?.focus()
      })
    }
    return true
  } catch (cause) {
    if (sequence !== loadSequence) return false
    const described = describeCatalogError(cause)
    error.value = described
    liveMessage.value = `目录 Run 读取失败：${described.message}`
    return true
  } finally {
    if (sequence === loadSequence) loading.value = false
  }
}

async function retryCatalog() {
  const selected = selectedCatalogRunId.value
  await refreshCatalog()
  if (!appMounted) return
  const route = currentRoute()
  if (selected && catalog.value && route.kind === 'run' && route.catalogRunId === selected) {
    onHistoryChange()
  }
}

function returnToCatalog() {
  if (!isRunDetail.value) return
  ++loadSequence
  releaseCurrentBundle()
  clearLoadedAnalysis()
  loading.value = false
  error.value = null
  if (catalog.value) catalogError.value = null
  activeSource.value = 'catalog'
  publicView.value = 'runs'
  runSurface.value = 'catalog'
  const runId = selectedCatalogRunId.value ?? lastCatalogTriggerId
  selectedCatalogRunId.value = null
  runDetailPanel.value = null
  pushRoute({ kind: 'catalog' })
  liveMessage.value = '已返回本地 Run 目录。'
  void nextTick(() => {
    document.documentElement.scrollTop = 0
    document.body.scrollTop = 0
    if (!runId) return
    document.querySelector<HTMLElement>(`[data-catalog-run-id="${runId}"]`)?.focus({ preventScroll: true })
  })
}

function isPrimaryActivationPointer(event: PointerEvent): boolean {
  return event.isPrimary !== false && (event.pointerType !== 'mouse' || event.button === 0)
}

function suppressNextPointerClick() {
  pendingPointerClickCleanup?.()
  let timeoutId: number | undefined
  const cleanup = () => {
    document.removeEventListener('click', consumePointerClick, true)
    if (timeoutId !== undefined) window.clearTimeout(timeoutId)
    if (pendingPointerClickCleanup === cleanup) pendingPointerClickCleanup = null
  }
  const consumePointerClick = (event: MouseEvent) => {
    // Keyboard activation emits a click with detail 0 and must retain the
    // native click fallback. A pointer click can otherwise land on the newly
    // rendered Catalog after pointerdown removes the source control.
    if (event.detail === 0) return
    event.preventDefault()
    event.stopImmediatePropagation()
    cleanup()
  }
  document.addEventListener('click', consumePointerClick, true)
  timeoutId = window.setTimeout(cleanup, 800)
  pendingPointerClickCleanup = cleanup
}

function returnToCatalogOnPrimaryPointer(event: PointerEvent) {
  if (!isPrimaryActivationPointer(event)) return
  suppressNextPointerClick()
  returnToCatalog()
}

function goToCatalogHome() {
  if (isRunDetail.value) {
    returnToCatalog()
    return
  }
  if (publicView.value !== 'runs') {
    selectPublicView('runs')
    void nextTick(() => {
      document.documentElement.scrollTop = 0
      document.body.scrollTop = 0
    })
    return
  }
  const route = currentRoute()
  if (route.kind === 'demo' && route.demoFixture === 'invalid') {
    dismissRunError()
    return
  }
  if (route.requiresCanonicalization) {
    pushRoute({ kind: 'catalog' })
    applyCatalogFromHistory(false)
  }
  document.documentElement.scrollTop = 0
  document.body.scrollTop = 0
  liveMessage.value = '已回到本地 Run 目录。'
  focusPublicViewTitle('runs')
}

function goToCatalogHomeOnPrimaryPointer(event: PointerEvent) {
  if (!isPrimaryActivationPointer(event)) return
  suppressNextPointerClick()
  goToCatalogHome()
}

function sourceLabel(id: DemoBundleId): string {
  if (id === 'positive') return '正向证据'
  if (id === 'negative') return '负向证据'
  return '损坏证据'
}

function applyRunPanelFromHistory(requestedPanel: RunDetailPanel | null, focusTarget: boolean) {
  const previousPanel = runDetailPanel.value
  runDetailPanel.value = requestedPanel
  if (!focusTarget) return
  void nextTick(() => {
    if (requestedPanel) {
      document.getElementById('run-detail-panel-title')?.focus()
    } else if (previousPanel) {
      document.querySelector<HTMLElement>(`[data-open-run-panel="${previousPanel}"]`)?.focus()
    } else {
      document.getElementById('run-detail-title')?.focus()
    }
  })
}

function applyCatalogFromHistory(focusTarget: boolean) {
  const previousRunId = selectedCatalogRunId.value ?? lastCatalogTriggerId
  ++loadSequence
  releaseCurrentBundle()
  clearLoadedAnalysis()
  activeSource.value = 'catalog'
  publicView.value = 'runs'
  runSurface.value = 'catalog'
  selectedCatalogRunId.value = null
  runDetailPanel.value = null
  loading.value = false
  error.value = null
  if (catalog.value) catalogError.value = null
  liveMessage.value = '本地 Run 目录已加载，请选择一项 Run。'
  if (!focusTarget) return
  void nextTick(() => {
    const row = previousRunId
      ? document.querySelector<HTMLElement>(`[data-catalog-run-id="${previousRunId}"]`)
      : null
    if (row) row.focus()
    else document.getElementById('view-runs-title')?.focus()
  })
}

function onHistoryChange(focusTarget = false) {
  const route = currentRoute()

  if (route.kind === 'analysis-view' && route.analysisView) {
    resetPublicView(route.analysisView)
    if (focusTarget) focusPublicViewTitle(route.analysisView)
    return
  }

  if (route.kind === 'run' && route.catalogRunId) {
    const catalogRunId = route.catalogRunId
    const requestedPanel = route.runDetailPanel
    if (selectedCatalogRunId.value === catalogRunId && bundle.value) {
      applyRunPanelFromHistory(requestedPanel, focusTarget)
      return
    }
    runDetailPanel.value = requestedPanel
    const run = catalog.value?.runs.find((candidate) => candidate.catalog_run_id === catalogRunId)
    if (run) {
      void selectCatalogRun(run, undefined, false).then((committed) => {
        if (!committed) return
        const current = currentRoute()
        if (
          current.kind !== 'run' ||
          current.catalogRunId !== catalogRunId ||
          current.runDetailPanel !== requestedPanel ||
          selectedCatalogRunId.value !== catalogRunId ||
          !bundle.value
        ) return
        runDetailPanel.value = requestedPanel
        if (focusTarget) {
          void nextTick(() => {
            if (requestedPanel) document.getElementById('run-detail-panel-title')?.focus()
            else document.getElementById('run-detail-title')?.focus()
          })
        }
      })
      return
    }
    if (catalogLoading.value && !catalog.value) {
      ++loadSequence
      releaseCurrentBundle()
      clearLoadedAnalysis()
      activeSource.value = 'catalog'
      publicView.value = 'runs'
      runSurface.value = 'detail'
      selectedCatalogRunId.value = catalogRunId
      loading.value = true
      error.value = null
      liveMessage.value = `正在从本地 Run 目录读取 ${catalogRunId}。`
      return
    }
    ++loadSequence
    releaseCurrentBundle()
    clearLoadedAnalysis()
    activeSource.value = 'catalog'
    publicView.value = 'runs'
    runSurface.value = 'detail'
    selectedCatalogRunId.value = catalogRunId
    loading.value = false
    error.value = {
      code: 'RUN_NOT_FOUND',
      message: 'URL 中的 Catalog Run 不存在，请返回目录重新选择。',
    }
    liveMessage.value = error.value.message
    return
  }

  if (route.kind === 'catalog') {
    applyCatalogFromHistory(focusTarget)
    return
  }

  if (route.kind === 'comparison') {
    if (comparison.value) {
      const requestedPanel = route.comparisonPanel
      const previousPanel = comparisonPanel.value
      comparisonPanel.value = requestedPanel
      if (focusTarget) {
        void nextTick(() => {
          if (requestedPanel) document.getElementById('view-comparison-title')?.focus()
          else if (previousPanel) document.querySelector<HTMLElement>(`[data-open-comparison-panel="${previousPanel}"]`)?.focus()
          else document.getElementById('view-comparison-title')?.focus()
        })
      }
      return
    }
    if (route.comparisonSample === 'drift') {
      void openComparisonReviewSample().then((committed) => {
        if (!committed) return
        const current = currentRoute()
        if (
          current.kind !== 'comparison' ||
          current.comparisonSample !== 'drift' ||
          current.comparisonPanel !== route.comparisonPanel ||
          !comparison.value
        ) return
        comparisonPanel.value = route.comparisonPanel
        if (focusTarget) focusPublicViewTitle('comparison')
      })
      return
    }
    ++loadSequence
    releaseCurrentBundle()
    clearLoadedAnalysis()
    activeSource.value = 'comparison'
    publicView.value = 'comparison'
    loading.value = false
    error.value = {
      code: 'COMPARISON_RESELECT_REQUIRED',
      message: '为保护隐私，本地比较包不会持久化；请重新选择 Comparison 目录。',
    }
    liveMessage.value = error.value.message
    if (focusTarget) focusPublicViewTitle('comparison')
    return
  }

  if (route.kind === 'pairing') {
    if (pairedAnalysis.value) {
      const requestedPanel = route.pairingPanel
      const previousPanel = pairingPanel.value
      pairingPanel.value = requestedPanel
      if (focusTarget) {
        void nextTick(() => {
          if (requestedPanel) document.getElementById('paired-title')?.focus()
          else if (previousPanel) document.querySelector<HTMLElement>(`[data-open-pairing-panel="${previousPanel}"]`)?.focus()
          else document.getElementById('paired-title')?.focus()
        })
      }
      return
    }
    if (route.pairingSample === 'supported') {
      void openPairingReviewSample().then((committed) => {
        if (!committed) return
        const current = currentRoute()
        if (
          current.kind !== 'pairing' ||
          current.pairingSample !== 'supported' ||
          current.pairingPanel !== route.pairingPanel ||
          !pairedAnalysis.value
        ) return
        pairingPanel.value = route.pairingPanel
        if (focusTarget) focusPublicViewTitle('pairing')
      })
      return
    }
    ++loadSequence
    releaseCurrentBundle()
    clearLoadedAnalysis()
    activeSource.value = 'pairing'
    publicView.value = 'pairing'
    loading.value = false
    error.value = {
      code: 'PAIRING_RESELECT_REQUIRED',
      message: '为保护隐私，本地配对包不会持久化；请重新选择 PairedAnalysis 目录。',
    }
    liveMessage.value = error.value.message
    if (focusTarget) focusPublicViewTitle('pairing')
    return
  }

  if (route.kind === 'batch') {
    ++loadSequence
    releaseCurrentBundle()
    clearLoadedAnalysis()
    activeSource.value = 'batch'
    publicView.value = 'batch'
    loading.value = false
    error.value = {
      code: 'BATCH_RESELECT_REQUIRED',
      message: '为保护隐私，本地批次包不会持久化；请重新选择 BatchAnalysis 四个文件。',
    }
    liveMessage.value = error.value.message
    if (focusTarget) focusPublicViewTitle('batch')
    return
  }

  if (route.kind === 'local') {
    if (activeSource.value === 'local' && bundle.value) {
      applyRunPanelFromHistory(route.runDetailPanel, focusTarget)
      return
    }
    ++loadSequence
    releaseCurrentBundle()
    clearLoadedAnalysis()
    activeSource.value = 'local'
    publicView.value = 'runs'
    runSurface.value = 'detail'
    runDetailPanel.value = route.runDetailPanel
    loading.value = false
    error.value = {
      code: 'LOCAL_RESELECT_REQUIRED',
      message: '为保护隐私，本地目录不会持久化；请重新选择目录或返回内置夹具。',
    }
    liveMessage.value = error.value.message
    if (focusTarget) focusPublicViewTitle('runs')
    return
  }

  if (route.kind === 'demo' && route.demoFixture) {
    if (activeSource.value === route.demoFixture && bundle.value) {
      applyRunPanelFromHistory(route.runDetailPanel, focusTarget)
      return
    }
    const requestedFixture = route.demoFixture
    const requestedPanel = route.runDetailPanel
    void selectDemo(requestedFixture, false, requestedPanel).then((committed) => {
      if (!committed) return
      const current = currentRoute()
      if (
        current.kind !== 'demo' ||
        current.demoFixture !== requestedFixture ||
        current.runDetailPanel !== requestedPanel ||
        activeSource.value !== requestedFixture ||
        (requestedFixture === 'invalid' ? !error.value : !bundle.value)
      ) return
      if (focusTarget) {
        if (requestedPanel) {
          void nextTick(() => document.getElementById('run-detail-panel-title')?.focus())
        } else {
          focusPublicViewTitle('runs')
        }
      }
    })
    return
  }

  applyCatalogFromHistory(focusTarget)
}

function onPopState() {
  onHistoryChange(true)
}

function shortHash(value: string): string {
  return `${value.slice(0, 12)}…${value.slice(-8)}`
}

function displayDate(value: string): string {
  const date = new Date(value)
  return Number.isNaN(date.valueOf()) ? value : date.toLocaleString('zh-CN', { hour12: false })
}

onMounted(() => {
  appMounted = true
  unsubscribeHistory = workbenchHistory.subscribe(onPopState)
  onHistoryChange()
  void refreshCatalog().then(() => {
    if (appMounted && currentRoute().kind === 'run') onHistoryChange()
  })
})

onBeforeUnmount(() => {
  appMounted = false
  ++loadSequence
  pendingPointerClickCleanup?.()
  unsubscribeHistory?.()
  unsubscribeHistory = null
  releaseCurrentBundle()
})
</script>

<template>
  <div
    :class="[
      'app-shell',
      {
        'app-shell--runs': publicView === 'runs',
        'app-shell--catalog': publicView === 'runs' && !isRunDetail,
        'app-shell--run-detail': isRunDetail,
        'app-shell--pairing': publicView === 'pairing',
        'app-shell--comparison': publicView === 'comparison',
        'app-shell--batch': publicView === 'batch',
        'app-shell--reference-analysis': publicView !== 'runs',
      },
    ]"
  >
    <p class="sr-only app-live-region" aria-live="polite">{{ liveMessage }}</p>

    <header class="masthead">
      <div class="masthead__roofline" aria-hidden="true"><span></span></div>
      <div class="masthead__inner">
        <div class="masthead__primary">
          <div class="brand-lockup">
            <span class="brand-seal" aria-hidden="true">迹</span>
            <div>
              <p>VeriTrail · Palace Evidence</p>
              <h1>验迹证据工作台</h1>
              <span>让每一项结论，都沿证据中轴归位。</span>
            </div>
          </div>
          <aside class="masthead__scope" aria-label="工作台运行边界">
            <span>工作台</span>
            <span>本地证据包</span>
            <span>只读边界</span>
          </aside>
        </div>
      </div>
    </header>

    <div class="court-threshold" aria-hidden="true"><span></span></div>

    <section class="navigation-courtyard">
      <CrossAxisNavigation
        :current-view="publicView"
        @select="selectPublicView"
      />
    </section>

    <main
      id="main-content"
      class="evidence-axis"
      :aria-busy="publicView === 'runs' && loading ? 'true' : undefined"
    >
      <template v-if="publicView === 'runs'">
        <section v-if="!isRunDetail" class="view-introduction view-introduction--runs" aria-labelledby="view-runs-title">
          <div class="view-introduction__heading">
            <p class="eyebrow">Public View · 北向</p>
            <h2 id="view-runs-title" tabindex="-1" data-testid="view-runs-title">Runs / Catalog</h2>
          </div>
          <div class="runs-toolstrip" aria-label="Runs 证据包来源" data-testid="runs-toolstrip">
            <div class="source-switcher" role="group" aria-label="示例证据">
              <span class="source-switcher__label">示例证据</span>
              <button
                type="button"
                :aria-pressed="activeSource === 'positive'"
                :aria-busy="loading && activeSource === 'positive' ? 'true' : undefined"
                data-testid="fixture-positive"
                @click="selectDemo('positive')"
              >
                <img :src="'/textures/r3-command-positive.png'" alt="" aria-hidden="true" />
                <span>正向证据</span>
              </button>
              <button
                type="button"
                :aria-pressed="activeSource === 'negative'"
                :aria-busy="loading && activeSource === 'negative' ? 'true' : undefined"
                data-testid="fixture-negative"
                @click="selectDemo('negative')"
              >
                <img :src="'/textures/r3-command-negative.png'" alt="" aria-hidden="true" />
                <span>负向证据</span>
              </button>
              <button
                type="button"
                :aria-pressed="activeSource === 'invalid'"
                :aria-expanded="activeSource === 'invalid' && Boolean(error)"
                :aria-busy="loading && activeSource === 'invalid' ? 'true' : undefined"
                aria-controls="run-error-state"
                data-testid="fixture-invalid"
                @click="toggleInvalidDemo"
              >
                <img :src="'/textures/r3-command-invalid.png'" alt="" aria-hidden="true" />
                <span>校验损坏包</span>
              </button>
            </div>
            <label
              class="local-import runs-toolstrip__local"
              :class="{ 'is-active': activeSource === 'local' }"
              :aria-busy="loading && activeSource === 'local' ? 'true' : undefined"
            >
              <img :src="'/textures/r3-command-upload.png'" alt="" aria-hidden="true" />
              <span>选择本地证据包</span>
              <input
                type="file"
                multiple
                webkitdirectory
                aria-label="选择本地 VeriTrail 证据包目录"
                data-testid="local-bundle-input"
                @change="importLocal"
              />
            </label>
          </div>
        </section>

      <RunCatalog
        v-if="!isRunDetail && (catalogLoading || catalog || catalogError)"
        :catalog="catalog"
        :loading="catalogLoading"
        :busy="loading"
        :error="catalogError"
        :selected-run-id="selectedCatalogRunId"
        @select="selectCatalogRun"
        @retry="retryCatalog"
      />

      <nav
        v-if="isRunDetail"
        class="run-detail-breadcrumb"
        aria-label="Run 详情路径与分区"
        data-testid="run-detail-breadcrumb"
      >
        <div class="run-detail-breadcrumb__path">
          <button
            type="button"
            :data-testid="report && bundle ? 'catalog-return' : undefined"
            @pointerdown="returnToCatalogOnPrimaryPointer"
            @click="returnToCatalog"
          >
            返回目录
          </button>
          <span aria-hidden="true">/</span>
          <span>Runs</span>
          <span aria-hidden="true">/</span>
          <span>Catalog</span>
          <span aria-hidden="true">/</span>
          <strong :title="runLocationLabel">
            {{ runLocationLabel }}
          </strong>
        </div>
        <div v-if="report && bundle && !runDetailPanel" class="run-detail-breadcrumb__sections" aria-label="详情分区导航">
          <a href="#overview-title">结论总览</a>
          <a href="#assertions-title">确定性断言</a>
          <a href="#ledger-title">证据账册</a>
          <a href="#browser-title">浏览器事实</a>
          <a href="#boundary-title">边界与复现</a>
        </div>
        <div v-else-if="report && bundle && runDetailPanel" class="run-detail-breadcrumb__sections">
          <button type="button" class="run-detail-breadcrumb__back" @click="closeRunDetailPanel">返回详情</button>
          <span aria-hidden="true">/</span>
          <strong>{{ runDetailPanelLabel(runDetailPanel) }}</strong>
        </div>
      </nav>

      <RunErrorState
        v-if="error"
        :error="error"
        :kind="stateCourtKind(error.code)"
        :retry-mode="activeSource === 'catalog' ? 'catalog' : 'positive'"
        :retry-disabled="activeSource === 'catalog' && catalogLoading"
        @dismiss="dismissRunError(true)"
        @retry="activeSource === 'catalog' ? retryCatalog() : selectDemo('positive')"
      />

      <section
        v-else-if="isRunDetail && loading"
        class="run-detail-loading"
        role="status"
        aria-live="polite"
        data-testid="run-detail-loading"
      >
        <div>
          <p class="eyebrow">Evidence Verification · 核验中</p>
          <h2>正在核验证据卷宗</h2>
          <p>{{ liveMessage }}</p>
        </div>
      </section>

      <template v-else-if="report && bundle">
        <section v-if="!runDetailPanel" class="run-detail-header" aria-label="当前 Run 摘要">
          <div class="run-plaque" data-testid="run-summary">
            <div>
              <p>当前证据包</p>
              <strong id="run-detail-title" tabindex="-1">{{ report.run_id }}</strong>
              <span>{{ bundle.sourceLabel }}</span>
            </div>
            <dl>
              <div>
                <dt>Plan</dt>
                <dd>{{ report.plan.id }} · v{{ report.plan.version }}</dd>
              </div>
              <div>
                <dt>Plan SHA-256</dt>
                <dd>
                  <details class="inline-disclosure">
                    <summary aria-label="展开完整 Plan SHA-256"><code>{{ shortHash(report.plan.sha256) }}</code></summary>
                    <code class="inline-disclosure__full">{{ report.plan.sha256 }}</code>
                  </details>
                </dd>
              </div>
              <div>
                <dt>生成时间</dt>
                <dd>{{ displayDate(report.created_at) }}</dd>
              </div>
            </dl>
          </div>

          <div class="status-gate status-gate--detail" data-testid="status-gate">
            <StatusBadge dimension="execution" :value="report.execution_status" />
            <div class="status-gate__axis" aria-hidden="true"><span></span></div>
            <StatusBadge dimension="verdict" :value="report.verdict" />
            <div class="integrity-seal" data-testid="integrity-status">
              <span aria-hidden="true">◇</span>
              <div>
                <small>{{ bundle?.integrity.authorityVerified ? 'Core 裁决' : 'Bundle 字节' }}</small>
                <strong>{{ bundle?.integrity.authorityVerified ? '已核验' : '自报 Verdict' }}</strong>
                <em>{{ bundle?.integrity.verifiedFiles }} 个文件</em>
              </div>
            </div>
          </div>
        </section>

        <RunOverview v-if="!runDetailPanel" :report="report" />

        <section v-if="runDetailPanel" class="run-detail-subview-header" aria-labelledby="run-detail-panel-title">
          <div>
            <p class="eyebrow">Run Detail · 完整账册</p>
            <h2 id="run-detail-panel-title" tabindex="-1">{{ runDetailPanelLabel(runDetailPanel) }}</h2>
          </div>
        </section>

        <RunAssertions
          v-if="!runDetailPanel || runDetailPanel === 'assertions'"
          :report="report"
          :full="runDetailPanel === 'assertions'"
          @show-all="openRunDetailPanel('assertions')"
        />

        <RunEvidenceLedger
          v-if="!runDetailPanel || runDetailPanel === 'ledger'"
          :report="report"
          :full="runDetailPanel === 'ledger'"
          @show-all="openRunDetailPanel('ledger')"
        />

        <SectionFrame
          v-if="!runDetailPanel || runDetailPanel === 'browser'"
          :class="['run-section--browser', { 'run-section--standalone': runDetailPanel === 'browser' }]"
          title="浏览器事实"
          kicker="Browser Evidence · 西庑"
          section-id="browser-title"
        >
          <BrowserEvidence
            :evidence="browserSession"
            :image-urls="bundle.imageUrls"
            :summary="!runDetailPanel"
            @show-all="openRunDetailPanel('browser')"
          />
        </SectionFrame>

        <RunBoundary v-if="!runDetailPanel" :report="report" />

        <nav v-if="runDetailPanel" class="run-detail-panel-return" aria-label="完整账册返回操作">
          <button type="button" data-testid="run-panel-return-bottom" @click="closeRunDetailPanel">
            返回 Run 详情
          </button>
        </nav>
      </template>
      </template>

      <section v-else-if="publicView === 'comparison'" class="analysis-view" aria-labelledby="view-comparison-title">
        <ComparisonEntryState v-if="!comparison" :mode="loading ? 'loading' : error ? 'error' : 'empty'" :error="error">
          <template #action>
            <label class="local-import rerun-reselect" :class="{ 'is-active': activeSource === 'comparison' }">
              <span>{{ error ? '重新选择比较目录' : '选择复跑比较目录' }}</span>
              <input
                type="file"
                multiple
                webkitdirectory
                aria-label="选择本地 VeriTrail Comparison 目录"
                data-testid="local-comparison-input"
                @change="importComparison"
              />
            </label>
          </template>
        </ComparisonEntryState>
        <ComparisonView
          v-else
          :loaded="comparison"
          :panel="comparisonPanel"
          @open-panel="openComparisonPanel"
          @close-panel="closeComparisonPanel"
        >
          <template #actions>
            <label v-if="!comparisonPanel" class="local-import rerun-reselect" :class="{ 'is-active': activeSource === 'comparison' }">
              <span>重新选择比较目录</span>
              <input
                type="file"
                multiple
                webkitdirectory
                aria-label="重新选择本地 VeriTrail Comparison 目录"
                @change="importComparison"
              />
            </label>
          </template>
        </ComparisonView>
      </section>

      <section v-else-if="publicView === 'pairing'" class="analysis-view" aria-labelledby="view-pairing-title">
        <PairingEntryState v-if="!pairedAnalysis" :mode="loading ? 'loading' : error ? 'error' : 'empty'" :error="error">
          <template #action>
            <label class="local-import pairing-reselect" :class="{ 'is-active': activeSource === 'pairing' }">
              <span>{{ error ? '重新选择配对文件' : '选择四角色配对文件' }}</span>
              <input
                type="file"
                multiple
                accept=".json,.md,application/json,text/markdown"
                aria-label="选择本地 VeriTrail PairedAnalysis 四个文件"
                data-testid="local-pairing-input"
                @change="importPairedAnalysis"
              />
            </label>
          </template>
        </PairingEntryState>
        <PairedAnalysisView
          v-else
          :loaded="pairedAnalysis"
          :panel="pairingPanel"
          @open-panel="openPairingPanel"
          @close-panel="closePairingPanel"
        >
          <template #actions>
            <label v-if="!pairingPanel" class="local-import pairing-reselect" :class="{ 'is-active': activeSource === 'pairing' }">
              <span>重新选择配对文件</span>
              <input
                type="file"
                multiple
                accept=".json,.md,application/json,text/markdown"
                aria-label="重新选择本地 VeriTrail PairedAnalysis 四个文件"
                @change="importPairedAnalysis"
              />
            </label>
          </template>
        </PairedAnalysisView>
      </section>

      <section v-else class="analysis-view" aria-labelledby="view-batch-title">
        <BatchEntryState
          v-if="!batchAnalysis"
          :mode="loading ? 'loading' : error ? 'error' : 'empty'"
          :error="error"
          :kind="error ? stateCourtKind(error.code) : undefined"
        >
          <template #action>
            <label class="local-import batch-entry__import" :class="{ 'is-active': activeSource === 'batch' }">
              <span>{{ error ? '重新选择批次文件' : '选择全因子批次文件' }}</span>
              <input
                type="file"
                multiple
                accept=".json,.md,application/json,text/markdown"
                aria-label="选择本地 VeriTrail BatchAnalysis 四个文件"
                data-testid="local-batch-input"
                @change="importBatchAnalysis"
              />
            </label>
          </template>
        </BatchEntryState>
        <BatchAnalysisView v-else :loaded="batchAnalysis" />
      </section>
    </main>

    <footer class="site-footer">
      <span>VeriTrail / 验迹</span>
      <p>本地读取 · 确定性裁决 · 证据有界</p>
      <code>Palace Evidence 0.1</code>
      <button
        type="button"
        class="site-footer__seal"
        aria-label="返回本地 Run 目录"
        title="返回本地 Run 目录"
        @pointerdown="goToCatalogHomeOnPrimaryPointer"
        @click="goToCatalogHome"
      >
        验
      </button>
    </footer>
  </div>
</template>
