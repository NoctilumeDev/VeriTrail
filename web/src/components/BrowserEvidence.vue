<script setup lang="ts">
import { computed, nextTick, ref } from 'vue'
import type {
  BrowserConsoleEntry,
  BrowserNetworkEntry,
  BrowserScreenshot,
  BrowserStep,
  BrowserViewportRun,
  EvidenceDocument,
} from '../domain/types'

const props = defineProps<{
  evidence: EvidenceDocument | null
  imageUrls: Record<string, string>
  summary?: boolean
}>()

const emit = defineEmits<{
  showAll: []
}>()

type TabId = 'steps' | 'console' | 'network' | 'screenshots'

const tabs: Array<{ id: TabId; label: string }> = [
  { id: 'steps', label: '步骤' },
  { id: 'console', label: 'Console' },
  { id: 'network', label: 'Network' },
  { id: 'screenshots', label: '截图' },
]
const activeTab = ref<TabId>('steps')
const tabButtons = ref<HTMLButtonElement[]>([])
const dialog = ref<HTMLDialogElement | null>(null)
const selectedScreenshot = ref<BrowserScreenshot | null>(null)
const lastTrigger = ref<HTMLElement | null>(null)

const facts = computed(() => props.evidence?.facts ?? {})
const steps = computed(() => (Array.isArray(facts.value.steps) ? (facts.value.steps as BrowserStep[]) : []))
const consoleEntries = computed(() =>
  Array.isArray(facts.value.console) ? (facts.value.console as BrowserConsoleEntry[]) : [],
)
const networkEntries = computed(() =>
  Array.isArray(facts.value.network) ? (facts.value.network as BrowserNetworkEntry[]) : [],
)
const screenshots = computed(() =>
  Array.isArray(facts.value.screenshots) ? (facts.value.screenshots as BrowserScreenshot[]) : [],
)
const visibleSteps = computed(() => (props.summary ? steps.value.slice(0, 3) : steps.value))
const visibleConsoleEntries = computed(() =>
  props.summary ? consoleEntries.value.slice(0, 3) : consoleEntries.value,
)
const visibleNetworkEntries = computed(() =>
  props.summary ? networkEntries.value.slice(0, 3) : networkEntries.value,
)
const visibleScreenshots = computed(() =>
  props.summary ? screenshots.value.slice(0, 3) : screenshots.value,
)
const viewports = computed(() =>
  Array.isArray(facts.value.viewport_runs) ? (facts.value.viewport_runs as BrowserViewportRun[]) : [],
)
const visibleViewports = computed(() => (props.summary ? viewports.value.slice(0, 2) : viewports.value))
const errorCount = computed(
  () =>
    Number(facts.value.unexpected_console_error_count ?? 0) +
    Number(facts.value.page_error_count ?? 0) +
    Number(facts.value.unexpected_http_error_count ?? 0),
)

function selectTab(id: TabId) {
  activeTab.value = id
}

function moveTab(event: KeyboardEvent, index: number) {
  if (!['ArrowLeft', 'ArrowRight', 'Home', 'End'].includes(event.key)) return
  event.preventDefault()
  let next = index
  if (event.key === 'ArrowRight') next = (index + 1) % tabs.length
  if (event.key === 'ArrowLeft') next = (index - 1 + tabs.length) % tabs.length
  if (event.key === 'Home') next = 0
  if (event.key === 'End') next = tabs.length - 1
  activeTab.value = tabs[next]!.id
  void nextTick(() => tabButtons.value[next]?.focus())
}

function openScreenshot(screenshot: BrowserScreenshot, event: MouseEvent) {
  selectedScreenshot.value = screenshot
  lastTrigger.value = event.currentTarget as HTMLElement
  dialog.value?.showModal()
}

function closeScreenshot() {
  dialog.value?.close()
}

function restoreFocus() {
  selectedScreenshot.value = null
  lastTrigger.value?.focus()
}

function compactUrl(value: string): string {
  try {
    const url = new URL(value)
    return `${url.pathname}${url.search}`
  } catch {
    return value
  }
}
</script>

