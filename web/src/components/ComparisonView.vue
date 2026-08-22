<script setup lang="ts">
import { computed } from 'vue'
import type { ComparisonDifference, ComparisonSource, LoadedComparison } from '../domain/types'

type ComparisonPanel = 'differences'

const props = defineProps<{
  loaded: LoadedComparison
  panel?: ComparisonPanel | null
}>()

const emit = defineEmits<{
  openPanel: [panel: ComparisonPanel]
  closePanel: []
}>()

const sources = computed(() => [
  props.loaded.comparison.sources.baseline,
  props.loaded.comparison.sources.repeat,
])

const differencePreview = computed(() => props.loaded.comparison.differences.slice(0, 3))

function pretty(value: unknown): string {
  if (typeof value === 'string') return value
  if (value === undefined) return '〈不存在〉'
  return JSON.stringify(value, null, 2)
}

function compactValue(value: unknown): string {
  const rendered = pretty(value).replace(/\s+/g, ' ')
  return rendered.length > 44 ? `${rendered.slice(0, 41)}…` : rendered
}

function shortHash(value: string): string {
  return `${value.slice(0, 12)}…${value.slice(-8)}`
}

function displayDate(value: string): string {
  const date = new Date(value)
  return Number.isNaN(date.valueOf())
    ? value
    : date.toLocaleString('zh-CN', { hour12: false, timeZone: 'Asia/Shanghai' })
}

function formatBytes(bytes: number): string {
  if (bytes < 1024) return `${bytes} B`
  return `${(bytes / 1024).toFixed(1)} KiB`
}

function sourceLabel(source: ComparisonSource): string {
  return source.role === 'BASELINE' ? '基线 Run' : '重复 Run'
}

function differenceKind(difference: ComparisonDifference): string {
  if (difference.path.startsWith('/assertions/')) return '断言差异'
  if (difference.path === '/verdict') return '裁决差异'
  if (difference.path === '/evidence_shape') return '证据形态'
  if (difference.path === '/reason_codes') return '理由差异'
  return '语义差异'
}

function differenceImpact(difference: ComparisonDifference): string {
  return difference.path === '/verdict' || difference.path.includes('/status') ? '高' : '中'
}
</script>

