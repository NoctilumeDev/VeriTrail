<script setup lang="ts">
import { computed } from 'vue'
import StatusBadge from './StatusBadge.vue'
import type { BatchAnalysisSlot, LoadedBatchAnalysis } from '../domain/types'

const props = defineProps<{ loaded: LoadedBatchAnalysis }>()

const waves = computed(() => {
  const result: Array<{ key: string; phase: string; repetition: number; wave: number; slots: BatchAnalysisSlot[] }> = []
  for (const slot of props.loaded.analysis.slots) {
    const key = `${slot.phase}:${slot.repetition}:${slot.wave}`
    const current = result.at(-1)
    if (!current || current.key !== key) {
      result.push({ key, phase: slot.phase, repetition: slot.repetition, wave: slot.wave, slots: [] })
    }
    result.at(-1)!.slots.push(slot)
  }
  return result
})

function pretty(value: unknown): string {
  if (typeof value === 'string') return value
  return JSON.stringify(value, null, 2)
}

function shortHash(value: string): string {
  return `${value.slice(0, 12)}…${value.slice(-8)}`
}

function formatBytes(bytes: number): string {
  if (bytes < 1024) return `${bytes} B`
  return `${(bytes / 1024).toFixed(1)} KiB`
}

function statusMark(status: string): string {
  if (status === 'COMPLETE' || status === 'SUPPORTED') return '证'
  if (status === 'CONTRADICTED') return '驳'
  if (status === 'INCOMPLETE') return '缺'
  return '疑'
}

function waveMemory(slots: BatchAnalysisSlot[]): number {
  const profiles = new Map(props.loaded.batchPlan.profiles.map((profile) => [profile.id, profile]))
  return slots.reduce(
    (total, slot) => total + (profiles.get(slot.profile_id)?.estimated_memory_mb ?? 0),
    0,
  )
}
</script>

