import { mount } from '@vue/test-utils'
import { describe, expect, it } from 'vitest'
import BatchAnalysisView from '../src/components/BatchAnalysisView.vue'
import {
  BatchLoadError,
  loadBatchAnalysisFromBlobs,
} from '../src/domain/batch'
import { sha256Hex } from '../src/domain/bundle'
import { createBatchAnalysisBundle } from './support'

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
    expect(wrapper.get('[data-testid="batch-coverage-status"]').attributes('aria-label')).toBe(
      '覆盖状态：COMPLETE',
    )
    expect(wrapper.get('[data-testid="batch-hypothesis-status"]').text()).toContain('SUPPORTED')
    expect(wrapper.get('[data-testid="batch-profile-matrix"]').text()).toContain('combined')
    expect(wrapper.get('[data-testid="batch-wave-list"]').text()).toContain('FAIL')
    expect(wrapper.get('[data-testid="batch-boundary"]').text()).toContain('不证明真实并行')
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
  })

  it('keeps missing and contaminated matrices distinct', async () => {
    const incomplete = await loadBatchAnalysisFromBlobs(await createBatchAnalysisBundle('INCOMPLETE'))
    const contaminated = await loadBatchAnalysisFromBlobs(await createBatchAnalysisBundle('INCONCLUSIVE'))

    expect(incomplete.analysis.coverage_status).toBe('INCOMPLETE')
    expect(incomplete.analysis.slots.some((slot) => slot.source === null)).toBe(true)
    expect(contaminated.analysis.coverage_status).toBe('INCONCLUSIVE')
    expect(contaminated.analysis.unplanned_differences).toHaveLength(1)
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
