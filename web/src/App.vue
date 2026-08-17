<script setup lang="ts">
import { computed, nextTick, onBeforeUnmount, onMounted, ref, shallowRef } from 'vue'
import BatchAnalysisView from './components/BatchAnalysisView.vue'
import BrowserEvidence from './components/BrowserEvidence.vue'
import ComparisonView from './components/ComparisonView.vue'
import CrossAxisNavigation from './components/CrossAxisNavigation.vue'
import PairedAnalysisView from './components/PairedAnalysisView.vue'
import PairingEntryState from './components/PairingEntryState.vue'
import RunCatalog from './components/RunCatalog.vue'
import RunBoundary from './components/RunBoundary.vue'
import RunAssertions from './components/RunAssertions.vue'
import RunEvidenceLedger from './components/RunEvidenceLedger.vue'
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
  catalogRunIdFromLocation,
  CatalogLoadError,
  fetchCatalog,
} from './domain/catalog'
import { BatchLoadError, loadLocalBatchAnalysis } from './domain/batch'
import { ComparisonLoadError, loadLocalComparison } from './domain/comparison'
import { loadLocalPairedAnalysis, PairingLoadError } from './domain/pairing'
import type {
  CatalogResponse,
  CatalogRunSummary,
  LoadedBatchAnalysis,
  LoadedBundle,
  LoadedComparison,
  LoadedPairedAnalysis,
} from './domain/types'

type PublicView = 'runs' | 'comparison' | 'pairing' | 'batch'
type RunDetailPanel = 'browser' | 'assertions' | 'ledger'
type PairingPanel = 'sources' | 'outcomes'

const bundle = shallowRef<LoadedBundle | null>(null)
const comparison = shallowRef<LoadedComparison | null>(null)
const pairedAnalysis = shallowRef<LoadedPairedAnalysis | null>(null)
const batchAnalysis = shallowRef<LoadedBatchAnalysis | null>(null)
const loading = ref(true)
const error = ref<{ code: string; message: string } | null>(null)
const activeSource = ref<DemoBundleId | 'local' | 'catalog' | 'comparison' | 'pairing' | 'batch'>('positive')
const publicView = ref<PublicView>('runs')
const liveMessage = ref('正在读取正向证据包。')
const catalog = shallowRef<CatalogResponse | null>(null)
const catalogLoading = ref(true)
const catalogError = ref<{ code: string; message: string } | null>(null)
const selectedCatalogRunId = ref<string | null>(null)
const runDetailPanel = ref<RunDetailPanel | null>(null)
const pairingPanel = ref<PairingPanel | null>(null)
let lastCatalogTriggerId: string | null = null
let loadSequence = 0

const report = computed(() => bundle.value?.report ?? null)
const browserSession = computed(() => (bundle.value ? browserEvidence(bundle.value) : null))
const isCatalogRunDetail = computed(
  () =>
    publicView.value === 'runs' &&
    activeSource.value === 'catalog' &&
    selectedCatalogRunId.value !== null,
)
const usesInnerShell = computed(
  () =>
    isCatalogRunDetail.value ||
    Boolean(report.value && bundle.value) ||
    publicView.value === 'comparison' ||
    publicView.value === 'batch',
)

function runDetailPanelFromLocation(): RunDetailPanel | null {
  const panel = new URLSearchParams(window.location.search).get('panel')
  return panel === 'browser' || panel === 'assertions' || panel === 'ledger' ? panel : null
}

function runDetailPanelLabel(panel: RunDetailPanel): string {
  if (panel === 'browser') return '浏览器事实'
  if (panel === 'assertions') return '确定性断言'
  return '证据账册'
}

function pairingPanelFromLocation(): PairingPanel | null {
  const panel = new URLSearchParams(window.location.search).get('panel')
  return panel === 'sources' || panel === 'outcomes' ? panel : null
}

function pairingPanelLabel(panel: PairingPanel): string {
  return panel === 'sources' ? '四角色来源账册' : '预注册断言全貌'
}