<template>
  <section
    class="rerun-page"
    :class="[`rerun-page--${loaded.comparison.comparison_status.toLowerCase()}`, { 'rerun-page--panel': panel }]"
    data-testid="comparison-view"
    aria-labelledby="view-comparison-title"
  >
    <header class="rerun-heading">
      <div class="rerun-heading__title">
        <img :src="'/textures/r3-nav-comparison.png'" alt="" aria-hidden="true" />
        <div>
          <p class="eyebrow">Rerun Comparison · 对照殿</p>
          <h2 id="view-comparison-title" tabindex="-1" data-testid="view-comparison-title">
            {{ panel ? '完整语义差异账册' : '复跑比较' }}
          </h2>
        </div>
      </div>
      <div v-if="!panel" class="rerun-heading__status">
        <dl>
          <div>
            <dt>比较状态</dt>
            <dd>{{ loaded.comparison.comparison_status }}</dd>
            <span>{{ loaded.comparison.reasons[0]?.message }}</span>
          </div>
          <div>
            <dt>可比较性</dt>
            <dd>{{ loaded.comparison.comparable ? 'COMPARABLE' : 'BLOCKED' }}</dd>
            <span>{{ loaded.comparison.comparable ? '同计划、同随机种子' : '比较前提未满足' }}</span>
          </div>
          <div>
            <dt>完整性</dt>
            <dd>VERIFIED</dd>
            <span>{{ loaded.integrity.verifiedFiles }} 个文件已核验</span>
          </div>
        </dl>
      </div>
      <div class="rerun-heading__actions">
        <slot name="actions" />
      </div>
    </header>

    <template v-if="panel === 'differences'">
      <section class="rerun-ledger" aria-labelledby="rerun-ledger-title" data-testid="comparison-differences">
        <header class="rerun-section-heading">
          <div>
            <p class="eyebrow">Semantic Differences · 差异全貌</p>
            <h3 id="rerun-ledger-title">语义差异 {{ loaded.comparison.differences.length }} 项</h3>
          </div>
          <span>{{ loaded.comparison.rule_version }}</span>
        </header>

        <p v-if="loaded.comparison.differences.length === 0" class="rerun-ledger__empty" data-testid="comparison-no-differences">
          冻结语义投影内没有差异；两个来源 Run 的身份与哈希仍分别保留。
        </p>
        <ol v-else class="rerun-ledger__list">
          <li v-for="(difference, index) in loaded.comparison.differences" :key="difference.path">
            <header>
              <span>{{ String(index + 1).padStart(2, '0') }}</span>
              <div>
                <strong>{{ differenceKind(difference) }}</strong>
                <code>{{ difference.path }}</code>
              </div>
              <em>{{ differenceImpact(difference) }}影响</em>
            </header>
            <div class="rerun-ledger__values">
              <section>
                <h4>BASELINE</h4>
                <pre>{{ difference.baseline_present ? pretty(difference.baseline) : '〈不存在〉' }}</pre>
              </section>
              <section>
                <h4>REPEAT</h4>
                <pre>{{ difference.repeat_present ? pretty(difference.repeat) : '〈不存在〉' }}</pre>
              </section>
            </div>
          </li>
        </ol>

        <aside class="rerun-ledger__basis">
          <div>
            <p class="eyebrow">Decision Basis · 判定依据</p>
            <h3>{{ loaded.comparison.reasons[0]?.code }}</h3>
          </div>
          <p>{{ loaded.comparison.reasons[0]?.message }}</p>
          <code>{{ loaded.comparison.comparison_id }}</code>
        </aside>
      </section>

      <nav class="rerun-panel-return" aria-label="完整差异账册返回操作">
        <button type="button" data-testid="comparison-panel-return-bottom" @click="emit('closePanel')">
          返回复跑比较总览
        </button>
      </nav>
    </template>

    <template v-else>
      <section class="rerun-overview" :aria-label="`复跑比较：${loaded.comparison.comparison_status}`" data-testid="comparison-status">
        <div class="rerun-overview__verdict" :aria-label="`复跑比较：${loaded.comparison.comparison_status}`">
          <span>比较裁决</span>
          <strong>{{ loaded.comparison.comparison_status }}</strong>
          <p>{{ loaded.comparison.comparison_status === 'MATCH' ? '冻结投影一致' : loaded.comparison.comparison_status === 'DRIFT' ? '差异 · 需关注' : '前提不足 · 未决' }}</p>
        </div>
        <div class="rerun-overview__source">
          <small>基线 Run · BASELINE</small>
          <strong :title="loaded.comparison.sources.baseline.run_id">{{ loaded.comparison.sources.baseline.run_id }}</strong>
          <time :datetime="loaded.comparison.sources.baseline.created_at">{{ displayDate(loaded.comparison.sources.baseline.created_at) }}</time>
        </div>
        <img :src="'/textures/r3-nav-comparison.png'" alt="" aria-hidden="true" />
        <div class="rerun-overview__source rerun-overview__source--repeat">
          <small>重复 Run · REPEAT</small>
          <strong :title="loaded.comparison.sources.repeat.run_id">{{ loaded.comparison.sources.repeat.run_id }}</strong>
          <time :datetime="loaded.comparison.sources.repeat.created_at">{{ displayDate(loaded.comparison.sources.repeat.created_at) }}</time>
        </div>
      </section>

      <div class="rerun-data-court">
        <section class="rerun-mirror" aria-label="同计划复跑来源与核心判定" data-testid="comparison-sources">
          <header class="rerun-mirror__beam" aria-hidden="true">
            <div class="rerun-mirror__beam-source rerun-mirror__beam-source--baseline">
              <span>基线 Run</span>
              <strong>BASELINE</strong>
            </div>
            <div class="rerun-mirror__beam-axis">
              <span>勘合</span>
              <strong>JUDGMENT</strong>
            </div>
            <div class="rerun-mirror__beam-source rerun-mirror__beam-source--repeat">
              <span>重复 Run</span>
              <strong>REPEAT</strong>
            </div>
          </header>

          <template v-for="source in sources" :key="source.role">
            <article
              class="rerun-source"
              :class="`rerun-source--${source.role.toLowerCase()}`"
              :data-testid="`comparison-source-${source.role.toLowerCase()}`"
              :aria-label="`${sourceLabel(source)} ${source.role}`"
            >
              <p class="rerun-source__mobile-title" aria-hidden="true">
                <span>{{ sourceLabel(source) }}</span>
                <strong>{{ source.role }}</strong>
              </p>
              <dl class="rerun-source__statuses">
                <div><dt>Execution Status</dt><dd>{{ source.execution_status }}</dd></div>
                <div><dt>Run Verdict</dt><dd :class="`is-${source.verdict.toLowerCase()}`">{{ source.verdict }}</dd></div>
                <div><dt>Source Identity</dt><dd>PRESERVED</dd></div>
              </dl>
              <dl class="rerun-source__facts">
                <div><dt>Run ID</dt><dd :title="source.run_id">{{ source.run_id }}</dd></div>
                <div><dt>Plan</dt><dd>{{ source.plan.id }} · v{{ source.plan.version }}</dd></div>
                <div><dt>Random Seed</dt><dd>{{ source.random_seed }}</dd></div>
                <div>
                  <dt>Plan SHA-256</dt>
                  <dd>
                    <details>
                      <summary><code>{{ shortHash(source.plan.sha256) }}</code></summary>
                      <code>{{ source.plan.sha256 }}</code>
                    </details>
                  </dd>
                </div>
                <div>
                  <dt>Bundle SHA-256</dt>
                  <dd>
                    <details>
                      <summary><code>{{ shortHash(source.bundle_sha256) }}</code></summary>
                      <code>{{ source.bundle_sha256 }}</code>
                    </details>
                  </dd>
                </div>
              </dl>
            </article>

            <aside
              v-if="source.role === 'BASELINE'"
              class="rerun-judgment"
              aria-label="勘合中轴图案"
              data-testid="comparison-judgment"
            >
              <p class="eyebrow">Core Judgment · 中轴</p>
              <img :src="'/textures/r3-nav-comparison.png'" alt="" aria-hidden="true" />
            </aside>
          </template>
        </section>

        <div class="rerun-summary-grid">
          <section class="rerun-difference-preview" aria-labelledby="difference-preview-title">
            <header class="rerun-section-heading">
              <div>
                <p class="eyebrow">Semantic Differences · 差异预览</p>
                <h3 id="difference-preview-title">语义差异账</h3>
              </div>
              <span>共 {{ loaded.comparison.differences.length }} 项</span>
            </header>

            <p v-if="differencePreview.length === 0" class="rerun-difference-preview__empty" data-testid="comparison-no-differences">
              没有差异；冻结语义投影一致。
            </p>
            <div v-else class="rerun-difference-table" data-testid="comparison-differences-preview">
              <div class="rerun-difference-table__head" aria-hidden="true">
                <span>类型</span><span>影响</span><span>路径</span><span>基线</span><span>重复</span>
              </div>
              <article v-for="difference in differencePreview" :key="difference.path">
                <strong>{{ differenceKind(difference) }}</strong>
                <em>{{ differenceImpact(difference) }}</em>
                <code :title="difference.path">{{ difference.path }}</code>
                <span :title="pretty(difference.baseline)">{{ difference.baseline_present ? compactValue(difference.baseline) : '〈不存在〉' }}</span>
                <span :title="pretty(difference.repeat)">{{ difference.repeat_present ? compactValue(difference.repeat) : '〈不存在〉' }}</span>
              </article>
            </div>

            <button
              type="button"
              data-testid="comparison-open-differences"
              data-open-comparison-panel="differences"
              @click="emit('openPanel', 'differences')"
            >
              查看全部差异与判定依据
            </button>
          </section>

          <aside
            class="rerun-judgment-details"
            :class="`rerun-judgment-details--${loaded.comparison.comparison_status.toLowerCase()}`"
            :aria-label="`复跑比较：${loaded.comparison.comparison_status}`"
          >
            <dl>
              <div><dt>核心判定</dt><dd>{{ loaded.comparison.comparison_status }}</dd></div>
              <div><dt>适用性</dt><dd>{{ loaded.comparison.comparable ? '适用' : '不适用' }}</dd></div>
              <div><dt>差异统计</dt><dd>{{ loaded.comparison.differences.length }} 项</dd></div>
              <div><dt>比较文件</dt><dd>{{ formatBytes(loaded.integrity.totalBytes) }}</dd></div>
            </dl>
          </aside>

          <aside class="rerun-boundary" aria-labelledby="rerun-boundary-title" data-testid="comparison-boundary">
            <header class="rerun-section-heading">
              <div>
                <p class="eyebrow">Applicability & Boundary · 边界</p>
                <h3 id="rerun-boundary-title">适用性与限制</h3>
              </div>
            </header>
            <dl>
              <div><dt>计划一致</dt><dd>{{ loaded.comparison.sources.baseline.plan.sha256 === loaded.comparison.sources.repeat.plan.sha256 ? '一致' : '不一致' }}</dd></div>
              <div><dt>随机种子</dt><dd>{{ loaded.comparison.sources.baseline.random_seed === loaded.comparison.sources.repeat.random_seed ? '一致' : '不一致' }}</dd></div>
              <div><dt>比较规则</dt><dd>{{ loaded.comparison.rule_version }}</dd></div>
              <div><dt>来源身份</dt><dd>分别保留</dd></div>
            </dl>
            <ul>
              <li v-for="item in loaded.comparison.limits" :key="item">{{ item }}</li>
            </ul>
            <code>{{ loaded.comparison.comparison_id }}</code>
          </aside>
        </div>
      </div>
    </template>
  </section>
</template>
