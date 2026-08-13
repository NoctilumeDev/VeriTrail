import { flushPromises, mount } from '@vue/test-utils'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import App from '../src/App.vue'
import {
  createBatchAnalysisBundle,
  createComparisonBundle,
  createMinimalBundle,
  createPairedAnalysisBundle,
  installFetchForBundles,
} from './support'

async function waitFor(wrapper: ReturnType<typeof mount>, selector: string) {
  for (let attempt = 0; attempt < 30; attempt += 1) {
    await flushPromises()
    if (wrapper.find(selector).exists()) return
    await new Promise((resolve) => setTimeout(resolve, 0))
  }
  throw new Error(`Timed out waiting for ${selector}`)
}

describe('App', () => {
  let bundles: Record<string, Map<string, Blob>>

  beforeEach(async () => {
    window.history.replaceState({}, '', '/?fixture=positive')
    bundles = {
      'm2-positive': await createMinimalBundle(),
      'm2-negative': await createMinimalBundle({
        run_id: 'unit-negative',
        verdict: 'FAIL',
        reasons: [{ code: 'NEGATIVE', message: 'Hard assertion failed.' }],
        assertions: [
          {
            id: 'negative-assertion',
            severity: 'HARD',
            status: 'FAIL',
            expected: 0,
            actual: 1,
          },
        ],
      }),
      'm2-invalid': await createMinimalBundle(),
    }
    const invalid = bundles['m2-invalid']!
    invalid.set('report.json', new Blob(['{}']))
    installFetchForBundles(bundles)
  })

  afterEach(() => {
    vi.restoreAllMocks()
  })

  it('keeps ExecutionStatus and Verdict as separate labelled dimensions', async () => {
    const wrapper = mount(App)
    await waitFor(wrapper, '[data-testid="status-gate"]')

    expect(wrapper.get('[aria-label="运行状态：COMPLETED"]').text()).toContain('COMPLETED')
    expect(wrapper.get('[aria-label="验收结论：PASS"]').text()).toContain('PASS')
    expect(wrapper.get('[data-testid="integrity-status"]').text()).toContain('自报 Verdict')
    expect(wrapper.get('[data-testid="browser-empty"]').text()).toContain('不等于浏览器检查通过')
    wrapper.unmount()
  })

  it('switches only the evidence bundle and exposes negative assertions', async () => {
    const wrapper = mount(App)
    await waitFor(wrapper, '[data-testid="status-gate"]')
    await wrapper.get('[data-testid="fixture-negative"]').trigger('click')
    await waitFor(wrapper, '[aria-label="验收结论：FAIL"]')

    expect(wrapper.get('[aria-label="验收结论：FAIL"]').text()).toContain('FAIL')
    expect(wrapper.get('[data-testid="assertion-list"]').text()).toContain('negative-assertion')
    expect(window.location.search).toBe('?fixture=negative')
    wrapper.unmount()
  })

  it('keeps every local import focus target aligned with its visible label', async () => {
    const wrapper = mount(App)
    await waitFor(wrapper, '[data-testid="status-gate"]')

    const inputs = wrapper.findAll('.local-import input[type="file"]')
    expect(inputs).toHaveLength(4)
    for (const input of inputs) {
      expect(input.element.parentElement).toBeInstanceOf(HTMLLabelElement)
      expect(input.attributes('aria-label')).toMatch(/^选择本地 VeriTrail /)
    }

    wrapper.unmount()
  })

  it('contains an invalid bundle and recovers through the explicit retry', async () => {
    const wrapper = mount(App)
    await waitFor(wrapper, '[data-testid="status-gate"]')
    await wrapper.get('[data-testid="fixture-invalid"]').trigger('click')
    await waitFor(wrapper, '[data-testid="error-state"]')

    expect(wrapper.get('[data-testid="error-state"]').text()).toContain('没有据此改写 Run 的 Verdict')
    await wrapper.get('[data-testid="retry-positive"]').trigger('click')
    await waitFor(wrapper, '[aria-label="验收结论：PASS"]')
    expect(wrapper.find('[aria-label="验收结论：PASS"]').exists()).toBe(true)
    wrapper.unmount()
  })

  it('imports a local Comparison only after manifest verification', async () => {
    const wrapper = mount(App)
    await waitFor(wrapper, '[data-testid="status-gate"]')
    const entries = await createComparisonBundle('MATCH')
    const files = [...entries].map(([name, blob]) => {
      const file = new File([blob], name, { type: blob.type })
      Object.defineProperty(file, 'webkitRelativePath', {
        value: `unit-comparison/${name}`,
      })
      return file
    })
    const input = wrapper.get('[data-testid="local-comparison-input"]')
    Object.defineProperty(input.element, 'files', { configurable: true, value: files })
    await input.trigger('change')
    await waitFor(wrapper, '[data-testid="comparison-view"]')

    expect(wrapper.get('[data-testid="comparison-status"]').text()).toContain('MATCH')
    expect(window.location.search).toBe('?fixture=comparison')
    expect(wrapper.find('[data-testid="status-gate"]').exists()).toBe(false)
    wrapper.unmount()
  })

  it('imports a local PairedAnalysis only after plan seal and manifest verification', async () => {
    const wrapper = mount(App)
    await waitFor(wrapper, '[data-testid="status-gate"]')
    const entries = await createPairedAnalysisBundle('SUPPORTED')
    const files = [...entries].map(([name, blob]) => {
      const file = new File([blob], name, { type: blob.type })
      Object.defineProperty(file, 'webkitRelativePath', {
        value: `unit-pairing/${name}`,
      })
      return file
    })
    const input = wrapper.get('[data-testid="local-pairing-input"]')
    Object.defineProperty(input.element, 'files', { configurable: true, value: files })
    await input.trigger('change')
    await waitFor(wrapper, '[data-testid="paired-analysis-view"]')

    expect(wrapper.get('[data-testid="paired-analysis-status"]').text()).toContain('SUPPORTED')
    expect(window.location.search).toBe('?fixture=pairing')
    expect(wrapper.find('[data-testid="status-gate"]').exists()).toBe(false)
    wrapper.unmount()
  })

  it('imports four explicit BatchAnalysis files and keeps local files ephemeral', async () => {
    const wrapper = mount(App)
    await waitFor(wrapper, '[data-testid="status-gate"]')
    const entries = await createBatchAnalysisBundle('SUPPORTED')
    const files = [...entries].map(([name, blob]) => new File([blob], name, { type: blob.type }))
    const input = wrapper.get('[data-testid="local-batch-input"]')
    Object.defineProperty(input.element, 'files', { configurable: true, value: files })
    await input.trigger('change')
    await waitFor(wrapper, '[data-testid="batch-analysis-view"]')

    expect(wrapper.get('[data-testid="batch-coverage-status"]').text()).toContain('COMPLETE')
    expect(wrapper.get('[data-testid="batch-hypothesis-status"]').text()).toContain('SUPPORTED')
    expect(window.location.search).toBe('?fixture=batch')
    expect(wrapper.find('[data-testid="status-gate"]').exists()).toBe(false)
    wrapper.unmount()
  })
})
