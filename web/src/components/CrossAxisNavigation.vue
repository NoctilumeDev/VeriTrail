<script setup lang="ts">
import { nextTick, ref } from 'vue'

type PublicView = 'runs' | 'comparison' | 'pairing' | 'batch'

const props = defineProps<{
  currentView: PublicView
  expanded: boolean
}>()

const emit = defineEmits<{
  toggle: [expanded: boolean]
  select: [view: PublicView]
}>()

const centerButton = ref<HTMLButtonElement | null>(null)
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

function setTarget(view: PublicView, element: unknown) {
  targets[view] = element instanceof HTMLButtonElement ? element : null
}

function toggle() {
  emit('toggle', !props.expanded)
}

function select(view: PublicView) {
  emit('select', view)
}

function moveFocus(view: PublicView) {
  targets[view]?.focus()
}

function handleCenterKeydown(event: KeyboardEvent) {
  if (event.key !== 'Escape') return
  if (props.expanded) {
    event.preventDefault()
    emit('toggle', false)
  }
}

function handleTargetKeydown(event: KeyboardEvent, view: PublicView) {
  if (event.key === 'Escape') {
    event.preventDefault()
    emit('toggle', false)
    void nextTick(() => centerButton.value?.focus())
    return
  }

  const directions: Record<PublicView, Partial<Record<string, PublicView>>> = {
    runs: { ArrowRight: 'batch', ArrowDown: 'comparison', ArrowLeft: 'pairing' },
    batch: { ArrowLeft: 'pairing', ArrowDown: 'comparison', ArrowUp: 'runs' },
    comparison: { ArrowUp: 'runs', ArrowLeft: 'pairing', ArrowRight: 'batch' },
    pairing: { ArrowRight: 'batch', ArrowUp: 'runs', ArrowDown: 'comparison' },
  }
  const destination = directions[view][event.key]
  if (!destination) return
  event.preventDefault()
  moveFocus(destination)
}
</script>

<template>
  <nav class="cross-axis-navigation" aria-label="公共分析视图">
    <div class="cross-axis-navigation__stage">
      <button
        ref="centerButton"
        type="button"
        class="cross-axis-navigation__center"
        data-testid="cross-axis-toggle"
        :aria-expanded="expanded"
        aria-controls="cross-axis-targets"
        @click="toggle"
        @keydown="handleCenterKeydown"
      >
        <span>目录</span>
        <strong>{{ labels[currentView] }}</strong>
      </button>

      <div v-if="expanded" id="cross-axis-targets" class="cross-axis-navigation__targets">
        <button
          :ref="(element) => setTarget('runs', element)"
          type="button"
          class="cross-axis-navigation__target cross-axis-navigation__target--north"
          data-testid="cross-axis-runs"
          :aria-current="currentView === 'runs' ? 'page' : undefined"
          @click="select('runs')"
          @keydown="handleTargetKeydown($event, 'runs')"
        >
          Runs / Catalog
        </button>
        <button
          :ref="(element) => setTarget('batch', element)"
          type="button"
          class="cross-axis-navigation__target cross-axis-navigation__target--east"
          data-testid="cross-axis-batch"
          :aria-current="currentView === 'batch' ? 'page' : undefined"
          @click="select('batch')"
          @keydown="handleTargetKeydown($event, 'batch')"
        >
          Batch Analysis
        </button>
        <button
          :ref="(element) => setTarget('comparison', element)"
          type="button"
          class="cross-axis-navigation__target cross-axis-navigation__target--south"
          data-testid="cross-axis-comparison"
          :aria-current="currentView === 'comparison' ? 'page' : undefined"
          @click="select('comparison')"
          @keydown="handleTargetKeydown($event, 'comparison')"
        >
          Rerun Comparison
        </button>
        <button
          :ref="(element) => setTarget('pairing', element)"
          type="button"
          class="cross-axis-navigation__target cross-axis-navigation__target--west"
          data-testid="cross-axis-pairing"
          :aria-current="currentView === 'pairing' ? 'page' : undefined"
          @click="select('pairing')"
          @keydown="handleTargetKeydown($event, 'pairing')"
        >
          Paired Analysis
        </button>
      </div>
    </div>
  </nav>
