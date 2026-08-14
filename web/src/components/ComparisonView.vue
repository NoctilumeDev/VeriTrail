<script setup lang="ts">
import StatusBadge from './StatusBadge.vue'
import type { LoadedComparison } from '../domain/types'

const props = defineProps<{ loaded: LoadedComparison }>()

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
  if (props.loaded.comparison.comparison_status === 'MATCH') return '合'
  if (props.loaded.comparison.comparison_status === 'DRIFT') return '异'
  return '疑'
}
</script>

<template>
  <section class="comparison-court comparison-court--rerun" data-testid="comparison-view" aria-labelledby="comparison-title">
    <header class="comparison-court__heading">
      <div>
        <p class="eyebrow">Rerun Comparison · 对照殿</p>
        <h2 id="comparison-title">同计划复跑比较</h2>
      </div>
      <span>本地只读 · {{ loaded.integrity.verifiedFiles }} 文件已核验</span>
    </header>

    <section class="comparison-mirror" aria-label="同计划复跑来源与比较结论" data-testid="comparison-sources">
      <article
        v-for="source in [loaded.comparison.sources.baseline, loaded.comparison.sources.repeat]"
        :key="source.role"
        class="comparison-mirror__source"
        :class="`comparison-mirror__source--${source.role.toLowerCase()}`"
        :data-testid="`comparison-source-${source.role.toLowerCase()}`"
      >
        <header>
          <div><small>{{ source.role }}</small><h3>{{ source.run_id }}</h3></div>
          <div class="comparison-mirror__source-status">
            <StatusBadge dimension="execution" :value="source.execution_status" compact />
            <StatusBadge dimension="verdict" :value="source.verdict" compact />
          </div>
        </header>
        <dl>
          <div><dt>Plan</dt><dd>{{ source.plan.id }} · v{{ source.plan.version }}</dd></div>
          <div><dt>Plan SHA-256</dt><dd><code :title="source.plan.sha256">{{ shortHash(source.plan.sha256) }}</code></dd></div>
          <div><dt>Bundle</dt><dd><code :title="source.bundle_sha256">{{ shortHash(source.bundle_sha256) }}</code></dd></div>
          <div><dt>Semantic</dt><dd><code :title="source.semantic_sha256">{{ shortHash(source.semantic_sha256) }}</code></dd></div>
        </dl>
      </article>

      <div
        class="comparison-mirror__verdict"
        :class="`comparison-mirror__verdict--${loaded.comparison.comparison_status.toLowerCase()}`"
        :aria-label="`复跑比较：${loaded.comparison.comparison_status}`"
        data-testid="comparison-status"
      >
        <span aria-hidden="true">{{ statusMark() }}</span>
        <div>
          <small>ComparisonStatus · 独立于 Run Verdict</small>
          <strong>{{ loaded.comparison.comparison_status }}</strong>
          <p>{{ loaded.comparison.reasons[0]?.message }}</p>
        </div>
        <dl>
          <div><dt>可比较</dt><dd>{{ loaded.comparison.comparable ? '是' : '否' }}</dd></div>
          <div><dt>差异</dt><dd>{{ loaded.comparison.differences.length }}</dd></div>
          <div><dt>完整性</dt><dd>{{ formatBytes(loaded.integrity.totalBytes) }}</dd></div>
        </dl>
      </div>
    </section>

    <section class="comparison-rerun-differences" aria-labelledby="difference-title">
      <header>
        <p class="eyebrow">Frozen Projection · 差异账</p>
        <h3 id="difference-title">语义差异 {{ loaded.comparison.differences.length }} 项</h3>
      </header>
      <p v-if="loaded.comparison.differences.length === 0" class="comparison-rerun-empty" data-testid="comparison-no-differences">
        冻结投影内没有差异；来源文件哈希仍各自保留，不被伪装成同一个 Run。
      </p>
      <div v-else class="comparison-rerun-difference-list" data-testid="comparison-differences">
        <article v-for="difference in loaded.comparison.differences" :key="difference.path">
          <code>{{ difference.path }}</code>
          <div>
            <section><h4>BASELINE</h4><pre>{{ difference.baseline_present ? pretty(difference.baseline) : '〈不存在〉' }}</pre></section>
            <section><h4>REPEAT</h4><pre>{{ difference.repeat_present ? pretty(difference.repeat) : '〈不存在〉' }}</pre></section>
          </div>
        </article>
      </div>
    </section>

    <aside class="comparison-rerun-boundary" data-testid="comparison-boundary">
      <div><p class="eyebrow">Applicability · 边界</p><h3>这项比较没有越权裁决</h3></div>
      <ul><li v-for="item in loaded.comparison.limits" :key="item">{{ item }}</li></ul>
      <code>{{ loaded.comparison.comparison_id }} · {{ loaded.comparison.rule_version }}</code>
    </aside>
  </section>
</template>
