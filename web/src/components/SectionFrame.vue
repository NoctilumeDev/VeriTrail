<script setup lang="ts">
defineProps<{
  title: string
  kicker: string
  sectionId?: string
}>()
</script>

<template>
  <section class="courtyard" :aria-labelledby="sectionId">
    <header class="courtyard__heading">
      <div>
        <p class="courtyard__kicker">{{ kicker }}</p>
        <h2 :id="sectionId">{{ title }}</h2>
      </div>
      <div v-if="$slots.actions" class="courtyard__actions">
        <slot name="actions" />
      </div>
    </header>
    <div class="courtyard__body">
      <slot />
    </div>
  </section>
</template>
