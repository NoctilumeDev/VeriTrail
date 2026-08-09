<script setup lang="ts">
import type { ExecutionStatus, Verdict } from '../domain/types'

defineProps<{
  dimension: 'execution' | 'verdict'
  value: ExecutionStatus | Verdict
  compact?: boolean
}>()

const icons: Record<string, string> = {
  PASS: '✓',
  FAIL: '×',
  INCONCLUSIVE: '?',
  PENDING: '…',
  PLANNED: '○',
  RUNNING: '↻',
  COMPLETED: '✓',
  ABORTED: '■',
  ERROR: '!',
}

const dimensionLabels = {
  execution: '运行状态',
  verdict: '验收结论',
}
</script>

<template>
  <div
    class="status-badge"
    :class="[`status-badge--${dimension}`, `status--${value.toLowerCase()}`, { 'status-badge--compact': compact }]"
    :aria-label="`${dimensionLabels[dimension]}：${value}`"
  >
    <span class="status-badge__icon" aria-hidden="true">{{ icons[value] }}</span>
    <span class="status-badge__copy">
      <small>{{ dimensionLabels[dimension] }}</small>
      <strong>{{ value }}</strong>
    </span>
  </div>
</template>
