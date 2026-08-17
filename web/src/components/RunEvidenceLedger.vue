<script setup lang="ts">
import { computed } from 'vue'
import type { VerdictReport } from '../domain/types'
import SectionFrame from './SectionFrame.vue'

const props = defineProps<{
  report: VerdictReport
  full: boolean
}>()

const emit = defineEmits<{
  showAll: []
}>()

const visibleEvidence = computed(() => props.full ? props.report.evidence : props.report.evidence.slice(0, 3))

function shortHash(value: string): string {
  return `${value.slice(0, 12)}…${value.slice(-8)}`
}

function formatBytes(bytes: number): string {
  if (bytes < 1024) return `${bytes} B`
  return `${(bytes / 1024).toFixed(1)} KiB`
}
</script>

<template>
  <SectionFrame
    :class="['run-section--ledger', { 'run-section--standalone': full }]"
    title="证据账册"
    kicker="Evidence Ledger · 东庑"
    section-id="ledger-title"
  >
    <div class="ledger" data-testid="evidence-ledger">
      <article v-for="artifact in visibleEvidence" :key="artifact.sha256" class="ledger-row">
        <div class="ledger-row__type">
          <span aria-hidden="true">档</span>
          <div>
            <strong>{{ artifact.evidence_type }}</strong>
            <small>{{ artifact.source }}</small>
          </div>
        </div>
        <dl>
          <div>
            <dt>SHA-256</dt>
            <dd><code :title="artifact.sha256">{{ full ? artifact.sha256 : shortHash(artifact.sha256) }}</code></dd>
          </div>
          <div><dt>大小</dt><dd>{{ formatBytes(artifact.size) }}</dd></div>
          <div><dt>脱敏</dt><dd>{{ artifact.redacted ? `是 · ${artifact.redacted_fields}` : '无命中' }}</dd></div>
          <div><dt>解析器</dt><dd>{{ artifact.parser_version }}</dd></div>
        </dl>
      </article>
    </div>

    <button
      v-if="!full"
      type="button"
      class="run-section-show-all"
      data-open-run-panel="ledger"
      @click="emit('showAll')"
    >
      查看全部 {{ report.evidence.length }} 项证据
    </button>
  </SectionFrame>
</template>
