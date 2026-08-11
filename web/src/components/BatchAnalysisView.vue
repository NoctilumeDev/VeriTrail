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
  <section class="comparison-court batch-court" data-testid="batch-analysis-view" aria-labelledby="batch-title">
    <header class="comparison-court__heading">
      <div>
        <p class="eyebrow">Full-factorial Batch · 万象院</p>
        <h2 id="batch-title">预注册全因子批次分析</h2>
      </div>
      <span>本地只读 · {{ loaded.integrity.verifiedFiles }} 文件已核验</span>
    </header>

    <div class="batch-status-gate" data-testid="batch-status-gate">
      <article
        class="batch-status"
        :class="`batch-status--${loaded.analysis.coverage_status.toLowerCase()}`"
        :aria-label="`覆盖状态：${loaded.analysis.coverage_status}`"
        data-testid="batch-coverage-status"
      >
        <span aria-hidden="true">{{ statusMark(loaded.analysis.coverage_status) }}</span>
        <div>
          <small>CoverageStatus · 矩阵是否可信完整</small>
          <strong>{{ loaded.analysis.coverage_status }}</strong>
        </div>
      </article>
      <div class="batch-status-axis" aria-hidden="true"><span></span></div>
      <article
        class="batch-status"
        :class="`batch-status--${loaded.analysis.hypothesis_status.toLowerCase()}`"
        :aria-label="`假设状态：${loaded.analysis.hypothesis_status}`"
        data-testid="batch-hypothesis-status"
      >
        <span aria-hidden="true">{{ statusMark(loaded.analysis.hypothesis_status) }}</span>
        <div>
          <small>HypothesisStatus · 预注册结果是否成立</small>
          <strong>{{ loaded.analysis.hypothesis_status }}</strong>
        </div>
      </article>
    </div>

    <section class="batch-policy" aria-labelledby="batch-policy-title">
      <header>
        <p class="eyebrow">Sealed Policy · 调度契约</p>
        <h3 id="batch-policy-title">先确定性覆盖，再固定种子扰动</h3>
      </header>
      <dl>
        <div><dt>Seed</dt><dd>{{ loaded.analysis.execution_policy.seed }}</dd></div>
        <div><dt>算法</dt><dd>{{ loaded.analysis.execution_policy.order_algorithm }}</dd></div>
        <div><dt>扰动轮次</dt><dd>{{ loaded.analysis.execution_policy.perturbation_repetitions }}</dd></div>
        <div><dt>微并行上限</dt><dd>{{ loaded.analysis.execution_policy.max_parallel }}</dd></div>
        <div><dt>Wave 预算</dt><dd>{{ loaded.analysis.execution_policy.memory_budget_mb }} MiB</dd></div>
        <div><dt>完整性</dt><dd>{{ formatBytes(loaded.integrity.totalBytes) }}</dd></div>
      </dl>
    </section>

    <section class="batch-matrix" aria-labelledby="batch-matrix-title">
      <header>
        <p class="eyebrow">Dimension Matrix · 格局</p>
        <h3 id="batch-matrix-title">{{ loaded.batchPlan.dimensions.length }} 维 · {{ loaded.analysis.profiles.length }} 个 Profile</h3>
      </header>
      <div class="batch-matrix-scroll" role="region" aria-label="全因子 Profile 矩阵" tabindex="0">
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
            <tr v-for="profile in loaded.analysis.profiles" :key="profile.id">
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

    <section class="batch-waves" aria-labelledby="batch-waves-title">
      <header>
        <p class="eyebrow">Phase / Wave Ledger · 行次</p>
        <h3 id="batch-waves-title">{{ waves.length }} 个有界 wave · {{ loaded.analysis.slots.length }} 个 slot</h3>
      </header>
      <div class="batch-wave-list" data-testid="batch-wave-list">
        <article v-for="wave in waves" :key="wave.key" class="batch-wave">
          <header>
            <div>
              <small>{{ wave.phase }} · REP {{ wave.repetition }}</small>
              <strong>Wave {{ wave.wave }}</strong>
            </div>
            <span>{{ wave.slots.length }} slot · {{ waveMemory(wave.slots) }} MiB</span>
          </header>
          <ol>
            <li v-for="slot in wave.slots" :key="slot.slot_id" :class="{ 'is-missing': !slot.source }">
              <div class="batch-slot-identity">
                <span>{{ slot.position }}</span>
                <div>
                  <strong>{{ slot.profile_id }}</strong>
                  <code>{{ slot.slot_id }}</code>
                </div>
              </div>
              <template v-if="slot.source">
                <div class="batch-slot-run">
                  <small>Run</small>
                  <strong>{{ slot.source.run_id }}</strong>
                  <code :title="slot.source.bundle_sha256">{{ shortHash(slot.source.bundle_sha256) }}</code>
                </div>
                <div class="batch-slot-statuses">
                  <StatusBadge dimension="execution" :value="slot.source.execution_status" compact />
                  <StatusBadge dimension="verdict" :value="slot.source.verdict" compact />
                </div>
              </template>
              <div v-else class="batch-slot-missing" role="status">
                <strong>MISSING</strong>
                <small>来源 Run 未提供</small>
              </div>
              <details>
                <summary>Outcome {{ slot.outcomes.filter((outcome) => !outcome.matches).length }} 项不符</summary>
                <dl>
                  <div v-for="outcome in slot.outcomes" :key="outcome.assertion_id" :class="{ 'is-mismatch': !outcome.matches }">
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

    <section class="batch-reasons" aria-labelledby="batch-reasons-title">
      <header>
        <p class="eyebrow">Deterministic Reasons · 判词</p>
        <h3 id="batch-reasons-title">状态依据</h3>
      </header>
      <ul data-testid="batch-reasons">
        <li v-for="reason in loaded.analysis.reasons" :key="reason.code">
          <code>{{ reason.code }}</code>
          <span>{{ reason.message }}</span>
        </li>
      </ul>
    </section>

    <aside class="comparison-boundary batch-boundary" data-testid="batch-boundary">
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
