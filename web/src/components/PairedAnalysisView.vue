<script setup lang="ts">
import { computed } from 'vue'
import PairingOutcomes from './PairingOutcomes.vue'
import PairingSources from './PairingSources.vue'
import { PAIRING_ROLES, PAIRING_ROLE_META, pairingValue } from './pairingPresentation'
import type { LoadedPairedAnalysis, PairingRole } from '../domain/types'

type PairingPanel = 'sources' | 'outcomes'

const props = defineProps<{
  loaded: LoadedPairedAnalysis
  panel?: PairingPanel | null
}>()

const emit = defineEmits<{
  openPanel: [panel: PairingPanel]
  closePanel: []
}>()

function sameValue(left: unknown, right: unknown): boolean {
  return JSON.stringify(left) === JSON.stringify(right)
}

function actualVector(role: PairingRole): unknown[] {
  return props.loaded.analysis.outcomes.map((outcome) => outcome.roles[role].actual)
}

const allSourcesCompleted = computed(() =>
  PAIRING_ROLES.every((role) => props.loaded.analysis.sources[role].execution_status === 'COMPLETED'),
)

const matchedCounts = computed(() =>
  Object.fromEntries(
    PAIRING_ROLES.map((role) => [
      role,
      props.loaded.analysis.outcomes.filter((outcome) => outcome.roles[role].matches).length,
    ]),
  ) as Record<PairingRole, number>,
)

const relationships = computed(() => {
  const baseline = actualVector('BASELINE')
  const treatment = actualVector('TREATMENT')
  const restored = actualVector('RESTORED_BASELINE')
  const negative = actualVector('NEGATIVE_CONTROL')
  const recovered = sameValue(restored, baseline)

  return [
    {
      from: 'BASELINE' as const,
      to: 'TREATMENT' as const,
      label: sameValue(baseline, treatment) ? '一致' : '变化',
      result: sameValue(baseline, treatment) ? 'CONSISTENT' : 'DRIFT',
      detail: sameValue(baseline, treatment) ? '未见处理差异' : '处理后出现事实差异',
      tone: sameValue(baseline, treatment) ? 'positive' : 'negative',
    },
    {
      from: 'TREATMENT' as const,
      to: 'RESTORED_BASELINE' as const,
      label: recovered ? '恢复' : '未恢复',
      result: recovered ? 'RECOVERED' : 'UNRESOLVED',
      detail: recovered ? '复归后回到基线事实' : '复归后仍偏离基线',
      tone: recovered ? 'positive' : 'negative',
    },
    {
      from: 'RESTORED_BASELINE' as const,
      to: 'NEGATIVE_CONTROL' as const,
      label: sameValue(restored, negative) ? '一致' : '偏离',
      result: sameValue(restored, negative) ? 'CONSISTENT' : 'DRIFT',
      detail: sameValue(restored, negative) ? '负控未引入额外差异' : '负控出现额外差异',
      tone: sameValue(restored, negative) ? 'positive' : 'negative',
    },
    {
      from: 'BASELINE' as const,
      to: 'NEGATIVE_CONTROL' as const,
      label: sameValue(baseline, negative) ? '一致' : '偏离',
      result: sameValue(baseline, negative) ? 'CONSISTENT' : 'DRIFT',
      detail: sameValue(baseline, negative) ? '基线与负控事实一致' : '负控偏离基线事实',
      tone: sameValue(baseline, negative) ? 'positive' : 'negative',
    },
  ]
})

const analysisStatusLabel = computed(() => {
  if (props.loaded.analysis.analysis_status === 'SUPPORTED') return '结论成立'
  if (props.loaded.analysis.analysis_status === 'CONTRADICTED') return '结论受驳'
  return '证据未决'
})

</script>

