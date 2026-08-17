<script setup lang="ts">
import { computed, ref } from 'vue'
import type { VerdictReport } from '../domain/types'
import SectionFrame from './SectionFrame.vue'

const props = defineProps<{
  report: VerdictReport
}>()

const previewLimit = 3
const expanded = ref(false)

const missingEvidence = computed(() => props.report.missing_evidence ?? [])
const contamination = computed(() => props.report.contamination ?? [])
const reproductionSteps = computed(() => props.report.reproduction_steps ?? [])
const cleanupSteps = computed(() => props.report.cleanup_steps ?? [])
const hasHiddenContent = computed(() =>
  [missingEvidence.value, contamination.value, reproductionSteps.value, cleanupSteps.value]
    .some((items) => items.length > previewLimit),
)

function visibleItems<T>(items: T[]): T[] {
  return expanded.value ? items : items.slice(0, previewLimit)
}

function pretty(value: unknown): string {
  if (typeof value === 'string') return value
  return JSON.stringify(value, null, 2)
}
</script>

<template>
  <SectionFrame class="run-section--boundary" title="缺口、复现与清理" kicker="Boundary · 后寝" section-id="boundary-title">
    <div id="boundary-ledger" class="boundary-grid">
      <article>
        <h3>证据缺口</h3>
        <p v-if="missingEvidence.length === 0" class="quiet-pass">未记录缺失证据</p>
        <ul v-else><li v-for="item in visibleItems(missingEvidence)" :key="item">{{ item }}</li></ul>
      </article>
      <article>
        <h3>污染清单</h3>
        <p v-if="contamination.length === 0" class="quiet-pass">未记录环境污染</p>
        <pre v-else>{{ pretty(visibleItems(contamination)) }}</pre>
      </article>
      <article>
        <h3>复现步骤</h3>
        <ol><li v-for="item in visibleItems(reproductionSteps)" :key="item">{{ item }}</li></ol>
      </article>
      <article>
        <h3>清理步骤</h3>
        <ol><li v-for="item in visibleItems(cleanupSteps)" :key="item">{{ item }}</li></ol>
      </article>
    </div>
    <button
      v-if="hasHiddenContent"
      type="button"
      class="run-section-show-all boundary-show-all"
      :aria-expanded="expanded"
      aria-controls="boundary-ledger"
      @click="expanded = !expanded"
    >
      {{ expanded ? '收起完整边界信息' : '展开完整边界信息' }}
    </button>
  </SectionFrame>
</template>
