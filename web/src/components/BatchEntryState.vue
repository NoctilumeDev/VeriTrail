<script setup lang="ts">
import { computed } from 'vue'

type BatchEntryMode = 'empty' | 'loading' | 'error'

const props = defineProps<{
  mode: BatchEntryMode
  error?: { code: string; message: string } | null
  kind?: 'invalid' | 'operational' | 'privacy'
}>()

const stateTitle = computed(() => {
  if (props.mode === 'loading') return '正在核验全因子批次卷宗'
  if (props.mode === 'error') return '批次卷宗需要重新选择'
  return '全因子批次待入册'
})

const stateDescription = computed(() => {
  if (props.mode === 'loading') return 'Manifest、BatchPlan seal 与完整矩阵正在本机内存中逐项比对。'
  if (props.mode === 'error') return props.error?.message ?? '所选批次文件未能进入可信展示。'
  return '请选择四份冻结文件；工作台只在本机内存中核验，不上传，也不持久化。'
})

const stateTestId = computed(() => {
  if (props.mode === 'loading') return 'loading-state'
  if (props.mode === 'error') return 'error-state'
  return 'batch-empty'
})
</script>

<template>
  <section
    class="batch-entry"
    :class="`batch-entry--${mode}`"
    aria-labelledby="view-batch-title"
    data-testid="batch-entry-state"
  >
    <header class="batch-entry__heading">
      <div class="batch-entry__title">
        <img :src="'/textures/r3-nav-batch.png'" alt="" aria-hidden="true" />
        <div>
          <p class="eyebrow">Batch Analysis · 万象院</p>
          <h2 id="view-batch-title" tabindex="-1" data-testid="view-batch-title">全因子批次分析</h2>
        </div>
      </div>
      <slot name="action" />
    </header>

    <div
      class="batch-entry__court"
      :role="mode === 'loading' ? 'status' : mode === 'error' ? 'alert' : undefined"
      :data-testid="stateTestId"
      :data-state-kind="mode === 'error' ? kind ?? 'invalid' : mode"
      aria-labelledby="batch-entry-title"
    >
      <div class="batch-entry__opening">
        <img :src="'/textures/r3-nav-batch.png'" alt="" aria-hidden="true" />
        <p class="eyebrow">Sealed Matrix · 四卷候核</p>
        <h3 id="batch-entry-title">{{ stateTitle }}</h3>
        <p>{{ stateDescription }}</p>
        <code v-if="mode === 'error' && error">{{ error.code }}</code>
      </div>

      <ol class="batch-entry__files" aria-label="批次分析四份冻结文件">
        <li><span>壹</span><strong>批次清单</strong><small>MANIFEST</small></li>
        <li><span>贰</span><strong>封存计划</strong><small>SEALED PLAN</small></li>
        <li><span>叁</span><strong>分析事实</strong><small>ANALYSIS JSON</small></li>
        <li><span>肆</span><strong>可读判词</strong><small>REPORT</small></li>
      </ol>
    </div>
  </section>
</template>
