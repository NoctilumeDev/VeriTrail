<script setup lang="ts">
import { computed } from 'vue'
import { PAIRING_ROLES, PAIRING_ROLE_META } from './pairingPresentation'

type PairingEntryMode = 'empty' | 'loading' | 'error'

const props = defineProps<{
  mode: PairingEntryMode
  error?: { code: string; message: string } | null
}>()

const stateTitle = computed(() => {
  if (props.mode === 'loading') return '正在核验四角色配对卷宗'
  if (props.mode === 'error') return '配对卷宗需要重新选择'
  return '四象待入册'
})

const stateDescription = computed(() => {
  if (props.mode === 'loading') return 'Manifest、PairingPlan seal 与来源交叉引用正在本机内存中逐项比对。'
  if (props.mode === 'error') return props.error?.message ?? '所选配对文件未能进入可信展示。'
  return '请选择四份冻结文件；工作台只在本机内存中核验，不上传，也不持久化。'
})

const stateTestId = computed(() => {
  if (props.mode === 'loading') return 'loading-state'
  if (props.mode === 'error') return 'error-state'
  return 'pairing-empty'
})

const stateRole = computed(() => {
  if (props.mode === 'loading') return 'status'
  if (props.mode === 'error') return 'alert'
  return undefined
})
</script>

<template>
  <section
    class="pairing-page pairing-page--entry"
    :class="`pairing-page--entry-${mode}`"
    aria-labelledby="view-pairing-title"
    data-testid="pairing-entry-state"
  >
    <header class="pairing-heading pairing-heading--entry">
      <div class="pairing-heading__title">
        <img :src="'/textures/r3-nav-pairing-thin.svg'" alt="" aria-hidden="true" />
        <div>
          <p class="eyebrow">Paired Analysis · 四象殿</p>
          <h2 id="view-pairing-title" tabindex="-1" data-testid="view-pairing-title">配对实验</h2>
        </div>
      </div>
      <div class="pairing-heading__actions">
        <slot name="action" />
      </div>
    </header>

    <div
      class="pairing-entry-court"
      :role="stateRole"
      :data-testid="stateTestId"
      :data-state-kind="mode"
      aria-labelledby="pairing-entry-state-title"
    >
      <div class="pairing-entry-court__opening">
        <p class="eyebrow">Pairing Ledger · 四序候核</p>
        <h3 id="pairing-entry-state-title">{{ stateTitle }}</h3>
        <p>{{ stateDescription }}</p>
        <code v-if="mode === 'error' && error">{{ error.code }}</code>
      </div>

      <ol class="pairing-entry-roles" aria-label="四角色配对文件要求">
        <li v-for="(role, index) in PAIRING_ROLES" :key="role">
          <span>{{ index + 1 }}</span>
          <img :src="'/textures/pairing-palace-hall-line.png'" alt="" aria-hidden="true" />
          <strong>{{ PAIRING_ROLE_META[role].chinese }}</strong>
          <small>{{ PAIRING_ROLE_META[role].english }}</small>
          <em>{{ mode === 'loading' ? '核验中' : '待选择' }}</em>
        </li>
      </ol>
    </div>
  </section>
</template>
