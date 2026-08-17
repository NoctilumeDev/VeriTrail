import { mount } from '@vue/test-utils'
import { describe, expect, it } from 'vitest'
import ComparisonView from '../src/components/ComparisonView.vue'
import {
  ComparisonLoadError,
  loadComparisonFromBlobs,
} from '../src/domain/comparison'
import { sha256Hex } from '../src/domain/bundle'
import { createComparisonBundle } from './support'

describe('Comparison Loader and View', () => {
  it('verifies a MATCH bundle and displays a status independent of Run Verdict', async () => {
    const loaded = await loadComparisonFromBlobs(await createComparisonBundle('MATCH'))
    const wrapper = mount(ComparisonView, { props: { loaded } })

    expect(loaded.comparison.comparison_status).toBe('MATCH')
    expect(loaded.integrity.verifiedFiles).toBe(2)
    expect(loaded.integrity.authorityVerified).toBe(false)
    expect(wrapper.get('[data-testid="comparison-status"]').attributes('aria-label')).toBe('复跑比较：MATCH')
    expect(wrapper.get('[data-testid="comparison-view"]').classes()).toContain('rerun-page--match')
    expect(wrapper.get('[data-testid="comparison-sources"]').text()).toContain('unit-baseline')
    expect(wrapper.get('[data-testid="comparison-sources"]').text()).toContain('PASS')
    expect(wrapper.findAll('[data-testid^="comparison-source-"]').map((item) => item.attributes('data-testid'))).toEqual([
      'comparison-source-baseline',
      'comparison-source-repeat',
    ])
    expect(wrapper.get('[data-testid="comparison-no-differences"]').text()).toContain('没有差异')
    expect(wrapper.get('[data-testid="comparison-boundary"]').text()).toContain('不等于')
  })

  it('displays a DRIFT path with both source values', async () => {
    const loaded = await loadComparisonFromBlobs(await createComparisonBundle('DRIFT'))
    const wrapper = mount(ComparisonView, { props: { loaded } })

    expect(wrapper.get('[data-testid="comparison-status"]').text()).toContain('DRIFT')
    expect(wrapper.get('[data-testid="comparison-view"]').classes()).toContain('rerun-page--drift')
    expect(wrapper.get('[data-testid="comparison-differences-preview"]').text()).toContain('/verdict')
    expect(wrapper.get('[data-testid="comparison-differences-preview"]').text()).toContain('FAIL')

    await wrapper.get('[data-testid="comparison-open-differences"]').trigger('click')
    expect(wrapper.emitted('openPanel')).toEqual([['differences']])

    await wrapper.setProps({ panel: 'differences' })
    expect(wrapper.get('[data-testid="comparison-differences"]').text()).toContain('/verdict')
    await wrapper.get('[data-testid="comparison-panel-return-bottom"]').trigger('click')
    expect(wrapper.emitted('closePanel')).toHaveLength(1)
  })

  it('retains a non-comparable input as INCONCLUSIVE', async () => {
    const loaded = await loadComparisonFromBlobs(await createComparisonBundle('INCONCLUSIVE'))
    const wrapper = mount(ComparisonView, { props: { loaded } })

    expect(loaded.comparison.comparable).toBe(false)
    expect(loaded.comparison.sources.repeat.execution_status).toBe('ABORTED')
    expect(wrapper.get('[data-testid="comparison-view"]').classes()).toContain('rerun-page--inconclusive')
  })

  it('rejects a changed comparison before exposing partial facts', async () => {
    const entries = await createComparisonBundle('MATCH')
    entries.set('comparison.json', new Blob(['{}']))

    await expect(loadComparisonFromBlobs(entries)).rejects.toMatchObject({
      code: 'COMPARISON_SIZE_MISMATCH',
    })
  })

  it('rejects extra, missing, and state-conflicting files', async () => {
    const extra = await createComparisonBundle('MATCH')
    extra.set('extra.json', new Blob(['{}']))
    await expect(loadComparisonFromBlobs(extra)).rejects.toBeInstanceOf(ComparisonLoadError)

    const missing = await createComparisonBundle('MATCH')
    missing.delete('comparison.md')
    await expect(loadComparisonFromBlobs(missing)).rejects.toMatchObject({
      code: 'COMPARISON_FILE_SET_MISMATCH',
    })

    const conflict = await createComparisonBundle('MATCH')
    const comparison = JSON.parse(await conflict.get('comparison.json')!.text()) as Record<string, unknown>
    comparison.comparison_status = 'DRIFT'
    const changed = new Blob([JSON.stringify(comparison)])
    conflict.set('comparison.json', changed)
    const manifest = JSON.parse(await conflict.get('comparison-manifest.json')!.text()) as {
      files: Array<{ path: string; sha256: string; size: number }>
    }
    const entry = manifest.files.find((file) => file.path === 'comparison.json')!
    entry.sha256 = await sha256Hex(changed)
    entry.size = changed.size
    conflict.set('comparison-manifest.json', new Blob([JSON.stringify(manifest)]))
    await expect(loadComparisonFromBlobs(conflict)).rejects.toMatchObject({
      code: 'COMPARISON_STATE_CONFLICT',
    })
  })
})