function openPairingPanel(panel: PairingPanel) {
  pairingPanel.value = panel
  const url = new URL(window.location.href)
  url.searchParams.set('fixture', 'pairing')
  url.searchParams.set('panel', panel)
  window.history.pushState({ fixture: 'pairing', panel }, '', url)
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
  const url = new URL(window.location.href)
  url.searchParams.delete('panel')
  window.history.pushState({ fixture: 'pairing' }, '', url)
  liveMessage.value = '已返回配对实验总览。'
  void nextTick(() => {
    if (panel) document.querySelector<HTMLElement>(`[data-open-pairing-panel="${panel}"]`)?.focus()
  })
}

function openRunDetailPanel(panel: RunDetailPanel) {
  runDetailPanel.value = panel
  const url = new URL(window.location.href)
  url.searchParams.set('panel', panel)
  window.history.pushState({ run: selectedCatalogRunId.value, panel }, '', url)
  liveMessage.value = `已进入${runDetailPanelLabel(panel)}完整视图。`
  void nextTick(() => {
    document.getElementById('run-detail-panel-title')?.focus()
    document.documentElement.scrollTop = 0
    document.body.scrollTop = 0
  })
}

function closeRunDetailPanel() {
  const panel = runDetailPanel.value
  runDetailPanel.value = null
  const url = new URL(window.location.href)
  url.searchParams.delete('panel')
  window.history.pushState({ run: selectedCatalogRunId.value }, '', url)
  liveMessage.value = '已返回 Run 详情总览。'
  void nextTick(() => {
    if (panel) document.querySelector<HTMLElement>(`[data-open-run-panel="${panel}"]`)?.focus()
  })
}

function fixtureFromLocation(): DemoBundleId | 'local' | 'comparison' | 'pairing' | 'batch' {
  const value = new URLSearchParams(window.location.search).get('fixture')
  return value === 'negative' || value === 'invalid' || value === 'local' || value === 'comparison' || value === 'pairing' || value === 'batch'
    ? value
    : 'positive'
}

