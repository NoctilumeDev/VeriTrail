<script setup lang="ts">
defineProps<{ introduction: string }>()

const emit = defineEmits<{
  close: []
}>()
</script>

<template>
  <div class="pairing-court pairing-court--panel" data-testid="pairing-panel-court">
    <p class="pairing-panel-introduction">{{ introduction }}</p>
    <slot />
    <nav class="pairing-panel-return" aria-label="配对实验返回操作">
      <button type="button" data-testid="pairing-panel-return" @click="emit('close')">返回配对实验</button>
    </nav>
  </div>
</template>
