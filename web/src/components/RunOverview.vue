<script setup lang="ts">
import { computed, ref } from 'vue'
import type { VerdictReport } from '../domain/types'
import SectionFrame from './SectionFrame.vue'

const props = defineProps<{
  report: VerdictReport
}>()

const applicabilityOpen = ref(false)
const overviewOpen = ref(false)

function pretty(value: unknown): string {
  if (typeof value === 'string') return value
  return JSON.stringify(value, null, 2)
}

function syncApplicabilityState(event: Event) {
  applicabilityOpen.value = (event.currentTarget as HTMLDetailsElement).open
}

const hasOverviewOverflow = computed(() => {
  const values = [
    props.report.baseline?.id,
    props.report.baseline?.status,
    props.report.primary_variable?.name,
    props.report.primary_variable?.value,
    props.report.load_model,
    props.report.change_scope?.level,
    props.report.change_scope?.owner,
  ]
  return values.some((value) => pretty(value ?? '').length > 24)
})
</script>

<template>
  <SectionFrame class="run-section--overview" title="结论总览" kicker="Overview · 前朝" section-id="overview-title">
    <div class="reason-banner" :class="`reason-banner--${report.verdict.toLowerCase()}`">
      <span aria-hidden="true">{{ report.verdict === 'PASS' ? '✓' : report.verdict === 'FAIL' ? '×' : '?' }}</span>
      <div>
        <small>确定性裁决原因</small>
        <strong>{{ report.reasons[0]?.code }}</strong>
        <p>{{ report.reasons[0]?.message }}</p>
      </div>
    </div>

    <div id="overview-facts" :class="['overview-grid', { 'overview-grid--expanded': overviewOpen }]">
      <article class="fact-card">
        <p>比较基线</p>
        <strong :title="String(report.baseline?.id ?? '未声明')">{{ report.baseline?.id ?? '未声明' }}</strong>
        <code :title="pretty(report.baseline?.status ?? 'UNKNOWN')">{{ pretty(report.baseline?.status ?? 'UNKNOWN') }}</code>
      </article>
      <article class="fact-card">
        <p>唯一主要变量</p>
        <strong :title="String(report.primary_variable?.name ?? '未声明')">{{ report.primary_variable?.name ?? '未声明' }}</strong>
        <code :title="pretty(report.primary_variable?.value ?? null)">{{ pretty(report.primary_variable?.value ?? null) }}</code>
      </article>
      <article class="fact-card">
        <p>负载语义</p>
        <strong :title="`${Object.keys(report.load_model ?? {}).length} 个维度`">{{ Object.keys(report.load_model ?? {}).length }} 个维度</strong>
        <code :title="pretty(report.load_model ?? {})">{{ pretty(report.load_model ?? {}) }}</code>
      </article>
      <article class="fact-card">
        <p>影响层级</p>
        <strong :title="String(report.change_scope?.level ?? '未声明')">{{ report.change_scope?.level ?? '未声明' }}</strong>
        <code :title="pretty(report.change_scope?.owner ?? 'UNKNOWN')">{{ pretty(report.change_scope?.owner ?? 'UNKNOWN') }}</code>
      </article>
    </div>

    <button
      v-if="hasOverviewOverflow"
      type="button"
      class="overview-expand"
      :aria-expanded="overviewOpen"
      aria-controls="overview-facts"
      @click="overviewOpen = !overviewOpen"
    >
      {{ overviewOpen ? '收起完整结论字段' : '展开完整结论字段' }}
    </button>

    <details class="applicability" @toggle="syncApplicabilityState">
      <summary>{{ applicabilityOpen ? '收起适用边界与资源预算' : '展开适用边界与资源预算' }}</summary>
      <div>
        <article><h3>Subject</h3><pre>{{ pretty(report.subject ?? {}) }}</pre></article>
        <article><h3>Resource budget</h3><pre>{{ pretty(report.resource_budget ?? {}) }}</pre></article>
        <article><h3>Change scope</h3><pre>{{ pretty(report.change_scope ?? {}) }}</pre></article>
      </div>
    </details>
  </SectionFrame>
</template>
