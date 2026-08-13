import { mount } from '@vue/test-utils'
import { describe, expect, it } from 'vitest'
import PairedAnalysisView from '../src/components/PairedAnalysisView.vue'
import {
  loadPairedAnalysisFromBlobs,
  PairingLoadError,
} from '../src/domain/pairing'
import { sha256Hex } from '../src/domain/bundle'
import { createPairedAnalysisBundle } from './support'

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
    expect(wrapper.get('[data-testid="paired-sequence"]').text()).toContain('NEGATIVE_CONTROL')
    expect(wrapper.get('[data-testid="paired-sources"]').text()).toContain('unit-treatment')
    expect(wrapper.get('[data-testid="paired-sources"]').text()).toContain('FAIL')
    expect(wrapper.get('[data-testid="paired-outcomes"]').text()).toContain('suite-completed')
    expect(wrapper.get('[data-testid="paired-boundary"]').text()).toContain('不等于')
  })

  it('retains a complete treatment counterexample as CONTRADICTED', async () => {
    const loaded = await loadPairedAnalysisFromBlobs(
      await createPairedAnalysisBundle('CONTRADICTED'),
    )
    const wrapper = mount(PairedAnalysisView, { props: { loaded } })

    expect(loaded.analysis.attributable).toBe(true)
    expect(wrapper.get('[data-testid="paired-analysis-status"]').text()).toContain('CONTRADICTED')
    expect(wrapper.get('[data-testid="paired-outcomes"]').text()).toContain('不符')
  })

  it('retains a negative-control effect as INCONCLUSIVE', async () => {
    const loaded = await loadPairedAnalysisFromBlobs(
      await createPairedAnalysisBundle('INCONCLUSIVE'),
    )

    expect(loaded.analysis.attributable).toBe(false)
    expect(loaded.analysis.sources.NEGATIVE_CONTROL.verdict).toBe('FAIL')
    expect(loaded.analysis.outcomes[0]?.roles.NEGATIVE_CONTROL.matches).toBe(false)
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