</template>

<style scoped>
.cross-axis-navigation {
  padding: 1rem;
  border: 1px solid color-mix(in srgb, var(--structure-gold) 70%, var(--surface-ink));
  background: color-mix(in srgb, var(--surface-ink-raised) 88%, var(--surface-ink));
  color: var(--text-on-ink);
}

.cross-axis-navigation__stage {
  position: relative;
  block-size: 10.5rem;
}

.cross-axis-navigation__center,
.cross-axis-navigation__target {
  min-inline-size: 11rem;
  min-block-size: 2.75rem;
  border: 1px solid var(--structure-gold);
  border-radius: 0;
  background: var(--surface-ink-raised);
  color: var(--text-on-ink);
  font: inherit;
}

.cross-axis-navigation__center {
  display: grid;
  gap: 0.2rem;
  position: absolute;
  inset: 50% auto auto 50%;
  transform: translate(-50%, -50%);
  z-index: 1;
  color: var(--text-primary);
  background: var(--surface-courtyard);
  box-shadow: inset 0 0 0 3px color-mix(in srgb, var(--structure-gold) 18%, transparent);
}

.cross-axis-navigation__center span {
  font-size: 0.78rem;
}

.cross-axis-navigation__center strong {
  font-size: 0.95rem;
}

.cross-axis-navigation__targets {
  display: grid;
  grid-template-columns: minmax(7rem, 1fr) minmax(11rem, 1.2fr) minmax(7rem, 1fr);
  grid-template-rows: repeat(3, minmax(2.75rem, auto));
  gap: 0.5rem;
  position: absolute;
  inset: 0;
}

.cross-axis-navigation__target {
  min-inline-size: 0;
}

.cross-axis-navigation__target--north {
  grid-column: 2;
  grid-row: 1;
}

.cross-axis-navigation__target--east {
  grid-column: 3;
  grid-row: 2;
}

.cross-axis-navigation__target--south {
  grid-column: 2;
  grid-row: 3;
}

.cross-axis-navigation__target--west {
  grid-column: 1;
  grid-row: 2;
}

.cross-axis-navigation__center {
  grid-column: 2;
  grid-row: 2;
}

button:hover,
button:focus-visible,
button[aria-current='page'] {
  outline: 3px solid var(--focus-ring);
  outline-offset: 2px;
}

.cross-axis-navigation__target:hover,
.cross-axis-navigation__target[aria-current='page'] {
  color: var(--text-primary);
  background: var(--structure-gold);
}

@media (forced-colors: active) {
  .cross-axis-navigation,
  .cross-axis-navigation__center,
  .cross-axis-navigation__target {
    color: CanvasText;
    background: Canvas;
    border-color: CanvasText;
  }

  button:hover,
  button:focus-visible,
  button[aria-current='page'] {
    outline-color: Highlight;
  }
}

@media (max-width: 32rem) {
  .cross-axis-navigation {
    padding-inline: 0.5rem;
  }

  .cross-axis-navigation__stage {
    block-size: 12rem;
  }

  .cross-axis-navigation__center {
    box-sizing: border-box;
    inline-size: 5.75rem;
    min-inline-size: 0;
    padding: 0.2rem;
    gap: 0;
  }

  .cross-axis-navigation__center span {
    font-size: 0.7rem;
  }

  .cross-axis-navigation__center strong {
    font-size: 0.82rem;
    line-height: 1.1;
  }

  .cross-axis-navigation__targets {
    grid-template-columns: minmax(0, 1fr) minmax(0, 1.2fr) minmax(0, 1fr);
    gap: 0.25rem;
  }

  .cross-axis-navigation__target {
    font-size: 0.82rem;
  }
}

@media (prefers-reduced-motion: reduce) {
  * {
    transition-duration: 0ms !important;
  }
}
</style>
