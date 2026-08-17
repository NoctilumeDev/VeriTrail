import { mount } from '@vue/test-utils'
import { describe, expect, it } from 'vitest'
import PairedAnalysisView from '../src/components/PairedAnalysisView.vue'
import {
  loadPairedAnalysisFromBlobs,
  PairingLoadError,
} from '../src/domain/pairing'
import { sha256Hex } from '../src/domain/bundle'
import { createPairedAnalysisBundle } from './support'

const ROLES = ['BASELINE', 'TREATMENT', 'RESTORED_BASELINE', 'NEGATIVE_CONTROL']

function roleOrder(wrapper: ReturnType<typeof mount>, selector: string): string[] {
  return wrapper
    .findAll(`${selector} [data-pairing-role]`)
    .map((node) => node.attributes('data-pairing-role'))
    .filter((role): role is string => role !== undefined)
}

describe('PairedAnalysis Loader and View', () => {
  it('verifies SUPPORTED and displays all four source Verdicts independently', async () => {
    const loaded = await loadPairedAnalysisFromBlobs(
      await createPairedAnalysisBundle('SUPPORTED'),
    )
    const wrapper = mount(PairedAnalysisView, { props: { loaded } })

    expect(loaded.analysis.analysis_status).toBe('SUPPORTED')
    expect(loaded.integrity.verifiedFiles).toBe(3)
    expect(loaded.integrity.authorityVerified).toBe(false)
    expect(wrapper.get('[data-testid="paired-analysis-status"]').attributes('aria-label')).toBe(
      '配对分析：SUPPORTED',
    )
    expect(wrapper.find('.pairing-page').exists()).toBe(true)
    expect(wrapper.find('.comparison-court').exists()).toBe(false)
    expect(roleOrder(wrapper, '[data-testid="paired-sequence"]')).toEqual(ROLES)
    expect(wrapper.findAll('.pairing-sequence__emblem')).toHaveLength(4)
    expect(wrapper.get('[data-testid="pairing-open-sources"]').text()).toContain('来源账册')
    expect(wrapper.get('[data-testid="pairing-open-outcomes"]').text()).toContain('全部 1 项断言')

    await wrapper.setProps({ panel: 'sources' })
    expect(wrapper.get('[data-testid="pairing-panel-court"]').classes()).toContain('pairing-court')
    expect(roleOrder(wrapper, '[data-testid="paired-sources"]')).toEqual(ROLES)
    expect(wrapper.get('[data-testid="paired-sources"]').text()).toContain('unit-treatment')
    expect(wrapper.get('[data-testid="paired-sources"]').text()).toContain('FAIL')

    await wrapper.setProps({ panel: 'outcomes' })
    expect(wrapper.get('[data-testid="pairing-panel-court"]').classes()).toContain('pairing-court')
    expect(roleOrder(wrapper, '[data-testid="paired-outcomes"]')).toEqual(ROLES)
    expect(wrapper.get('[data-testid="paired-outcomes"]').text()).toContain('suite-completed')

    await wrapper.setProps({ panel: null })
    expect(wrapper.get('[data-testid="paired-boundary"]').text()).toContain('不等于')
  })

  it('retains a complete treatment counterexample as CONTRADICTED', async () => {
    const loaded = await loadPairedAnalysisFromBlobs(
      await createPairedAnalysisBundle('CONTRADICTED'),
    )
    const wrapper = mount(PairedAnalysisView, { props: { loaded } })

    expect(loaded.analysis.attributable).toBe(true)
    expect(wrapper.get('.pairing-heading__status').text()).toContain('CONTRADICTED')
    await wrapper.setProps({ panel: 'sources' })
    const treatmentSourceText = wrapper.get('[data-testid="paired-sources"] [data-pairing-role="TREATMENT"]').text()
    await wrapper.setProps({ panel: 'outcomes' })
    const treatmentOutcomeText = wrapper.get('[data-testid="paired-outcomes"] [data-pairing-role="TREATMENT"]').text()
    expect(treatmentSourceText).toContain('PASS')
    expect(treatmentOutcomeText).toContain('不符')
  })

  it('retains a negative-control effect as INCONCLUSIVE', async () => {
    const loaded = await loadPairedAnalysisFromBlobs(
      await createPairedAnalysisBundle('INCONCLUSIVE'),
    )
    const wrapper = mount(PairedAnalysisView, { props: { loaded } })

    expect(loaded.analysis.attributable).toBe(false)
    expect(loaded.analysis.sources.NEGATIVE_CONTROL.verdict).toBe('FAIL')
    expect(loaded.analysis.outcomes[0]?.roles.NEGATIVE_CONTROL.matches).toBe(false)
    expect(wrapper.get('.pairing-heading__status').text()).toContain('INCONCLUSIVE')
    await wrapper.setProps({ panel: 'outcomes' })
    expect(
      wrapper.get('[data-testid="paired-outcomes"] [data-pairing-role="NEGATIVE_CONTROL"]').text(),
    ).toContain('不符')
  })

  it('keeps an unusually long source Run ID within the named source record', async () => {
    const loaded = await loadPairedAnalysisFromBlobs(
      await createPairedAnalysisBundle('SUPPORTED'),
    )
    loaded.analysis.sources.BASELINE.run_id = `long-${'run-id-'.repeat(24)}baseline`
    const wrapper = mount(PairedAnalysisView, { props: { loaded, panel: 'sources' } })

    const baseline = wrapper.get('[data-testid="paired-sources"] [data-pairing-role="BASELINE"]')
    expect(baseline.text()).toContain(loaded.analysis.sources.BASELINE.run_id)
  })

  it('opens full ledgers and exposes a reversible return interaction', async () => {
    const loaded = await loadPairedAnalysisFromBlobs(
      await createPairedAnalysisBundle('SUPPORTED'),
    )
    const wrapper = mount(PairedAnalysisView, { props: { loaded } })

    await wrapper.get('[data-testid="pairing-open-sources"]').trigger('click')
    await wrapper.get('[data-testid="pairing-open-outcomes"]').trigger('click')
    expect(wrapper.emitted('openPanel')).toEqual([['sources'], ['outcomes']])

    await wrapper.setProps({ panel: 'sources' })
    await wrapper.get('[data-testid="pairing-panel-return"]').trigger('click')
    expect(wrapper.emitted('closePanel')).toEqual([[]])
  })

  it('rejects a changed PairingPlan even when the manifest hash is recomputed', async () => {
    const entries = await createPairedAnalysisBundle('SUPPORTED')
    const plan = JSON.parse(await entries.get('sealed-pairing-plan.json')!.text()) as Record<
      string,
      unknown
    >
    plan.question = 'Changed after seal.'
    const changed = new Blob([JSON.stringify(plan)])
    entries.set('sealed-pairing-plan.json', changed)
    const manifest = JSON.parse(await entries.get('paired-analysis-manifest.json')!.text()) as {
      files: Array<{ path: string; sha256: string; size: number }>
    }
    const file = manifest.files.find((item) => item.path === 'sealed-pairing-plan.json')!
    file.sha256 = await sha256Hex(changed)
    file.size = changed.size
    entries.set('paired-analysis-manifest.json', new Blob([JSON.stringify(manifest)]))

    await expect(loadPairedAnalysisFromBlobs(entries)).rejects.toMatchObject({
      code: 'PAIRING_PLAN_SEAL_MISMATCH',
    })
  })

  it('rejects extra files and a state conflict before exposing partial facts', async () => {
    const extra = await createPairedAnalysisBundle('SUPPORTED')
    extra.set('extra.json', new Blob(['{}']))
    await expect(loadPairedAnalysisFromBlobs(extra)).rejects.toBeInstanceOf(PairingLoadError)

    const conflict = await createPairedAnalysisBundle('SUPPORTED')
    const analysis = JSON.parse(await conflict.get('paired-analysis.json')!.text()) as Record<
      string,
      unknown
    >
    analysis.analysis_status = 'INCONCLUSIVE'
    const changed = new Blob([JSON.stringify(analysis)])
    conflict.set('paired-analysis.json', changed)
    const manifest = JSON.parse(await conflict.get('paired-analysis-manifest.json')!.text()) as {
      files: Array<{ path: string; sha256: string; size: number }>
    }
    const file = manifest.files.find((item) => item.path === 'paired-analysis.json')!
    file.sha256 = await sha256Hex(changed)
    file.size = changed.size
    conflict.set('paired-analysis-manifest.json', new Blob([JSON.stringify(manifest)]))
    await expect(loadPairedAnalysisFromBlobs(conflict)).rejects.toMatchObject({
      code: 'PAIRING_STATE_CONFLICT',
    })
  })
})