<template>
  <div v-if="!evidence" class="browser-absence" data-testid="browser-empty" data-state-kind="no-browser">
    <span class="browser-absence__mark" aria-hidden="true">—</span>
    <div>
      <p class="browser-absence__kicker">Browser Evidence · 未适用</p>
      <strong>未包含浏览器证据</strong>
      <p>该 Report 0.1 没有声明 browser.session；这不等于浏览器检查通过。</p>
    </div>
  </div>

  <div v-else class="browser-evidence" data-testid="browser-evidence">
    <section class="browser-summary" aria-label="浏览器采集摘要" data-testid="browser-summary">
      <header class="browser-summary__heading">
        <p>Browser Evidence · 西庑账册</p>
        <h3>浏览器采集摘要</h3>
      </header>
      <div class="browser-metrics">
        <div>
          <small>采集</small>
          <strong>{{ facts.capture_complete ? '完整' : '不完整' }}</strong>
        </div>
        <div>
          <small>清理</small>
          <strong>{{ facts.cleanup_complete ? '完成' : '未完成' }}</strong>
        </div>
        <div>
          <small>视口</small>
          <strong>{{ viewports.length }}</strong>
        </div>
        <div :class="{ 'metric-alert': errorCount > 0 }">
          <small>异常事实</small>
          <strong>{{ errorCount }}</strong>
        </div>
      </div>
    </section>

    <section class="viewport-ledger" aria-label="视口覆盖">
      <p class="viewport-ledger__label">视口记录</p>
      <div class="viewport-strip">
        <article v-for="viewport in visibleViewports" :key="viewport.name" class="viewport-chip">
          <span aria-hidden="true">{{ viewport.is_mobile ? '▯' : '▭' }}</span>
          <div>
            <strong>{{ viewport.name }}</strong>
            <small>{{ viewport.width }}×{{ viewport.height }} · 溢出 {{ viewport.horizontal_overflow_px }}px</small>
          </div>
        </article>
      </div>
    </section>

    <div class="evidence-tabs">
      <div class="tab-list" role="tablist" aria-label="浏览器证据类型">
        <button
          v-for="(tab, index) in tabs"
          :key="tab.id"
          :ref="(element) => { if (element) tabButtons[index] = element as HTMLButtonElement }"
          type="button"
          role="tab"
          :id="`tab-${tab.id}`"
          :aria-controls="`panel-${tab.id}`"
          :aria-selected="activeTab === tab.id"
          :tabindex="activeTab === tab.id ? 0 : -1"
          @click="selectTab(tab.id)"
          @keydown="moveTab($event, index)"
        >
          {{ tab.label }}
          <span v-if="tab.id === 'steps'">{{ steps.length }}</span>
          <span v-else-if="tab.id === 'console'">{{ consoleEntries.length }}</span>
          <span v-else-if="tab.id === 'network'">{{ networkEntries.length }}</span>
          <span v-else>{{ screenshots.length }}</span>
        </button>
      </div>

      <div
        v-if="activeTab === 'steps'"
        id="panel-steps"
        class="tab-panel"
        role="tabpanel"
        aria-labelledby="tab-steps"
      >
          <ol class="timeline">
            <li
              v-for="step in visibleSteps"
              :key="`${step.viewport}-${step.step_id}`"
              :class="['timeline__entry', { 'timeline__entry--failed': step.status !== 'PASSED' }]"
            >
            <span class="timeline__mark" aria-hidden="true">{{ step.status === 'PASSED' ? '✓' : '×' }}</span>
            <div>
              <strong>{{ step.step_id }}</strong>
              <small>{{ step.viewport }} · {{ step.action }} · {{ step.elapsed_ms }}ms</small>
              <p v-if="step.error">{{ step.error }}</p>
            </div>
          </li>
        </ol>
      </div>

      <div
        v-else-if="activeTab === 'console'"
        id="panel-console"
        class="tab-panel"
        role="tabpanel"
        aria-labelledby="tab-console"
      >
        <div v-if="consoleEntries.length === 0" class="empty-inline">Console 没有持久化条目。</div>
        <ul v-else class="log-list">
          <li v-for="(entry, index) in visibleConsoleEntries" :key="`${entry.viewport}-${index}`" :class="`log--${entry.level}`">
            <span>{{ entry.level }}</span>
            <code>{{ entry.text }}</code>
            <small>{{ entry.viewport }}</small>
          </li>
        </ul>
      </div>

      <div
        v-else-if="activeTab === 'network'"
        id="panel-network"
        class="tab-panel"
        role="tabpanel"
        aria-labelledby="tab-network"
      >
        <div class="network-list">
          <article
            v-for="entry in visibleNetworkEntries"
            :key="`${entry.viewport}-${entry.sequence}`"
            :class="['network-row', { 'network-row--error': (entry.status ?? 0) >= 400 || entry.failure }]"
          >
            <span class="network-method">{{ entry.method }}</span>
            <code>{{ compactUrl(entry.url) }}</code>
            <span>{{ entry.status ?? 'FAILED' }}</span>
            <small>{{ entry.viewport }} · {{ entry.resource_type }}</small>
          </article>
        </div>
      </div>

      <div
        v-else
        id="panel-screenshots"
        class="tab-panel"
        role="tabpanel"
        aria-labelledby="tab-screenshots"
      >
        <div class="screenshot-grid">
          <button
            v-for="screenshot in visibleScreenshots"
            :key="screenshot.path"
            type="button"
            class="screenshot-card"
            :aria-label="`放大 ${screenshot.viewport} 截图 ${screenshot.name}`"
            data-testid="browser-screenshot-trigger"
            @click="openScreenshot(screenshot, $event)"
          >
            <img
              :src="imageUrls[screenshot.path]"
              :alt="`${screenshot.viewport} · ${screenshot.name}`"
              loading="lazy"
              decoding="async"
            />
            <span>
              <strong>{{ screenshot.viewport }}</strong>
              <small>{{ screenshot.name }} · {{ Math.ceil(screenshot.size / 1024) }} KiB</small>
            </span>
          </button>
        </div>
      </div>
    </div>

    <button
      v-if="summary"
      type="button"
      class="run-section-show-all browser-show-all"
      data-open-run-panel="browser"
      @click="emit('showAll')"
    >
      查看全部浏览器事实
    </button>

    <dialog ref="dialog" class="screenshot-dialog" @close="restoreFocus">
      <div v-if="selectedScreenshot" class="screenshot-dialog__body">
        <header>
          <div>
            <small>证据截图</small>
            <h3>{{ selectedScreenshot.viewport }} · {{ selectedScreenshot.name }}</h3>
          </div>
          <button type="button" class="icon-button" aria-label="关闭截图" @click="closeScreenshot">×</button>
        </header>
        <img
          :src="imageUrls[selectedScreenshot.path]"
          :alt="`${selectedScreenshot.viewport} · ${selectedScreenshot.name}`"
        />
        <code>{{ selectedScreenshot.sha256 }}</code>
      </div>
    </dialog>
  </div>
</template>