function publicViewFromLocation(): PublicView {
  const params = new URLSearchParams(window.location.search)
  const view = params.get('view')
  if (view === 'runs' || view === 'comparison' || view === 'pairing' || view === 'batch') {
    return view
  }
  const fixture = fixtureFromLocation()
  if (fixture === 'comparison' || fixture === 'pairing' || fixture === 'batch') return fixture
  return 'runs'
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
  activeSource.value = view === 'runs' ? 'catalog' : view
  selectedCatalogRunId.value = null
  runDetailPanel.value = null
  pairingPanel.value = null
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
  if (view === 'runs' && isCatalogRunDetail.value) {
    returnToCatalog()
    return
  }
  if (publicView.value !== view) {
    const url = new URL(window.location.href)
    url.searchParams.delete('fixture')
    url.searchParams.delete('run')
    url.searchParams.delete('panel')
    url.searchParams.set('view', view)
    window.history.pushState({ view }, '', url)
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

async function selectDemo(id: DemoBundleId, pushHistory = true) {
  const sequence = ++loadSequence
  loading.value = true
  error.value = null
  activeSource.value = id
  publicView.value = 'runs'
  selectedCatalogRunId.value = null
  comparison.value = null
  pairedAnalysis.value = null
  batchAnalysis.value = null
  liveMessage.value = `正在读取${sourceLabel(id)}。`
  if (pushHistory) {
    const url = new URL(window.location.href)
    url.searchParams.delete('run')
    url.searchParams.delete('view')
    url.searchParams.set('fixture', id)
    window.history.pushState({ fixture: id }, '', url)
  }
  releaseCurrentBundle()
  try {
    const loaded = await loadDemoBundle(id)
    if (sequence !== loadSequence) {
      loaded.release()
      return
    }
    bundle.value = loaded
    liveMessage.value = `${sourceLabel(id)}已加载，完整性核验通过。`
  } catch (cause) {
    if (sequence !== loadSequence) return
    error.value = describeError(cause)
    liveMessage.value = `证据包读取失败：${error.value.message}`
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
  releaseCurrentBundle()
  const url = new URL(window.location.href)
  url.searchParams.delete('fixture')
  url.searchParams.delete('run')
  url.searchParams.set('view', 'runs')
  window.history.pushState({ view: 'runs' }, '', url)
  liveMessage.value = '已收起损坏证据提示，返回本地 Run 目录。'
  if (restoreFocus) {
    void nextTick(() => document.querySelector<HTMLElement>('[data-testid="fixture-invalid"]')?.focus())
  }
}

function toggleInvalidDemo() {
  if (activeSource.value === 'invalid' && error.value) {
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
  selectedCatalogRunId.value = null
  comparison.value = null
  pairedAnalysis.value = null
  batchAnalysis.value = null
  liveMessage.value = '正在本地内存中核验所选证据包。'
  const url = new URL(window.location.href)
  url.searchParams.delete('run')
  url.searchParams.delete('view')
  url.searchParams.set('fixture', 'local')
  window.history.pushState({ fixture: 'local' }, '', url)
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

async function importComparison(event: Event) {
  const input = event.currentTarget as HTMLInputElement
  if (!input.files?.length) return
  const sequence = ++loadSequence
  loading.value = true
  error.value = null
  activeSource.value = 'comparison'
  publicView.value = 'comparison'
  selectedCatalogRunId.value = null
  comparison.value = null
  pairedAnalysis.value = null
  batchAnalysis.value = null
  liveMessage.value = '正在本地内存中核验复跑 Comparison Manifest。'
  const url = new URL(window.location.href)
  url.searchParams.delete('run')
  url.searchParams.delete('view')
  url.searchParams.set('fixture', 'comparison')
  window.history.pushState({ fixture: 'comparison' }, '', url)
  releaseCurrentBundle()
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
  const sequence = ++loadSequence
  loading.value = true
  error.value = null
  activeSource.value = 'pairing'
  publicView.value = 'pairing'
  selectedCatalogRunId.value = null
  comparison.value = null
  pairedAnalysis.value = null
  batchAnalysis.value = null
  pairingPanel.value = null
  liveMessage.value = '正在本地内存中核验 PairedAnalysis Manifest 与 PairingPlan seal。'
  const url = new URL(window.location.href)
  url.searchParams.delete('run')
  url.searchParams.delete('view')
  url.searchParams.delete('panel')
  url.searchParams.set('fixture', 'pairing')
  window.history.pushState({ fixture: 'pairing' }, '', url)
  releaseCurrentBundle()
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

async function importBatchAnalysis(event: Event) {
  const input = event.currentTarget as HTMLInputElement
  if (!input.files?.length) return
  const sequence = ++loadSequence
  loading.value = true
  error.value = null
  activeSource.value = 'batch'
  publicView.value = 'batch'
  selectedCatalogRunId.value = null
  comparison.value = null
  pairedAnalysis.value = null
  batchAnalysis.value = null
  liveMessage.value = '正在本地内存中核验 BatchAnalysis Manifest、BatchPlan seal 与完整矩阵。'
  const url = new URL(window.location.href)
  url.searchParams.delete('run')
  url.searchParams.delete('view')
  url.searchParams.set('fixture', 'batch')
  window.history.pushState({ fixture: 'batch' }, '', url)
  releaseCurrentBundle()
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
) {
  const sequence = ++loadSequence
  loading.value = true
  error.value = null
  catalogError.value = null
  activeSource.value = 'catalog'
  publicView.value = 'runs'
  selectedCatalogRunId.value = run.catalog_run_id
  runDetailPanel.value = null
  comparison.value = null
  pairedAnalysis.value = null
  batchAnalysis.value = null
  lastCatalogTriggerId = trigger ? run.catalog_run_id : lastCatalogTriggerId
  liveMessage.value = `正在从只读目录核验 ${run.run_id}。`
  if (pushHistory) {
    const url = new URL(window.location.href)
    url.searchParams.delete('fixture')
    url.searchParams.delete('view')
    url.searchParams.delete('panel')
    url.searchParams.set('run', run.catalog_run_id)
    window.history.pushState({ run: run.catalog_run_id }, '', url)
  }
  releaseCurrentBundle()
  comparison.value = null
  pairedAnalysis.value = null
  batchAnalysis.value = null
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
      return
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
  } catch (cause) {
    if (sequence !== loadSequence) return
    const described = describeCatalogError(cause)
    catalogError.value = described
    error.value = described
    liveMessage.value = `目录 Run 读取失败：${described.message}`
  } finally {
    if (sequence === loadSequence) loading.value = false
  }
}

async function retryCatalog() {
  const selected = selectedCatalogRunId.value
  await refreshCatalog()
  if (selected && catalog.value) {
    const run = catalog.value.runs.find((candidate) => candidate.catalog_run_id === selected)
    if (run) await selectCatalogRun(run, undefined, false)
  }
}

function returnToCatalog() {
  ++loadSequence
  releaseCurrentBundle()
  comparison.value = null
  pairedAnalysis.value = null
  batchAnalysis.value = null
  loading.value = false
  error.value = null
  activeSource.value = 'catalog'
  publicView.value = 'runs'
  const runId = selectedCatalogRunId.value ?? lastCatalogTriggerId
  selectedCatalogRunId.value = null
  runDetailPanel.value = null
  const url = new URL(window.location.href)
  url.searchParams.delete('run')
  url.searchParams.delete('fixture')
  url.searchParams.delete('view')
  url.searchParams.delete('panel')
  window.history.pushState({}, '', url)
  liveMessage.value = '已返回本地 Run 目录。'
  void nextTick(() => {
    if (!runId) return
    document.querySelector<HTMLElement>(`[data-catalog-run-id="${runId}"]`)?.focus()
  })
}

function goToCatalogHome() {
  if (isCatalogRunDetail.value) {
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
  document.documentElement.scrollTop = 0
  document.body.scrollTop = 0
  liveMessage.value = '已回到本地 Run 目录。'
  focusPublicViewTitle('runs')
}

function sourceLabel(id: DemoBundleId): string {
  if (id === 'positive') return '正向证据'
  if (id === 'negative') return '负向证据'
  return '损坏证据'
}

function onHistoryChange(focusTarget = false) {
  const params = new URLSearchParams(window.location.search)
  const requestedView = publicViewFromLocation()
  if (requestedView !== 'runs' && params.has('view')) {
    resetPublicView(requestedView)
    if (focusTarget) focusPublicViewTitle(requestedView)
    return
  }
  const catalogRunId = catalogRunIdFromLocation()
  if (catalogRunId) {
    const requestedPanel = runDetailPanelFromLocation()
    const previousPanel = runDetailPanel.value
    runDetailPanel.value = requestedPanel
    if (selectedCatalogRunId.value === catalogRunId && bundle.value) {
      if (focusTarget) {
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
      return
    }
    const run = catalog.value?.runs.find((candidate) => candidate.catalog_run_id === catalogRunId)
    if (run) {
      void selectCatalogRun(run, undefined, false).then(() => {
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
    ++loadSequence
    releaseCurrentBundle()
    comparison.value = null
    pairedAnalysis.value = null
    batchAnalysis.value = null
    activeSource.value = 'catalog'
    publicView.value = 'runs'
    selectedCatalogRunId.value = catalogRunId
    loading.value = false
    error.value = {
      code: 'RUN_NOT_FOUND',
      message: 'URL 中的 Catalog Run 不存在，请返回目录重新选择。',
    }
    catalogError.value = error.value
    liveMessage.value = error.value.message
    return
  }
  // `view=runs` is the public Catalog entry, not an implicit positive fixture.
  // Keeping that distinction prevents a deep-link refresh from bypassing the
  // ledger and dropping a user into an unrelated demo Run.
  if (catalog.value && !params.has('fixture') && !params.has('run') && (params.get('view') === 'runs' || !params.has('view'))) {
    const previousRunId = selectedCatalogRunId.value ?? lastCatalogTriggerId
    ++loadSequence
    releaseCurrentBundle()
    comparison.value = null
    pairedAnalysis.value = null
    batchAnalysis.value = null
    activeSource.value = 'catalog'
    publicView.value = 'runs'
    selectedCatalogRunId.value = null
    loading.value = false
    error.value = null
    liveMessage.value = '本地 Run 目录已加载，请选择一项 Run。'
    if (focusTarget) {
      void nextTick(() => {
        const row = previousRunId
          ? document.querySelector<HTMLElement>(`[data-catalog-run-id="${previousRunId}"]`)
          : null
        if (row) row.focus()
        else document.getElementById('view-runs-title')?.focus()
      })
    }
    return
  }
  const fixture = fixtureFromLocation()
  if (fixture === 'comparison') {
    ++loadSequence
    releaseCurrentBundle()
    comparison.value = null
    pairedAnalysis.value = null
    batchAnalysis.value = null
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
  if (fixture === 'pairing') {
    if (pairedAnalysis.value) {
      const requestedPanel = pairingPanelFromLocation()
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
    ++loadSequence
    releaseCurrentBundle()
    comparison.value = null
    pairedAnalysis.value = null
    batchAnalysis.value = null
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
  if (fixture === 'batch') {
    ++loadSequence
    releaseCurrentBundle()
    comparison.value = null
    pairedAnalysis.value = null
    batchAnalysis.value = null
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
  if (fixture === 'local') {
    ++loadSequence
    releaseCurrentBundle()
    comparison.value = null
    pairedAnalysis.value = null
    batchAnalysis.value = null
    activeSource.value = 'local'
    publicView.value = 'runs'
    loading.value = false
    error.value = {
      code: 'LOCAL_RESELECT_REQUIRED',
      message: '为保护隐私，本地目录不会持久化；请重新选择目录或返回内置夹具。',
    }
    liveMessage.value = error.value.message
    if (focusTarget) focusPublicViewTitle('runs')
    return
  }
  void selectDemo(fixture, false)
  if (focusTarget) focusPublicViewTitle('runs')
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
  window.addEventListener('popstate', onPopState)
  void refreshCatalog().then(() => onHistoryChange())
})

onBeforeUnmount(() => {
  ++loadSequence
  releaseCurrentBundle()
  window.removeEventListener('popstate', onPopState)
})
</script>

<template>
  <div
    :class="[
      'app-shell',
      {
        'app-shell--inner': usesInnerShell,
        'app-shell--catalog': publicView === 'runs' && !usesInnerShell,
        'app-shell--run-detail': isCatalogRunDetail,
        'app-shell--pairing': publicView === 'pairing',
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

    <main id="main-content" class="evidence-axis">
      <template v-if="publicView === 'runs'">
        <section v-if="!isCatalogRunDetail" class="view-introduction view-introduction--runs" aria-labelledby="view-runs-title">
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
                data-testid="fixture-positive"
                @click="selectDemo('positive')"
              >
                <img :src="'/textures/r3-command-positive.png'" alt="" aria-hidden="true" />
                <span>正向证据</span>
              </button>
              <button
                type="button"
                :aria-pressed="activeSource === 'negative'"
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
                aria-controls="run-error-state"
                data-testid="fixture-invalid"
                @click="toggleInvalidDemo"
              >
                <img :src="'/textures/r3-command-invalid.png'" alt="" aria-hidden="true" />
                <span>校验损坏包</span>
              </button>
            </div>
            <label class="local-import runs-toolstrip__local" :class="{ 'is-active': activeSource === 'local' }">
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
        v-if="!isCatalogRunDetail && (catalogLoading || catalog || catalogError)"
        :catalog="catalog"
        :loading="catalogLoading"
        :error="catalogError"
        :selected-run-id="selectedCatalogRunId"
        @select="selectCatalogRun"
        @retry="retryCatalog"
      />

      <nav
        v-if="isCatalogRunDetail"
        class="run-detail-breadcrumb"
        aria-label="Run 详情路径与分区"
        data-testid="run-detail-breadcrumb"
      >
        <div class="run-detail-breadcrumb__path">
          <button
            type="button"
            :data-testid="report && bundle ? 'catalog-return' : undefined"
            @click="returnToCatalog"
          >
            返回目录
          </button>
          <span aria-hidden="true">/</span>
          <span>Runs</span>
          <span aria-hidden="true">/</span>
          <span>Catalog</span>
          <span aria-hidden="true">/</span>
          <strong :title="report?.run_id ?? selectedCatalogRunId ?? undefined">
            {{ report?.run_id ?? selectedCatalogRunId }}
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

      <div v-if="loading" class="loading-court state-court state-court--loading" role="status" data-testid="loading-state" data-state-kind="loading">
        <span class="loading-court__mark" aria-hidden="true"></span>
        <p>正在沿清单核验证据包</p>
        <small>文件、大小、路径与 SHA-256 逐项比对</small>
      </div>

      <section
        v-else-if="error"
        id="run-error-state"
        :class="['error-court', 'state-court', `state-court--${stateCourtKind(error.code)}`]"
        :data-state-kind="stateCourtKind(error.code)"
        aria-labelledby="error-title"
        data-testid="error-state"
      >
        <button
          type="button"
          class="error-court__seal"
          aria-label="收起损坏证据提示"
          data-testid="dismiss-invalid-state"
          @click="dismissRunError(true)"
        >
          止
        </button>
        <p class="eyebrow">证据包未进入可信展示</p>
        <h2 id="error-title">{{ error.message }}</h2>
        <code>{{ error.code }}</code>
        <p>工作台没有据此改写 Run 的 Verdict，也没有展示部分可信内容。</p>
        <button
          type="button"
          :data-testid="activeSource === 'catalog' ? 'retry-catalog-run' : 'retry-positive'"
          @click="activeSource === 'catalog' ? retryCatalog() : selectDemo('positive')"
        >
          {{ activeSource === 'catalog' ? '重新读取目录 Run' : '返回正向证据重试' }}
        </button>
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
        <header class="view-introduction">
          <p class="eyebrow">Public View · 南向</p>
          <h2 id="view-comparison-title" tabindex="-1" data-testid="view-comparison-title">Rerun Comparison</h2>
          <label class="local-import" :class="{ 'is-active': activeSource === 'comparison' }">
            <span>选择复跑比较包</span>
            <input
              type="file"
              multiple
              webkitdirectory
              aria-label="选择本地 VeriTrail Comparison 目录"
              data-testid="local-comparison-input"
              @change="importComparison"
            />
          </label>
        </header>
        <div v-if="loading" class="loading-court state-court state-court--loading" role="status" data-testid="loading-state" data-state-kind="loading">
          <span class="loading-court__mark" aria-hidden="true"></span>
          <p>正在沿清单核验复跑比较包</p>
          <small>文件、大小、路径与 SHA-256 逐项比对</small>
        </div>
        <section
          v-else-if="error"
          :class="['error-court', 'state-court', `state-court--${stateCourtKind(error.code)}`]"
          :data-state-kind="stateCourtKind(error.code)"
          aria-labelledby="comparison-error-title"
          data-testid="error-state"
        >
          <span class="error-court__seal" aria-hidden="true">止</span>
          <p class="eyebrow">Comparison 未进入可信展示</p>
          <h3 id="comparison-error-title">{{ error.message }}</h3>
          <code>{{ error.code }}</code>
          <p>请重新选择本地 Comparison 目录；文件不会上传，也不会持久化。</p>
        </section>
        <ComparisonView v-else-if="comparison" :loaded="comparison" />
        <p v-else class="analysis-empty state-court state-court--empty" data-testid="comparison-empty" data-state-kind="empty">请选择两个同计划 Run 的 Comparison 目录。</p>
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
        <header class="view-introduction">
          <p class="eyebrow">Public View · 东向</p>
          <h2 id="view-batch-title" tabindex="-1" data-testid="view-batch-title">Batch Analysis</h2>
          <label class="local-import" :class="{ 'is-active': activeSource === 'batch' }">
            <span>选择全因子批次文件</span>
            <input
              type="file"
              multiple
              accept=".json,.md,application/json,text/markdown"
              aria-label="选择本地 VeriTrail BatchAnalysis 四个文件"
              data-testid="local-batch-input"
              @change="importBatchAnalysis"
            />
          </label>
        </header>
        <div v-if="loading" class="loading-court state-court state-court--loading" role="status" data-testid="loading-state" data-state-kind="loading">
          <span class="loading-court__mark" aria-hidden="true"></span>
          <p>正在核验全因子批次分析包</p>
          <small>Manifest、BatchPlan seal 与完整矩阵逐项比对</small>
        </div>
        <section
          v-else-if="error"
          :class="['error-court', 'state-court', `state-court--${stateCourtKind(error.code)}`]"
          :data-state-kind="stateCourtKind(error.code)"
          aria-labelledby="batch-error-title"
          data-testid="error-state"
        >
          <span class="error-court__seal" aria-hidden="true">止</span>
          <p class="eyebrow">Batch Analysis 未进入可信展示</p>
          <h3 id="batch-error-title">{{ error.message }}</h3>
          <code>{{ error.code }}</code>
          <p>请重新选择四个本地文件；文件不会上传，也不会持久化。</p>
        </section>
        <BatchAnalysisView v-else-if="batchAnalysis" :loaded="batchAnalysis" />
        <p v-else class="analysis-empty state-court state-court--empty" data-testid="batch-empty" data-state-kind="empty">请选择 BatchAnalysis 的四个本地文件。</p>
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
        @click="goToCatalogHome"
      >
        验
      </button>
    </footer>
  </div>
</template>
