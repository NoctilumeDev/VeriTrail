import { mount } from '@vue/test-utils'
import { describe, expect, it } from 'vitest'
import BatchAnalysisView from '../src/components/BatchAnalysisView.vue'
import {
  BatchLoadError,
  loadBatchAnalysisFromBlobs,
} from '../src/domain/batch'
import { sha256Hex } from '../src/domain/bundle'
import { createBatchAnalysisBundle } from './support'

function rowOrder(wrapper: ReturnType<typeof mount>, selector: string, attribute: string): string[] {
  return wrapper
    .findAll(selector)
    .map((node) => node.attributes(attribute))
    .filter((value): value is string => value !== undefined)
}

function canonicalJson(value: unknown): string {
  if (value === null || typeof value !== 'object') return JSON.stringify(value)
  if (Array.isArray(value)) return `[${value.map(canonicalJson).join(',')}]`
  const source = value as Record<string, unknown>
  return `{${Object.keys(source)
    .sort()
    .map((key) => `${JSON.stringify(key)}:${canonicalJson(source[key])}`)
    .join(',')}}`
}

async function replaceManifestFile(
  entries: Map<string, Blob>,
  path: string,
  blob: Blob,
) {
  entries.set(path, blob)
  const manifest = JSON.parse(await entries.get('batch-analysis-manifest.json')!.text()) as {
    files: Array<{ path: string; sha256: string; size: number }>
  }
  const file = manifest.files.find((item) => item.path === path)!
  file.sha256 = await sha256Hex(blob)
  file.size = blob.size
  entries.set('batch-analysis-manifest.json', new Blob([JSON.stringify(manifest)]))
}

