<script setup lang="ts">
import PairingPanelShell from './PairingPanelShell.vue'
import { PAIRING_ROLES, PAIRING_ROLE_META, pairingValue } from './pairingPresentation'
import type { LoadedPairedAnalysis, PairedOutcome } from '../domain/types'

defineProps<{ loaded: LoadedPairedAnalysis }>()

const emit = defineEmits<{
  close: []
}>()

function outcomeMatches(outcome: PairedOutcome): number {
  return PAIRING_ROLES.filter((role) => outcome.roles[role].matches).length
}
</script>

<template>
  <PairingPanelShell
    introduction="每项断言同时展示四角色预期与实测，不以摘要替代原始对照事实。"
    @close="emit('close')"
  >
    <div class="pairing-outcome-ledger" data-testid="paired-outcomes">
      <article v-for="(outcome, outcomeIndex) in loaded.analysis.outcomes" :key="outcome.assertion_id">
        <header>
          <span>{{ String(outcomeIndex + 1).padStart(2, '0') }}</span>
          <div>
            <p>Preregistered assertion</p>
            <h3>{{ outcome.assertion_id }}</h3>
          </div>
          <strong>{{ outcomeMatches(outcome) }}/{{ PAIRING_ROLES.length }} 吻合</strong>
        </header>
        <div class="pairing-outcome-ledger__roles">
          <section
            v-for="role in PAIRING_ROLES"
            :key="role"
            :class="{ 'is-mismatch': !outcome.roles[role].matches }"
            :data-pairing-role="role"
          >
            <header>
              <strong>{{ PAIRING_ROLE_META[role].chinese }}</strong>
              <span>{{ outcome.roles[role].matches ? '吻合' : '不符' }}</span>
            </header>
            <dl>
              <div><dt>Expected</dt><dd><code>{{ pairingValue(outcome.roles[role].expected_actual) }}</code></dd></div>
              <div><dt>Actual</dt><dd><code>{{ pairingValue(outcome.roles[role].actual) }}</code></dd></div>
            </dl>
          </section>
        </div>
      </article>
    </div>
  </PairingPanelShell>
</template>
