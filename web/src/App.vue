<script setup lang="ts">
import { computed, nextTick, onBeforeUnmount, onMounted, ref, shallowRef } from 'vue'
import BrowserEvidence from './components/BrowserEvidence.vue'
import RunCatalog from './components/RunCatalog.vue'
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
import type { CatalogResponse, CatalogRunSummary, LoadedBundle, ReportAssertion } from './domain/types'

type AssertionFilter = 'ALL' | 'PASS' | 'FAIL' | 'OTHER'

const bundle = shallowRef<LoadedBundle | null>(null)
const loading = ref(true)
const error = ref<{ code: string; message: string } | null>(null)
const activeSource = ref<DemoBundleId | 'local' | 'catalog'>('positive')
const assertionFilter = ref<AssertionFilter>('ALL')
const liveMessage = ref('正在读取正向证据包。')
const catalog = shallowRef<CatalogResponse | null>(null)
const catalogLoading = ref(true)
const catalogError = ref<{ code: string; message: string } | null>(null)
const selectedCatalogRunId = ref<string | null>(null)
let lastCatalogTriggerId: string | null = null
let loadSequence = 0

const report = computed(() => bundle.value?.report ?? null)
const browserSession = computed(() => (bundle.value ? browserEvidence(bundle.value) : null))
const filteredAssertions = computed(() => {
  const assertions = report.value?.assertions ?? []
  if (assertionFilter.value === 'ALL') return assertions
  if (assertionFilter.value === 'OTHER') {
    return assertions.filter((item) => !['PASS', 'FAIL'].includes(item.status))
  }
  return assertions.filter((item) => item.status === assertionFilter.value)
})
const assertionCounts = computed(() => {
  const assertions = report.value?.assertions ?? []
  return {
    ALL: assertions.length,
    PASS: assertions.filter((item) => item.status === 'PASS').length,
    FAIL: assertions.filter((item) => item.status === 'FAIL').length,
    OTHER: assertions.filter((item) => !['PASS', 'FAIL'].includes(item.status)).length,
  }
})