describe('BatchAnalysis Loader and View', () => {
  it('rebuilds COMPLETE/SUPPORTED and keeps a source FAIL visible', async () => {
    const loaded = await loadBatchAnalysisFromBlobs(await createBatchAnalysisBundle('SUPPORTED'))
    const wrapper = mount(BatchAnalysisView, { props: { loaded } })

    expect(loaded.integrity.verifiedFiles).toBe(3)
    expect(loaded.integrity.authorityVerified).toBe(false)
    expect(wrapper.get('[data-testid="batch-coverage-status"]').attributes('aria-label')).toBe(
      '覆盖状态：COMPLETE',
    )
    expect(wrapper.find('.batch-court').exists()).toBe(true)
    expect(wrapper.find('.comparison-court').exists()).toBe(false)
    expect(wrapper.get('[data-testid="view-batch-title"]').attributes('id')).toBe('view-batch-title')
    expect(wrapper.get('[data-testid="batch-status-gate"]').text()).toContain('CoverageStatus')
    expect(wrapper.get('[data-testid="batch-hypothesis-status"]').text()).toContain('SUPPORTED')
    expect(wrapper.get('[data-testid="batch-profile-matrix"]').text()).toContain('combined')
    expect(wrapper.get('[data-testid="batch-wave-list"]').text()).toContain('FAIL')
    expect(wrapper.get('.batch-slot__identity-copy').text()).toContain('baseline')
    expect(wrapper.get('.batch-slot__identity-copy').text()).toContain('coverage-01')
    expect(wrapper.get('[data-testid="batch-boundary"]').text()).toContain('不证明真实并行')
    expect(
      rowOrder(wrapper, '[data-testid="batch-profile-matrix"] tbody tr', 'data-batch-profile'),
    ).toEqual(loaded.analysis.profiles.map((profile) => profile.id))
    expect(rowOrder(wrapper, '[data-testid="batch-wave-list"] [data-batch-slot]', 'data-batch-slot')).toEqual(
      loaded.analysis.slots.map((slot) => slot.slot_id),
    )
  })

  it('retains stable mismatches as COMPLETE/CONTRADICTED', async () => {
    const loaded = await loadBatchAnalysisFromBlobs(await createBatchAnalysisBundle('CONTRADICTED'))
    const wrapper = mount(BatchAnalysisView, { props: { loaded } })

    expect(loaded.analysis.coverage_status).toBe('COMPLETE')
    expect(loaded.analysis.hypothesis_status).toBe('CONTRADICTED')
    expect(wrapper.get('[data-testid="batch-profile-matrix"]').text()).toContain('2')
    expect(wrapper.get('[data-testid="batch-reasons"]').text()).toContain(
      'BATCH_HYPOTHESIS_CONTRADICTED',
    )
    expect(wrapper.get('[data-testid="batch-status-gate"]').text()).toContain('COMPLETE')
    expect(wrapper.get('[data-testid="batch-status-gate"]').text()).toContain('CONTRADICTED')
  })

  it('keeps missing and contaminated matrices distinct', async () => {
    const incomplete = await loadBatchAnalysisFromBlobs(await createBatchAnalysisBundle('INCOMPLETE'))
    const contaminated = await loadBatchAnalysisFromBlobs(await createBatchAnalysisBundle('INCONCLUSIVE'))

    expect(incomplete.analysis.coverage_status).toBe('INCOMPLETE')
    expect(incomplete.analysis.slots.some((slot) => slot.source === null)).toBe(true)
    expect(contaminated.analysis.coverage_status).toBe('INCONCLUSIVE')
    expect(contaminated.analysis.unplanned_differences).toHaveLength(1)

    const incompleteWrapper = mount(BatchAnalysisView, { props: { loaded: incomplete } })
    const contaminatedWrapper = mount(BatchAnalysisView, { props: { loaded: contaminated } })
    expect(incompleteWrapper.get('[data-testid="batch-wave-list"]').text()).toContain('MISSING')
    expect(incompleteWrapper.get('[data-testid="batch-wave-list"]').text()).toContain('来源 Run 未提供')
    expect(contaminatedWrapper.get('[data-testid="batch-reasons"]').text()).toContain(
      'UNDECLARED_OUTCOME_DRIFT',
    )
  })

  it('keeps a long Profile ID, local matrix region, and native outcome details in their owned areas', async () => {
    const loaded = await loadBatchAnalysisFromBlobs(await createBatchAnalysisBundle('SUPPORTED'))
    loaded.analysis.profiles[0]!.id = `long-${'profile-id-'.repeat(20)}baseline`
    const wrapper = mount(BatchAnalysisView, { props: { loaded } })

    expect(wrapper.get('[data-testid="batch-profile-matrix"]').text()).toContain(
      loaded.analysis.profiles[0]!.id,
    )
    const matrixRegion = wrapper.get('[aria-label="全因子 Profile 矩阵"]')
    expect(matrixRegion.attributes('role')).toBe('region')
    expect(matrixRegion.attributes('tabindex')).toBe('0')
    expect(wrapper.get('[data-testid="batch-wave-list"] details').element).toBeInstanceOf(
      HTMLDetailsElement,
    )
  })

  it('accepts producer-declared incomplete source evidence without inventing boundary failures', async () => {
    const entries = await createBatchAnalysisBundle('SUPPORTED')
    const analysis = JSON.parse(await entries.get('batch-analysis.json')!.text()) as {
      coverage_status: string
      hypothesis_status: string
      reasons: Array<{ code: string; message: string }>
      slots: Array<{ source: null | Record<string, unknown> }>
    }
    analysis.coverage_status = 'INCOMPLETE'
    analysis.hypothesis_status = 'INCONCLUSIVE'
    analysis.reasons = [{ code: 'SOURCE_EVIDENCE_INCOMPLETE', message: 'Required source evidence is missing.' }]
    analysis.slots[0]!.source!.preflight_complete = false
    analysis.slots[0]!.source!.cleanup_complete = false
    analysis.slots[0]!.source!.browser_complete = false
    await replaceManifestFile(entries, 'batch-analysis.json', new Blob([JSON.stringify(analysis)]))

    const loaded = await loadBatchAnalysisFromBlobs(entries)
    expect(loaded.analysis.coverage_status).toBe('INCOMPLETE')
    expect(loaded.analysis.hypothesis_status).toBe('INCONCLUSIVE')
  })

  it('rejects a changed BatchPlan even when its manifest hash is recomputed', async () => {
    const entries = await createBatchAnalysisBundle('SUPPORTED')
    const plan = JSON.parse(await entries.get('sealed-batch-plan.json')!.text()) as Record<string, unknown>
    plan.question = 'Changed after seal.'
    await replaceManifestFile(entries, 'sealed-batch-plan.json', new Blob([JSON.stringify(plan)]))

    await expect(loadBatchAnalysisFromBlobs(entries)).rejects.toMatchObject({
      code: 'BATCH_PLAN_SEAL_MISMATCH',
    })
  })

  it('rejects a resealed but forged perturbation order', async () => {
    const entries = await createBatchAnalysisBundle('SUPPORTED')
    const plan = JSON.parse(await entries.get('sealed-batch-plan.json')!.text()) as Record<
      string,
      unknown
    >
    const schedule = plan.schedule as Array<Record<string, unknown>>
    const left = schedule[4]!.profile_id
    schedule[4]!.profile_id = schedule[5]!.profile_id
    schedule[5]!.profile_id = left
    const unsigned = { ...plan }
    delete unsigned.seal
    plan.seal = {
      algorithm: 'sha256',
      digest: await sha256Hex(new Blob([canonicalJson(unsigned)])),
    }
    await replaceManifestFile(entries, 'sealed-batch-plan.json', new Blob([JSON.stringify(plan)]))

    await expect(loadBatchAnalysisFromBlobs(entries)).rejects.toMatchObject({
      code: 'BATCH_PLAN_CONFLICT',
    })
  })

  it('rejects extra files and a dual-state conflict before exposing partial facts', async () => {
    const extra = await createBatchAnalysisBundle('SUPPORTED')
    extra.set('extra.json', new Blob(['{}']))
    await expect(loadBatchAnalysisFromBlobs(extra)).rejects.toBeInstanceOf(BatchLoadError)

    const conflict = await createBatchAnalysisBundle('SUPPORTED')
    const analysis = JSON.parse(await conflict.get('batch-analysis.json')!.text()) as Record<
      string,
      unknown
    >
    analysis.hypothesis_status = 'CONTRADICTED'
    await replaceManifestFile(conflict, 'batch-analysis.json', new Blob([JSON.stringify(analysis)]))
    await expect(loadBatchAnalysisFromBlobs(conflict)).rejects.toMatchObject({
      code: 'BATCH_STATE_CONFLICT',
    })
  })
})
