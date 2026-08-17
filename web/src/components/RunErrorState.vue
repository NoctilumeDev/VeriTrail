<script setup lang="ts">
defineProps<{
  error: { code: string; message: string }
  kind: 'invalid' | 'operational' | 'privacy'
  retryMode: 'catalog' | 'positive'
  retryDisabled?: boolean
}>()

const emit = defineEmits<{
  dismiss: []
  retry: []
}>()
</script>

<template>
  <section
    id="run-error-state"
    :class="['run-error-court', `run-error-court--${kind}`]"
    :data-state-kind="kind"
    aria-labelledby="error-title"
    data-testid="error-state"
  >
    <button
      type="button"
      class="run-error-court__seal"
      aria-label="收起损坏证据提示"
      data-testid="dismiss-invalid-state"
      @click="emit('dismiss')"
    >
      止
    </button>
    <p class="eyebrow">证据包未进入可信展示</p>
    <h2 id="error-title">{{ error.message }}</h2>
    <code>{{ error.code }}</code>
    <p>工作台没有据此改写 Run 的 Verdict，也没有展示部分可信内容。</p>
    <button
      type="button"
      :data-testid="retryMode === 'catalog' ? 'retry-catalog-run' : 'retry-positive'"
      :disabled="retryDisabled"
      @click="emit('retry')"
    >
      {{ retryMode === 'catalog' ? '重新读取目录 Run' : '返回正向证据重试' }}
    </button>
  </section>
</template>
