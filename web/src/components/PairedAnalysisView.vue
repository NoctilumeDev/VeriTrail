<script setup lang="ts">
import StatusBadge from './StatusBadge.vue'
import type { LoadedPairedAnalysis, PairingRole } from '../domain/types'

const props = defineProps<{ loaded: LoadedPairedAnalysis }>()

const roles: PairingRole[] = [
  'BASELINE',
  'TREATMENT',
  'RESTORED_BASELINE',
  'NEGATIVE_CONTROL',
]

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

function statusMark(): string {
  if (props.loaded.analysis.analysis_status === 'SUPPORTED') return '证'
  if (props.loaded.analysis.analysis_status === 'CONTRADICTED') return '驳'
  return '疑'
}
</script>

<template>
  <section class="comparison-court paired-court" data-testid="paired-analysis-view" aria-labelledby="paired-title">
    <header class="comparison-court__heading">
      <div>
        <p class="eyebrow">Paired Counterfactual · 四象殿</p>
        <h2 id="paired-title">预注册四角色配对分析</h2>
      </div>
      <span>本地只读 · {{ loaded.integrity.verifiedFiles }} 文件已核验</span>
    </header>

    <div
      class="comparison-verdict paired-verdict"
      :class="`paired-verdict--${loaded.analysis.analysis_status.toLowerCase()}`"
      :aria-label="`配对分析：${loaded.analysis.analysis_status}`"
      data-testid="paired-analysis-status"
    >
      <span aria-hidden="true">{{ statusMark() }}</span>
      <div>
        <small>AnalysisStatus · 独立于 Run Verdict</small>
        <strong>{{ loaded.analysis.analysis_status }}</strong>
        <p>{{ loaded.analysis.reasons[0]?.message }}</p>
      </div>
      <dl>
        <div><dt>可归因</dt><dd>{{ loaded.analysis.attributable ? '是' : '否' }}</dd></div>
        <div><dt>Outcome</dt><dd>{{ loaded.analysis.outcomes.length }}</dd></div>
        <div><dt>完整性</dt><dd>{{ formatBytes(loaded.integrity.totalBytes) }}</dd></div>
      </dl>
    </div>

    <ol class="paired-sequence" aria-label="预注册运行顺序" data-testid="paired-sequence">
      <li v-for="(role, index) in roles" :key="role">
        <span>{{ index + 1 }}</span>
        <strong>{{ role }}</strong>
        <small>{{ pretty(loaded.analysis.sources[role].primary_variable.value) }}</small>
      </li>
    </ol>

    <div class="comparison-sources paired-sources" data-testid="paired-sources">
      <article v-for="role in roles" :key="role">
        <header>
          <div><small>{{ role }}</small><h3>{{ loaded.analysis.sources[role].run_id }}</h3></div>
          <div class="comparison-source-status">
            <StatusBadge dimension="execution" :value="loaded.analysis.sources[role].execution_status" compact />
            <StatusBadge dimension="verdict" :value="loaded.analysis.sources[role].verdict" compact />
          </div>
        </header>
        <dl>
          <div><dt>主变量</dt><dd><code>{{ pretty(loaded.analysis.sources[role].primary_variable.value) }}</code></dd></div>
          <div><dt>Plan</dt><dd>{{ loaded.analysis.sources[role].plan.id }} · v{{ loaded.analysis.sources[role].plan.version }}</dd></div>
          <div><dt>Plan SHA-256</dt><dd><code :title="loaded.analysis.sources[role].plan.sha256">{{ shortHash(loaded.analysis.sources[role].plan.sha256) }}</code></dd></div>
          <div><dt>Bundle</dt><dd><code :title="loaded.analysis.sources[role].bundle_sha256">{{ shortHash(loaded.analysis.sources[role].bundle_sha256) }}</code></dd></div>
        </dl>
      </article>
    </div>

    <section class="paired-outcomes" aria-labelledby="paired-outcomes-title">
      <header>
        <p class="eyebrow">Preregistered Outcomes · 应验册</p>
        <h3 id="paired-outcomes-title">预期与实际 {{ loaded.analysis.outcomes.length }} 项</h3>
      </header>
      <div class="paired-outcome-list" data-testid="paired-outcomes">
        <article v-for="outcome in loaded.analysis.outcomes" :key="outcome.assertion_id">
          <h4>{{ outcome.assertion_id }}</h4>
          <div>
            <section v-for="role in roles" :key="role" :class="{ 'is-mismatch': !outcome.roles[role].matches }">
              <header><strong>{{ role }}</strong><span>{{ outcome.roles[role].matches ? '吻合' : '不符' }}</span></header>
              <dl>
                <div><dt>Expected</dt><dd><code>{{ pretty(outcome.roles[role].expected_actual) }}</code></dd></div>
                <div><dt>Actual</dt><dd><code>{{ pretty(outcome.roles[role].actual) }}</code></dd></div>
              </dl>
            </section>
          </div>
        </article>
      </div>
    </section>

    <aside class="comparison-boundary" data-testid="paired-boundary">
      <div>
        <p class="eyebrow">Applicability · 边界</p>
        <h3>来源 Verdict 未被改写</h3>
        <p>预热：{{ loaded.analysis.warmup.mode }} · {{ loaded.analysis.warmup.iterations }} 次</p>
      </div>
      <ul><li v-for="item in loaded.analysis.limits" :key="item">{{ item }}</li></ul>
      <code>{{ loaded.analysis.analysis_id }} · {{ loaded.analysis.rule_version }}</code>
    </aside>
  </section>
</template>
