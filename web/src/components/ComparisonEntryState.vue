<script setup lang="ts">
import { computed } from 'vue'

type ComparisonEntryMode = 'empty' | 'loading' | 'error'

const props = defineProps<{
  mode: ComparisonEntryMode
  error?: { code: string; message: string } | null
}>()

const stateTitle = computed(() => {
  if (props.mode === 'loading') return '正在核验复跑比较卷宗'
  if (props.mode === 'error') return '比较卷宗需要重新选择'
  return '两次独立 Run 待入对照轴'
})

const stateDescription = computed(() => {
  if (props.mode === 'loading') return 'Manifest、文件大小、路径与 SHA-256 正在本机内存中逐项比对。'
  if (props.mode === 'error') return props.error?.message ?? '所选比较文件未能进入可信展示。'
  return '请选择同一计划下两次独立运行的 Comparison 目录；文件只在本机内存中核验。'
})

const stateTestId = computed(() => {
  if (props.mode === 'loading') return 'loading-state'
  if (props.mode === 'error') return 'error-state'
  return 'comparison-empty'
})
</script>

<template>
  <section
    class="rerun-page rerun-page--entry"
    :class="`rerun-page--entry-${mode}`"
    aria-labelledby="view-comparison-title"
    data-testid="comparison-entry-state"
  >
    <header class="rerun-heading rerun-heading--entry">
      <div class="rerun-heading__title">
        <img :src="'/textures/r3-nav-comparison.png'" alt="" aria-hidden="true" />
        <div>
          <p class="eyebrow">Rerun Comparison · 对照殿</p>
          <h2 id="view-comparison-title" tabindex="-1" data-testid="view-comparison-title">复跑比较</h2>
        </div>
      </div>
      <div class="rerun-heading__actions">
        <slot name="action" />
      </div>
    </header>

    <div
      class="rerun-entry-court"
      :role="mode === 'loading' ? 'status' : mode === 'error' ? 'alert' : undefined"
      :data-testid="stateTestId"
      :data-state-kind="mode"
      aria-labelledby="rerun-entry-title"
    >
      <div class="rerun-entry-court__opening">
        <p class="eyebrow">Same Plan · Independent Runs</p>
        <h3 id="rerun-entry-title">{{ stateTitle }}</h3>
        <p>{{ stateDescription }}</p>
        <code v-if="mode === 'error' && error">{{ error.code }}</code>
      </div>

      <div class="rerun-entry-axis" aria-label="复跑比较需要的两个来源">
        <div>
          <span>壹</span>
          <strong>基线 Run</strong>
          <small>BASELINE</small>
        </div>
        <img :src="'/textures/r3-nav-comparison.png'" alt="" aria-hidden="true" />
        <div>
          <span>贰</span>
          <strong>重复 Run</strong>
          <small>REPEAT</small>
        </div>
      </div>
    </div>
  </section>
</template>