<template>
  <section class="batch-court" data-testid="batch-analysis-view" aria-labelledby="view-batch-title">
    <header class="batch-court__heading">
      <div>
        <p class="eyebrow">Full-factorial Batch · 万象院</p>
        <h2 id="view-batch-title" tabindex="-1" data-testid="view-batch-title">预注册全因子批次分析</h2>
      </div>
      <span>本地只读 · {{ loaded.integrity.verifiedFiles }} 文件已核验</span>
    </header>

    <section class="batch-state-gates" data-testid="batch-status-gate" aria-label="批次分析双状态">
      <article
        class="batch-analysis-status batch-analysis-status--coverage"
        :class="`batch-analysis-status--${loaded.analysis.coverage_status.toLowerCase()}`"
        :aria-label="`覆盖状态：${loaded.analysis.coverage_status}`"
        data-testid="batch-coverage-status"
      >
        <span class="batch-analysis-status__mark" aria-hidden="true">{{ statusMark(loaded.analysis.coverage_status) }}</span>
        <div class="batch-analysis-status__body">
          <small>CoverageStatus · 矩阵是否可信完整</small>
          <strong>{{ loaded.analysis.coverage_status }}</strong>
          <p>完整性、slot 唯一性与受控条件分别核验。</p>
        </div>
        <span class="batch-analysis-status__scope">COVERAGE</span>
      </article>
      <div class="batch-state-gates__axis" aria-hidden="true"><span></span></div>
      <article
        class="batch-analysis-status batch-analysis-status--hypothesis"
        :class="`batch-analysis-status--${loaded.analysis.hypothesis_status.toLowerCase()}`"
        :aria-label="`假设状态：${loaded.analysis.hypothesis_status}`"
        data-testid="batch-hypothesis-status"
      >
        <span class="batch-analysis-status__mark" aria-hidden="true">{{ statusMark(loaded.analysis.hypothesis_status) }}</span>
        <div class="batch-analysis-status__body">
          <small>HypothesisStatus · 预注册结果是否成立</small>
          <strong>{{ loaded.analysis.hypothesis_status }}</strong>
          <p>只读取完整 coverage 上的预注册 outcome。</p>
        </div>
        <span class="batch-analysis-status__scope">HYPOTHESIS</span>
      </article>
    </section>

    <section class="batch-policy-ledger" aria-labelledby="batch-policy-title">
      <header class="batch-section-heading">
        <p class="eyebrow">Sealed Policy · 调度契约</p>
        <h3 id="batch-policy-title">先确定性覆盖，再固定种子扰动</h3>
      </header>
      <dl class="batch-policy-ledger__facts">
        <div><dt>Seed</dt><dd>{{ loaded.analysis.execution_policy.seed }}</dd></div>
        <div><dt>算法</dt><dd>{{ loaded.analysis.execution_policy.order_algorithm }}</dd></div>
        <div><dt>扰动轮次</dt><dd>{{ loaded.analysis.execution_policy.perturbation_repetitions }}</dd></div>
        <div><dt>微并行上限</dt><dd>{{ loaded.analysis.execution_policy.max_parallel }}</dd></div>
        <div><dt>Wave 预算</dt><dd>{{ loaded.analysis.execution_policy.memory_budget_mb }} MiB</dd></div>
        <div><dt>完整性</dt><dd>{{ formatBytes(loaded.integrity.totalBytes) }}</dd></div>
      </dl>
    </section>

    <section class="batch-matrix-court" aria-labelledby="batch-matrix-title">
      <header class="batch-section-heading">
        <p class="eyebrow">Dimension Matrix · 格局</p>
        <h3 id="batch-matrix-title">{{ loaded.batchPlan.dimensions.length }} 维 · {{ loaded.analysis.profiles.length }} 个 Profile</h3>
      </header>
      <div class="batch-matrix-court__scroll batch-matrix-scroll" role="region" aria-label="全因子 Profile 矩阵" tabindex="0">
        <table data-testid="batch-profile-matrix">
          <thead>
            <tr>
              <th scope="col">Profile</th>
              <th v-for="dimension in loaded.batchPlan.dimensions" :key="dimension.name" scope="col">
                {{ dimension.name }}
              </th>
              <th scope="col">出现</th>
              <th scope="col">完成</th>
              <th scope="col">不符</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="profile in loaded.analysis.profiles" :key="profile.id" :data-batch-profile="profile.id">
              <th scope="row">{{ profile.id }}</th>
              <td v-for="dimension in loaded.batchPlan.dimensions" :key="dimension.name">
                <code>{{ profile.cells[dimension.name] }}</code>
              </td>
              <td>{{ profile.occurrence_count }}</td>
              <td>{{ profile.completed_count }}</td>
              <td :class="{ 'is-mismatch': profile.mismatch_count > 0 }">{{ profile.mismatch_count }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>

    <section class="batch-wave-ledger" aria-labelledby="batch-waves-title">
      <header class="batch-section-heading">
        <p class="eyebrow">Phase / Wave Ledger · 行次</p>
        <h3 id="batch-waves-title">{{ waves.length }} 个有界 wave · {{ loaded.analysis.slots.length }} 个 slot</h3>
      </header>
      <div class="batch-wave-ledger__list" data-testid="batch-wave-list">
        <article
          v-for="wave in waves"
          :key="wave.key"
          class="batch-wave"
          :data-batch-phase="wave.phase"
          :data-batch-wave="wave.wave"
        >
          <header class="batch-wave__heading">
            <div>
              <small>{{ wave.phase }} · REP {{ wave.repetition }}</small>
              <strong>Wave {{ wave.wave }}</strong>
            </div>
            <span>{{ wave.slots.length }} slot · {{ waveMemory(wave.slots) }} MiB</span>
          </header>
          <ol class="batch-wave__slots">
            <li
              v-for="slot in wave.slots"
              :key="slot.slot_id"
              class="batch-slot"
              :class="{ 'is-missing': !slot.source }"
              :data-batch-slot="slot.slot_id"
            >
              <div class="batch-slot__identity">
                <span class="batch-slot__position">{{ slot.position }}</span>
                <div class="batch-slot__identity-copy">
                  <strong>{{ slot.profile_id }}</strong>
                  <code>{{ slot.slot_id }}</code>
                </div>
              </div>
              <template v-if="slot.source">
                <div class="batch-slot__source">
                  <small>Run</small>
                  <strong>{{ slot.source.run_id }}</strong>
                  <code :title="slot.source.bundle_sha256">{{ shortHash(slot.source.bundle_sha256) }}</code>
                </div>
                <div class="batch-slot__statuses">
                  <StatusBadge dimension="execution" :value="slot.source.execution_status" compact />
                  <StatusBadge dimension="verdict" :value="slot.source.verdict" compact />
                </div>
              </template>
              <div v-else class="batch-slot__missing" role="status">
                <strong>MISSING</strong>
                <small>来源 Run 未提供</small>
              </div>
              <details>
                <summary>Outcome {{ slot.outcomes.filter((outcome) => !outcome.matches).length }} 项不符</summary>
                <dl>
                  <div v-for="outcome in slot.outcomes" :key="outcome.assertion_id" class="batch-slot__outcome" :class="{ 'is-mismatch': !outcome.matches }">
                    <dt>{{ outcome.assertion_id }} · {{ outcome.matches ? '吻合' : '不符' }}</dt>
                    <dd><code>Expected {{ pretty(outcome.expected_actual) }}</code></dd>
                    <dd><code>Actual {{ pretty(outcome.actual) }}</code></dd>
                  </div>
                </dl>
              </details>
            </li>
          </ol>
        </article>
      </div>
    </section>

    <section class="batch-reason-ledger" aria-labelledby="batch-reasons-title">
      <header class="batch-section-heading">
        <p class="eyebrow">Deterministic Reasons · 判词</p>
        <h3 id="batch-reasons-title">状态依据</h3>
      </header>
      <ul class="batch-reason-ledger__list" data-testid="batch-reasons">
        <li v-for="reason in loaded.analysis.reasons" :key="reason.code">
          <code>{{ reason.code }}</code>
          <span>{{ reason.message }}</span>
        </li>
      </ul>
    </section>

    <aside class="batch-boundary" data-testid="batch-boundary">
      <div>
        <p class="eyebrow">Applicability · 边界</p>
        <h3>覆盖、假设与 Run Verdict 各自独立</h3>
        <p>Wave 是封存的资源与顺序边界，<strong>不证明真实并行</strong>。</p>
        <p>Profile 信号不是统计显著性，也不自动证明组件级因果。</p>
      </div>
      <ul><li v-for="item in loaded.analysis.limits" :key="item">{{ item }}</li></ul>
      <code>{{ loaded.analysis.analysis_id }} · {{ loaded.analysis.rule_version }}</code>
    </aside>
  </section>
</template>
