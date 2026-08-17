<script setup lang="ts">
type PublicView = 'runs' | 'comparison' | 'pairing' | 'batch'

defineProps<{
  currentView: PublicView
}>()

const emit = defineEmits<{
  select: [view: PublicView]
}>()

const visualOrder: PublicView[] = ['pairing', 'runs', 'batch', 'comparison']
const targets: Record<PublicView, HTMLButtonElement | null> = {
  runs: null,
  comparison: null,
  pairing: null,
  batch: null,
}

const labels: Record<PublicView, string> = {
  runs: 'Runs / Catalog',
  comparison: 'Rerun Comparison',
  pairing: 'Paired Analysis',
  batch: 'Batch Analysis',
}

const icons: Record<PublicView, string> = {
  pairing: '/textures/r3-nav-pairing-thin.svg',
  runs: '/textures/r3-nav-runs.png',
  batch: '/textures/r3-nav-batch.png',
  comparison: '/textures/r3-nav-comparison.png',
}

function setTarget(view: PublicView, element: unknown) {
  targets[view] = element instanceof HTMLButtonElement ? element : null
}

function select(view: PublicView) {
  emit('select', view)
}

function moveFocus(view: PublicView) {
  targets[view]?.focus()
}

function handleTargetKeydown(event: KeyboardEvent, view: PublicView) {
  const currentIndex = visualOrder.indexOf(view)
  if (event.key === 'Home') {
    event.preventDefault()
    moveFocus(visualOrder[0])
    return
  }
  if (event.key === 'End') {
    event.preventDefault()
    moveFocus(visualOrder[visualOrder.length - 1])
    return
  }
  if (event.key !== 'ArrowLeft' && event.key !== 'ArrowRight') return
  event.preventDefault()
  const delta = event.key === 'ArrowLeft' ? -1 : 1
  const destination = visualOrder[(currentIndex + delta + visualOrder.length) % visualOrder.length]
  moveFocus(destination)
}
</script>

<template>
  <nav id="public-view-navigation" class="cross-axis-navigation" aria-label="公共分析视图">
    <ol class="cross-axis-navigation__waterline">
      <li v-for="(view, index) in visualOrder" :key="view">
        <button
          :ref="(element) => setTarget(view, element)"
          type="button"
          class="cross-axis-navigation__target"
          :class="`cross-axis-navigation__target--${view}`"
          :data-testid="`cross-axis-${view}`"
          :aria-current="currentView === view ? 'page' : undefined"
          @click="select(view)"
          @keydown="handleTargetKeydown($event, view)"
        >
          <span class="cross-axis-navigation__ordinal" aria-hidden="true">{{ index + 1 }}</span>
          <img class="cross-axis-navigation__mark" :src="icons[view]" alt="" aria-hidden="true" />
          <span class="cross-axis-navigation__label">{{ labels[view] }}</span>
        </button>
      </li>
    </ol>
  </nav>
</template>

<style scoped>
.cross-axis-navigation {
  width: min(100%, 86rem);
  color: var(--text-primary);
}

.cross-axis-navigation__waterline {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  position: relative;
  margin: 0;
  padding: 0 0 var(--space-4);
  list-style: none;
}

.cross-axis-navigation__waterline::after {
  position: absolute;
  right: 0;
  bottom: 0.35rem;
  left: 0;
  height: 1px;
  content: "";
  background: color-mix(in srgb, var(--structure-hairline) 78%, transparent);
}

.cross-axis-navigation__waterline > li {
  min-width: 0;
}

.cross-axis-navigation__target {
  display: grid;
  grid-template-columns: 2.1rem minmax(0, 1fr);
  align-items: center;
  width: 100%;
  min-height: 4.65rem;
  padding: var(--space-3) var(--space-4);
  color: var(--text-secondary);
  cursor: pointer;
  background: transparent;
  border: 0;
  font-family: var(--font-display);
  font-size: 1rem;
  text-align: left;
}

.cross-axis-navigation__target:hover,
.cross-axis-navigation__target:focus-visible,
.cross-axis-navigation__target[aria-current='page'] {
  color: var(--structure-vermilion);
}

.cross-axis-navigation__target:focus-visible {
  z-index: 1;
  outline: 3px solid var(--focus-ring);
  outline-offset: -3px;
}

.cross-axis-navigation__target[aria-current='page']::after {
  position: absolute;
  bottom: 0.28rem;
  left: 50%;
  width: 4rem;
  height: 2px;
  content: "";
  background: currentColor;
  transform: translateX(-50%);
}

.cross-axis-navigation__ordinal {
  display: grid;
  width: 1.65rem;
  height: 1.65rem;
  place-items: center;
  color: var(--structure-gold);
  font-family: var(--font-display);
  font-size: 0.95rem;
  border: 1px solid currentColor;
  border-radius: 50%;
}

.cross-axis-navigation__mark {
  display: none;
}

.cross-axis-navigation__target[aria-current='page'] .cross-axis-navigation__ordinal {
  color: var(--text-on-ink);
  background: var(--structure-vermilion);
  border-color: var(--structure-vermilion);
}

@media (forced-colors: active) {
  .cross-axis-navigation__waterline::after {
    background: CanvasText;
  }

  .cross-axis-navigation__target,
  .cross-axis-navigation__ordinal {
    color: CanvasText;
    border-color: CanvasText;
  }

  .cross-axis-navigation__target[aria-current='page'] {
    color: HighlightText;
    background: Highlight;
  }
}

@media (max-width: 40rem) {
  .cross-axis-navigation__waterline {
    grid-template-columns: repeat(2, minmax(0, 1fr));
    row-gap: var(--space-1);
  }

  .cross-axis-navigation__target {
    min-height: 4.25rem;
    padding-inline: var(--space-2);
    font-size: 0.9rem;
  }
}

</style>
