<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import type { ReportAssertion, VerdictReport } from '../domain/types'
import SectionFrame from './SectionFrame.vue'

type AssertionFilter = 'ALL' | 'PASS' | 'FAIL' | 'OTHER'

const props = defineProps<{
  report: VerdictReport
  full: boolean
}>()

const emit = defineEmits<{
  showAll: []
}>()

const filter = ref<AssertionFilter>('ALL')
const filters = ['ALL', 'PASS', 'FAIL', 'OTHER'] as const
const filteredAssertions = computed(() => {
  if (filter.value === 'ALL') return props.report.assertions
  if (filter.value === 'OTHER') return props.report.assertions.filter((item) => !['PASS', 'FAIL'].includes(item.status))
  return props.report.assertions.filter((item) => item.status === filter.value)
})
const counts = computed(() => ({
  ALL: props.report.assertions.length,
  PASS: props.report.assertions.filter((item) => item.status === 'PASS').length,
  FAIL: props.report.assertions.filter((item) => item.status === 'FAIL').length,
  OTHER: props.report.assertions.filter((item) => !['PASS', 'FAIL'].includes(item.status)).length,
}))
const visibleAssertions = computed(() => props.full ? filteredAssertions.value : filteredAssertions.value.slice(0, 3))

watch(() => props.report.run_id, () => { filter.value = 'ALL' })

function pretty(value: unknown): string {
  if (typeof value === 'string') return value
  return JSON.stringify(value, null, 2)
}

function assertionStatusClass(assertion: ReportAssertion): string {
  return `assertion--${assertion.status.toLowerCase()}`
}
</script>

<template>
  <SectionFrame
    :class="['run-section--assertions', { 'run-section--standalone': full }]"
    title="确定性断言"
    kicker="Assertions · 中庭"
    section-id="assertions-title"
  >
    <template #actions>
      <div class="filter-group" aria-label="断言状态筛选">
        <button
          v-for="item in filters"
          :key="item"
          type="button"
          :aria-pressed="filter === item"
          :data-testid="`filter-${item.toLowerCase()}`"
          @click="filter = item"
        >
          {{ item === 'ALL' ? '全部' : item === 'OTHER' ? '其他' : item }}
          <span>{{ counts[item] }}</span>
        </button>
      </div>
    </template>

    <div class="assertion-list" data-testid="assertion-list">
      <article
        v-for="assertion in visibleAssertions"
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
      <p v-if="filteredAssertions.length === 0" class="assertion-list__empty" data-testid="assertion-filter-empty">
        当前筛选条件下没有断言记录。
      </p>
    </div>

    <button
      v-if="!full"
      type="button"
      class="run-section-show-all"
      data-open-run-panel="assertions"
      @click="emit('showAll')"
    >
      查看全部 {{ filteredAssertions.length }} 项断言
    </button>
  </SectionFrame>
</template>