function fixtureFromLocation(): DemoBundleId | 'local' {
  const value = new URLSearchParams(window.location.search).get('fixture')
  return value === 'negative' || value === 'invalid' || value === 'local' ? value : 'positive'
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
  assertionFilter.value = 'ALL'
  activeSource.value = id
  selectedCatalogRunId.value = null
  liveMessage.value = `正在读取${sourceLabel(id)}。`
  if (pushHistory) {
    const url = new URL(window.location.href)
    url.searchParams.delete('run')
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

async function importLocal(event: Event) {
  const input = event.currentTarget as HTMLInputElement
  if (!input.files?.length) return
  const sequence = ++loadSequence
  loading.value = true
  error.value = null
  assertionFilter.value = 'ALL'
  activeSource.value = 'local'
  selectedCatalogRunId.value = null
  liveMessage.value = '正在本地内存中核验所选证据包。'
  const url = new URL(window.location.href)
  url.searchParams.delete('run')
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

async function selectCatalogRun(
  run: CatalogRunSummary,
  trigger?: HTMLElement,
  pushHistory = true,
) {
  const sequence = ++loadSequence
  loading.value = true
  error.value = null
  catalogError.value = null
  assertionFilter.value = 'ALL'
  activeSource.value = 'catalog'
  selectedCatalogRunId.value = run.catalog_run_id
  lastCatalogTriggerId = trigger ? run.catalog_run_id : lastCatalogTriggerId
  liveMessage.value = `正在从只读目录核验 ${run.run_id}。`
  if (pushHistory) {
    const url = new URL(window.location.href)
    url.searchParams.delete('fixture')
    url.searchParams.set('run', run.catalog_run_id)
    window.history.pushState({ run: run.catalog_run_id }, '', url)
  }
  releaseCurrentBundle()
  try {
    const loaded = await loadSameOriginBundle(run.bundle.base_url, `本地目录 · ${run.run_id}`)
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
  loading.value = false
  error.value = null
  activeSource.value = 'catalog'
  const runId = selectedCatalogRunId.value ?? lastCatalogTriggerId
  selectedCatalogRunId.value = null
  const url = new URL(window.location.href)
  url.searchParams.delete('run')
  url.searchParams.delete('fixture')
  window.history.pushState({}, '', url)
  liveMessage.value = '已返回本地 Run 目录。'
  void nextTick(() => {
    if (!runId) return
    document.querySelector<HTMLElement>(`[data-catalog-run-id="${runId}"]`)?.focus()
  })
}

function sourceLabel(id: DemoBundleId): string {
  if (id === 'positive') return '正向证据'
  if (id === 'negative') return '负向证据'
  return '损坏证据'
}

function onHistoryChange() {
  const catalogRunId = catalogRunIdFromLocation()
  if (catalogRunId) {
    const run = catalog.value?.runs.find((candidate) => candidate.catalog_run_id === catalogRunId)
    if (run) {
      void selectCatalogRun(run, undefined, false)
      return
    }
    ++loadSequence
    releaseCurrentBundle()
    activeSource.value = 'catalog'
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
  if (catalog.value && !new URLSearchParams(window.location.search).has('fixture')) {
    ++loadSequence
    releaseCurrentBundle()
    activeSource.value = 'catalog'
    selectedCatalogRunId.value = null
    loading.value = false
    error.value = null
    liveMessage.value = '本地 Run 目录已加载，请选择一项 Run。'
    return
  }
  const fixture = fixtureFromLocation()
  if (fixture === 'local') {
    ++loadSequence
    releaseCurrentBundle()
    activeSource.value = 'local'
    loading.value = false
    error.value = {
      code: 'LOCAL_RESELECT_REQUIRED',
      message: '为保护隐私，本地目录不会持久化；请重新选择目录或返回内置夹具。',
    }
    liveMessage.value = error.value.message
    return
  }
  void selectDemo(fixture, false)
}

function pretty(value: unknown): string {
  if (typeof value === 'string') return value
  return JSON.stringify(value, null, 2)
}

function shortHash(value: string): string {
  return `${value.slice(0, 12)}…${value.slice(-8)}`
}

function formatBytes(bytes: number): string {
  if (bytes < 1024) return `${bytes} B`
  return `${(bytes / 1024).toFixed(1)} KiB`
}

function displayDate(value: string): string {
  const date = new Date(value)
  return Number.isNaN(date.valueOf()) ? value : date.toLocaleString('zh-CN', { hour12: false })
}

function assertionStatusClass(assertion: ReportAssertion): string {
  return `assertion--${assertion.status.toLowerCase()}`
}

onMounted(() => {
  window.addEventListener('popstate', onHistoryChange)
  void refreshCatalog().then(onHistoryChange)
})

onBeforeUnmount(() => {
  ++loadSequence
  releaseCurrentBundle()
  window.removeEventListener('popstate', onHistoryChange)
})
</script>

<template>
  <div class="app-shell">
    <p class="sr-only" aria-live="polite">{{ liveMessage }}</p>

    <header class="masthead">
      <div class="masthead__roofline" aria-hidden="true"><span></span></div>
      <div class="masthead__inner">
        <div class="brand-lockup">
          <span class="brand-seal" aria-hidden="true">迹</span>
          <div>
            <p>VeriTrail · Palace Evidence</p>
            <h1>验迹证据工作台</h1>
            <span>让每一项结论，都沿证据中轴归位。</span>
          </div>
        </div>

        <nav class="source-switcher" aria-label="证据包来源">
          <button
            type="button"
            :aria-pressed="activeSource === 'positive'"
            data-testid="fixture-positive"
            @click="selectDemo('positive')"
          >
            正向证据
          </button>
          <button
            type="button"
            :aria-pressed="activeSource === 'negative'"
            data-testid="fixture-negative"
            @click="selectDemo('negative')"
          >
            负向证据
          </button>
          <button
            type="button"
            :aria-pressed="activeSource === 'invalid'"
            data-testid="fixture-invalid"
            @click="selectDemo('invalid')"
          >
            校验损坏包
          </button>
          <label class="local-import" :class="{ 'is-active': activeSource === 'local' }">
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
        </nav>

        <div v-if="report" class="status-gate" data-testid="status-gate">
          <StatusBadge dimension="execution" :value="report.execution_status" />
          <div class="status-gate__axis" aria-hidden="true"><span></span></div>
          <StatusBadge dimension="verdict" :value="report.verdict" />
          <div class="integrity-seal" data-testid="integrity-status">
            <span aria-hidden="true">◇</span>
            <div>
              <small>完整性</small>
              <strong>已核验</strong>
              <em>{{ bundle?.integrity.verifiedFiles }} 个文件</em>
            </div>
          </div>
        </div>
      </div>
    </header>

    <main id="main-content" class="evidence-axis">
      <RunCatalog
        v-if="catalogLoading || catalog || catalogError"
        :catalog="catalog"
        :loading="catalogLoading"
        :error="catalogError"
        :selected-run-id="selectedCatalogRunId"
        @select="selectCatalogRun"
        @retry="retryCatalog"
      />

      <div v-if="loading" class="loading-court" role="status" data-testid="loading-state">
        <span class="loading-court__mark" aria-hidden="true"></span>
        <p>正在沿清单核验证据包</p>
        <small>文件、大小、路径与 SHA-256 逐项比对</small>
      </div>

      <section v-else-if="error" class="error-court" aria-labelledby="error-title" data-testid="error-state">
        <span class="error-court__seal" aria-hidden="true">止</span>
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
        <div class="run-plaque" data-testid="run-summary">
          <div>
            <p>当前证据包</p>
            <strong>{{ report.run_id }}</strong>
            <span>{{ bundle.sourceLabel }}</span>
            <button
              v-if="activeSource === 'catalog'"
              type="button"
              class="catalog-return"
              data-testid="catalog-return"
              @click="returnToCatalog"
            >
              返回 Run 目录
            </button>
          </div>
          <dl>
            <div>
              <dt>Plan</dt>
              <dd>{{ report.plan.id }} · v{{ report.plan.version }}</dd>
            </div>
            <div>
              <dt>Plan SHA-256</dt>
              <dd><code :title="report.plan.sha256">{{ shortHash(report.plan.sha256) }}</code></dd>
            </div>
            <div>
              <dt>生成时间</dt>
              <dd>{{ displayDate(report.created_at) }}</dd>
            </div>
          </dl>
        </div>

        <SectionFrame title="结论总览" kicker="Overview · 前朝" section-id="overview-title">
          <div class="reason-banner" :class="`reason-banner--${report.verdict.toLowerCase()}`">
            <span aria-hidden="true">{{ report.verdict === 'PASS' ? '✓' : report.verdict === 'FAIL' ? '×' : '?' }}</span>
            <div>
              <small>确定性裁决原因</small>
              <strong>{{ report.reasons[0]?.code }}</strong>
              <p>{{ report.reasons[0]?.message }}</p>
            </div>
          </div>

          <div class="overview-grid">
            <article class="fact-card">
              <p>比较基线</p>
              <strong>{{ report.baseline?.id ?? '未声明' }}</strong>
              <code>{{ pretty(report.baseline?.status ?? 'UNKNOWN') }}</code>
            </article>
            <article class="fact-card">
              <p>唯一主要变量</p>
              <strong>{{ report.primary_variable?.name ?? '未声明' }}</strong>
              <code>{{ pretty(report.primary_variable?.value ?? null) }}</code>
            </article>
            <article class="fact-card">
              <p>负载语义</p>
              <strong>{{ Object.keys(report.load_model ?? {}).length }} 个维度</strong>
              <code>{{ pretty(report.load_model ?? {}) }}</code>
            </article>
            <article class="fact-card">
              <p>影响层级</p>
              <strong>{{ report.change_scope?.level ?? '未声明' }}</strong>
              <code>{{ pretty(report.change_scope?.owner ?? 'UNKNOWN') }}</code>
            </article>
          </div>

          <details class="applicability">
            <summary>展开适用边界与资源预算</summary>
            <div>
              <article><h3>Subject</h3><pre>{{ pretty(report.subject ?? {}) }}</pre></article>
              <article><h3>Resource budget</h3><pre>{{ pretty(report.resource_budget ?? {}) }}</pre></article>
              <article><h3>Change scope</h3><pre>{{ pretty(report.change_scope ?? {}) }}</pre></article>
            </div>
          </details>
        </SectionFrame>

        <SectionFrame title="确定性断言" kicker="Assertions · 中庭" section-id="assertions-title">
          <template #actions>
            <div class="filter-group" aria-label="断言状态筛选">
              <button
                v-for="item in (['ALL', 'PASS', 'FAIL', 'OTHER'] as const)"
                :key="item"
                type="button"
                :aria-pressed="assertionFilter === item"
                :data-testid="`filter-${item.toLowerCase()}`"
                @click="assertionFilter = item"
              >
                {{ item === 'ALL' ? '全部' : item === 'OTHER' ? '其他' : item }}
                <span>{{ assertionCounts[item] }}</span>
              </button>
            </div>
          </template>

          <div class="assertion-list" data-testid="assertion-list">
            <article
              v-for="assertion in filteredAssertions"
              :key="assertion.id"
              :class="['assertion-card', assertionStatusClass(assertion)]"
            >
              <div class="assertion-card__status">
                <span aria-hidden="true">{{ assertion.status === 'PASS' ? '✓' : assertion.status === 'FAIL' ? '×' : '?' }}</span>
                <strong>{{ assertion.status }}</strong>
              </div>
              <div class="assertion-card__main">
                <div>
                  <h3>{{ assertion.id }}</h3>
                  <span>{{ assertion.severity }} · {{ assertion.operator ?? 'rule' }}</span>
                </div>
                <p>{{ assertion.explanation ?? '该结果由报告中的版本化规则提供。' }}</p>
              </div>
              <dl>
                <div><dt>Expected</dt><dd><code>{{ pretty(assertion.expected) }}</code></dd></div>
                <div><dt>Actual</dt><dd><code>{{ pretty(assertion.actual) }}</code></dd></div>
              </dl>
            </article>
          </div>
        </SectionFrame>

        <SectionFrame title="证据账册" kicker="Evidence Ledger · 东庑" section-id="ledger-title">
          <div class="ledger" data-testid="evidence-ledger">
            <article v-for="artifact in report.evidence" :key="artifact.sha256" class="ledger-row">
              <div class="ledger-row__type">
                <span aria-hidden="true">档</span>
                <div>
                  <strong>{{ artifact.evidence_type }}</strong>
                  <small>{{ artifact.source }}</small>
                </div>
              </div>
              <dl>
                <div><dt>SHA-256</dt><dd><code :title="artifact.sha256">{{ shortHash(artifact.sha256) }}</code></dd></div>
                <div><dt>大小</dt><dd>{{ formatBytes(artifact.size) }}</dd></div>
                <div><dt>脱敏</dt><dd>{{ artifact.redacted ? `是 · ${artifact.redacted_fields}` : '无命中' }}</dd></div>
                <div><dt>解析器</dt><dd>{{ artifact.parser_version }}</dd></div>
              </dl>
            </article>
          </div>
        </SectionFrame>

        <SectionFrame title="浏览器事实" kicker="Browser Evidence · 西庑" section-id="browser-title">
          <BrowserEvidence :evidence="browserSession" :image-urls="bundle.imageUrls" />
        </SectionFrame>

        <SectionFrame title="缺口、复现与清理" kicker="Boundary · 后寝" section-id="boundary-title">
          <div class="boundary-grid">
            <article>
              <h3>证据缺口</h3>
              <p v-if="report.missing_evidence.length === 0" class="quiet-pass">未记录缺失证据</p>
              <ul v-else><li v-for="item in report.missing_evidence" :key="item">{{ item }}</li></ul>
            </article>
            <article>
              <h3>污染清单</h3>
              <p v-if="report.contamination.length === 0" class="quiet-pass">未记录环境污染</p>
              <pre v-else>{{ pretty(report.contamination) }}</pre>
            </article>
            <article>
              <h3>复现步骤</h3>
              <ol><li v-for="item in report.reproduction_steps" :key="item">{{ item }}</li></ol>
            </article>
            <article>
              <h3>清理步骤</h3>
              <ol><li v-for="item in report.cleanup_steps" :key="item">{{ item }}</li></ol>
            </article>
          </div>
        </SectionFrame>
      </template>
    </main>

    <footer class="site-footer">
      <span>VeriTrail / 验迹</span>
      <p>本地读取 · 确定性裁决 · 证据有界</p>
      <code>Palace Evidence 0.1</code>
    </footer>
  </div>
</template>
