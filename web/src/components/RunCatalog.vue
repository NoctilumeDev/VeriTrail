<script setup lang="ts">
import StatusBadge from './StatusBadge.vue'
import type { CatalogResponse, CatalogRunSummary } from '../domain/types'

defineProps<{
  catalog: CatalogResponse | null
  loading: boolean
  error: { code: string; message: string } | null
  selectedRunId: string | null
}>()

const emit = defineEmits<{
  select: [run: CatalogRunSummary, trigger: HTMLElement]
  retry: []
}>()

function selectRun(run: CatalogRunSummary, event: Event) {
  emit('select', run, event.currentTarget as HTMLElement)
}

function displayDate(value: string): string {
  const date = new Date(value)
  return Number.isNaN(date.valueOf()) ? value : date.toLocaleString('zh-CN', { hour12: false })
}
</script>

<template>
  <section
    class="catalog-court"
    aria-labelledby="catalog-title"
    data-testid="run-catalog"
  >
    <header class="catalog-court__heading">
      <div>
        <p class="eyebrow">Run Catalog · 午门</p>
        <h2 id="catalog-title">本地 Run 目录</h2>
      </div>
      <span v-if="catalog" class="catalog-readonly">只读快照 · {{ catalog.catalog.run_count }} Runs</span>
    </header>

    <div v-if="loading" class="catalog-message" role="status" data-testid="catalog-loading">
      正在确认本地目录是否存在
    </div>

    <div v-else-if="error" class="catalog-message catalog-message--error" data-testid="catalog-error">
      <div>
        <strong>目录读取失败，但没有改写任何 Run 裁决</strong>
        <p>{{ error.message }} · <code>{{ error.code }}</code></p>
      </div>
      <button type="button" data-testid="catalog-retry" @click="emit('retry')">重试目录</button>
    </div>

    <template v-else-if="catalog">
      <div v-if="catalog.runs.length === 0" class="catalog-empty" data-testid="catalog-empty">
        <span aria-hidden="true">空</span>
        <div>
          <strong>目录有效，暂无 Run</strong>
          <p>这是 Catalog 的空集合状态，不是 Run 的 PENDING 裁决。</p>
        </div>
      </div>

      <div v-else class="catalog-runs" data-testid="catalog-runs">
        <button
          v-for="run in catalog.runs"
          :key="run.catalog_run_id"
          type="button"
          class="catalog-run"
          :class="{ 'is-selected': selectedRunId === run.catalog_run_id }"
          :aria-current="selectedRunId === run.catalog_run_id ? 'true' : undefined"
          :data-catalog-run-id="run.catalog_run_id"
          @click="selectRun(run, $event)"
        >
          <span class="catalog-run__identity">
            <small>Run</small>
            <strong>{{ run.run_id }}</strong>
            <em>{{ displayDate(run.created_at) }}</em>
          </span>
          <span class="catalog-run__status">
            <StatusBadge dimension="execution" :value="run.execution_status" compact />
            <StatusBadge dimension="verdict" :value="run.verdict" compact />
          </span>
          <span class="catalog-run__facts">
            <small>{{ run.plan.id }} · v{{ run.plan.version }}</small>
            <em>{{ run.bundle.file_count }} 文件 · {{ run.bundle.duplicate_count }} 重复</em>
          </span>
        </button>
      </div>

      <aside
        v-if="catalog.issues.length"
        class="catalog-issues"
        aria-labelledby="catalog-issues-title"
        data-testid="catalog-issues"
      >
        <div>
          <p class="eyebrow">Catalog Diagnostics · 独立于 Run</p>
          <h3 id="catalog-issues-title">目录问题 {{ catalog.catalog.issue_count }} 项</h3>
        </div>
        <ul>
          <li v-for="issue in catalog.issues" :key="issue.issue_id">
            <code>{{ issue.code }}</code>
            <span>{{ issue.run_id ?? issue.candidate_id }} · {{ issue.occurrence_count }} 个候选</span>
          </li>
        </ul>
        <p v-if="catalog.issues_truncated">这里只显示前 100 项稳定摘要。</p>
      </aside>
    </template>
  </section>
</template>