<template>
  <section
    class="pairing-page"
    :class="[`pairing-page--${loaded.analysis.analysis_status.toLowerCase()}`, { 'pairing-page--panel': panel }]"
    data-testid="paired-analysis-view"
    aria-labelledby="paired-title"
  >
    <header class="pairing-heading">
      <div class="pairing-heading__title">
        <img :src="'/textures/r3-nav-pairing-thin.svg'" alt="" aria-hidden="true" />
        <div>
          <p class="eyebrow">Paired Analysis · 四象殿</p>
          <h2 id="paired-title" tabindex="-1">{{ panel ? (panel === 'sources' ? '四角色来源账册' : '预注册断言全貌') : '配对实验' }}</h2>
        </div>
      </div>
      <div
        v-if="!panel"
        class="pairing-heading__status"
        :aria-label="`配对分析：${loaded.analysis.analysis_status}`"
        data-testid="paired-analysis-status"
      >
        <dl>
          <div>
            <dt>配对状态</dt>
            <dd>{{ allSourcesCompleted ? 'COMPLETED' : 'INCOMPLETE' }}</dd>
            <span>{{ allSourcesCompleted ? '四序执行完成' : '来源执行未完整' }}</span>
          </div>
          <div>
            <dt>核心裁决</dt>
            <dd>{{ loaded.analysis.analysis_status }}</dd>
            <span>{{ analysisStatusLabel }}</span>
          </div>
          <div>
            <dt>完整性</dt>
            <dd>SEALED</dd>
            <span>{{ loaded.integrity.verifiedFiles }} 个文件已核验</span>
          </div>
        </dl>
      </div>
      <div class="pairing-heading__actions">
        <slot name="actions" />
      </div>
    </header>

    <template v-if="!panel">
      <ol class="pairing-sequence" aria-label="预注册四角色运行顺序" data-testid="paired-sequence">
        <li
          v-for="(role, index) in PAIRING_ROLES"
          :key="role"
          class="pairing-sequence__step"
          :data-pairing-role="role"
        >
          <div class="pairing-sequence__emblem" aria-hidden="true">
            <span class="pairing-sequence__ordinal">{{ index + 1 }}</span>
            <img :src="'/textures/pairing-palace-hall-line.png'" alt="" />
          </div>
          <strong>{{ PAIRING_ROLE_META[role].chinese }}</strong>
          <small>{{ PAIRING_ROLE_META[role].english }}</small>
          <button
            type="button"
            :title="loaded.analysis.sources[role].run_id"
            @click="emit('openPanel', 'sources')"
          >
            {{ loaded.analysis.sources[role].run_id }}
          </button>
        </li>
      </ol>

      <div class="pairing-court">
        <section class="pairing-outcome-summary" aria-labelledby="pairing-summary-title">
          <header class="pairing-section-heading">
            <p class="eyebrow">Outcomes Summary · 应验总览</p>
            <h3 id="pairing-summary-title">配对结果总览</h3>
            <span>基于 {{ loaded.analysis.outcomes.length }} 项预注册断言的事实对照</span>
          </header>
          <div class="pairing-outcome-summary__grid">
            <article
              v-for="relationship in relationships"
              :key="`${relationship.from}-${relationship.to}`"
              :class="[`pairing-relationship`, `pairing-relationship--${relationship.tone}`]"
            >
              <h4>{{ PAIRING_ROLE_META[relationship.from].chinese }} → {{ PAIRING_ROLE_META[relationship.to].chinese }}</h4>
              <small>{{ relationship.from }} → {{ relationship.to }}</small>
              <div>
                <span>{{ relationship.label }}</span>
                <strong>{{ relationship.result }}</strong>
              </div>
              <p>{{ relationship.detail }}</p>
            </article>
          </div>
        </section>

        <div class="pairing-summary-grid">
        <section class="pairing-metrics" aria-labelledby="pairing-metrics-title">
          <header class="pairing-section-heading pairing-section-heading--compact">
            <p class="eyebrow">Key Metrics · 度支册</p>
            <h3 id="pairing-metrics-title">关键指标对比</h3>
          </header>
          <div class="pairing-metrics__table-wrap">
            <table>
              <thead>
                <tr>
                  <th scope="col">指标</th>
                  <th v-for="role in PAIRING_ROLES" :key="role" scope="col">{{ PAIRING_ROLE_META[role].chinese }}</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <th scope="row">断言吻合</th>
                  <td v-for="role in PAIRING_ROLES" :key="role">{{ matchedCounts[role] }}/{{ loaded.analysis.outcomes.length }}</td>
                </tr>
                <tr>
                  <th scope="row">来源 Verdict</th>
                  <td v-for="role in PAIRING_ROLES" :key="role" :class="`is-${loaded.analysis.sources[role].verdict.toLowerCase()}`">
                    {{ loaded.analysis.sources[role].verdict }}
                  </td>
                </tr>
                <tr>
                  <th scope="row">主变量</th>
                  <td v-for="role in PAIRING_ROLES" :key="role" :title="pairingValue(loaded.analysis.sources[role].primary_variable.value)">
                    {{ pairingValue(loaded.analysis.sources[role].primary_variable.value) }}
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
          <button type="button" data-testid="pairing-open-sources" data-open-pairing-panel="sources" @click="emit('openPanel', 'sources')">
            查看四角色来源账册
          </button>
        </section>

        <section class="pairing-interpretation" aria-labelledby="pairing-interpretation-title">
          <header class="pairing-section-heading pairing-section-heading--compact">
            <p class="eyebrow">Conclusion · 中枢判读</p>
            <h3 id="pairing-interpretation-title">结论与解释</h3>
          </header>
          <ol>
            <li v-for="reason in loaded.analysis.reasons" :key="reason.code">
              <span>{{ reason.code }}</span>
              <p>{{ reason.message }}</p>
            </li>
            <li>
              <span>VERDICT_BOUNDARY</span>
              <p>配对结论独立于来源 Run Verdict，不改写任一来源裁决。</p>
            </li>
            <li>
              <span>PLAN_SEAL</span>
              <p>四角色顺序与预期值均来自 sealed PairingPlan。</p>
            </li>
          </ol>
          <button type="button" data-testid="pairing-open-outcomes" data-open-pairing-panel="outcomes" @click="emit('openPanel', 'outcomes')">
            查看全部 {{ loaded.analysis.outcomes.length }} 项断言
          </button>
        </section>

        <section class="pairing-boundary" aria-labelledby="pairing-boundary-title" data-testid="paired-boundary">
          <header class="pairing-section-heading pairing-section-heading--compact">
            <p class="eyebrow">Applicability · 都察边界</p>
            <h3 id="pairing-boundary-title">适用性与边界</h3>
          </header>
          <dl>
            <div><dt>预热方式</dt><dd>{{ loaded.analysis.warmup.mode }} · {{ loaded.analysis.warmup.iterations }} 次</dd></div>
            <div><dt>计划版本</dt><dd>v{{ loaded.pairingPlan.version }}</dd></div>
            <div><dt>主变量来源</dt><dd>{{ loaded.analysis.primary_variable.source }}</dd></div>
            <div><dt>未计划差异</dt><dd>{{ loaded.analysis.unplanned_differences.length }} 项</dd></div>
          </dl>
          <ul>
            <li v-for="item in loaded.analysis.limits" :key="item">{{ item }}</li>
          </ul>
          <details>
            <summary>查看配对分析标识</summary>
            <code>{{ loaded.analysis.analysis_id }} · {{ loaded.analysis.rule_version }}</code>
          </details>
        </section>
        </div>
      </div>
    </template>

    <PairingSources v-else-if="panel === 'sources'" :loaded="loaded" @close="emit('closePanel')" />

    <PairingOutcomes v-else :loaded="loaded" @close="emit('closePanel')" />
  </section>
</template>
