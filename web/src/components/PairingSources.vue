<script setup lang="ts">
import PairingPanelShell from './PairingPanelShell.vue'
import StatusBadge from './StatusBadge.vue'
import {
  PAIRING_ROLES,
  PAIRING_ROLE_META,
  pairingDisplayDate,
  pairingShortHash,
  pairingValue,
} from './pairingPresentation'
import type { LoadedPairedAnalysis } from '../domain/types'

defineProps<{ loaded: LoadedPairedAnalysis }>()

const emit = defineEmits<{
  close: []
}>()
</script>

<template>
  <PairingPanelShell
    introduction="四个来源 Run 依照 sealed PairingPlan 的固定次序陈列；哈希与 Verdict 均保持原始事实。"
    @close="emit('close')"
  >
    <div class="pairing-source-grid" data-testid="paired-sources">
      <article v-for="(role, index) in PAIRING_ROLES" :key="role" class="pairing-source" :data-pairing-role="role">
        <header>
          <span>{{ index + 1 }}</span>
          <div>
            <p>{{ PAIRING_ROLE_META[role].chinese }} · {{ PAIRING_ROLE_META[role].english }}</p>
            <h3>{{ loaded.analysis.sources[role].run_id }}</h3>
            <small>{{ pairingDisplayDate(loaded.analysis.sources[role].created_at) }}（UTC+8）</small>
          </div>
        </header>
        <div class="pairing-source__status">
          <StatusBadge dimension="execution" :value="loaded.analysis.sources[role].execution_status" compact />
          <StatusBadge dimension="verdict" :value="loaded.analysis.sources[role].verdict" compact />
        </div>
        <dl>
          <div><dt>主变量</dt><dd><code>{{ pairingValue(loaded.analysis.sources[role].primary_variable.value) }}</code></dd></div>
          <div><dt>Plan</dt><dd>{{ loaded.analysis.sources[role].plan.id }} · v{{ loaded.analysis.sources[role].plan.version }}</dd></div>
          <div><dt>Random seed</dt><dd><code>{{ loaded.analysis.sources[role].random_seed }}</code></dd></div>
          <div>
            <dt>Plan SHA-256</dt>
            <dd><details><summary><code>{{ pairingShortHash(loaded.analysis.sources[role].plan.sha256) }}</code></summary><code>{{ loaded.analysis.sources[role].plan.sha256 }}</code></details></dd>
          </div>
          <div>
            <dt>Bundle SHA-256</dt>
            <dd><details><summary><code>{{ pairingShortHash(loaded.analysis.sources[role].bundle_sha256) }}</code></summary><code>{{ loaded.analysis.sources[role].bundle_sha256 }}</code></details></dd>
          </div>
        </dl>
      </article>
    </div>
  </PairingPanelShell>
</template>
