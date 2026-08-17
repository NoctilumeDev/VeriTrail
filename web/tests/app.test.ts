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

async function selectPublicView(
  wrapper: ReturnType<typeof mount>,
  view: 'runs' | 'comparison' | 'pairing' | 'batch',
) {
  const target = `[data-testid="cross-axis-${view}"]`
  if (!wrapper.find(target).exists()) {
    await wrapper.get('[data-testid="cross-axis-toggle"]').trigger('click')
  }
  const targetButton = wrapper.get(target)
  if (targetButton.attributes('aria-current') === 'page') return
  if (!targetButton.isVisible()) {
    await wrapper.get('[data-testid="cross-axis-toggle"]').trigger('click')
  }
  await wrapper.get(target).trigger('click')
  await flushPromises()
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
      'm6-comparison-drift': await createComparisonBundle('DRIFT'),
      'm7-paired-supported': await createPairedAnalysisBundle('SUPPORTED'),
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
    expect(wrapper.get('.app-shell').classes()).toContain('app-shell--runs')
    expect(wrapper.get('.app-shell').classes()).toContain('app-shell--run-detail')
    expect(wrapper.get('.app-shell').classes()).not.toContain('app-shell--inner')
    expect(wrapper.find('[data-testid="run-catalog"]').exists()).toBe(false)
    wrapper.unmount()
  })

  it('selects the URL-owned page before the Catalog API resolves', async () => {
    window.history.replaceState({}, '', '/?fixture=pairing&sample=supported')
    const fetchMock = vi.mocked(globalThis.fetch)
    const fixtureFetch = fetchMock.getMockImplementation()!
    let continueCatalog!: () => void
    const catalogGate = new Promise<void>((resolve) => {
      continueCatalog = resolve
    })
    fetchMock.mockImplementation(async (input) => {
      const url = new URL(
        typeof input === 'string' ? input : input instanceof URL ? input.href : input.url,
        window.location.href,
      )
      if (url.pathname === '/api/v1/catalog') await catalogGate
      return fixtureFetch(input)
    })

    const wrapper = mount(App)
    expect(wrapper.get('.app-shell').classes()).toContain('app-shell--pairing')
    expect(wrapper.find('[data-testid="run-catalog"]').exists()).toBe(false)
    expect(wrapper.find('.view-introduction--runs').exists()).toBe(false)

    continueCatalog()
    await waitFor(wrapper, '[data-testid="paired-analysis-view"]')
    expect(wrapper.get('[data-testid="paired-analysis-status"]').text()).toContain('SUPPORTED')
    wrapper.unmount()
  })

  it('switches only the evidence bundle and exposes negative assertions', async () => {
    const wrapper = mount(App)
    await waitFor(wrapper, '[data-testid="status-gate"]')
    await wrapper.get('[data-testid="catalog-return"]').trigger('click')
    await waitFor(wrapper, '[data-testid="fixture-negative"]')
    expect(wrapper.get('.app-shell').classes()).toContain('app-shell--runs')
    expect(wrapper.get('.app-shell').classes()).toContain('app-shell--catalog')
    await wrapper.get('[data-testid="fixture-negative"]').trigger('click')
    await waitFor(wrapper, '[aria-label="验收结论：FAIL"]')

    expect(wrapper.get('[aria-label="验收结论：FAIL"]').text()).toContain('FAIL')
    expect(wrapper.get('[data-testid="assertion-list"]').text()).toContain('negative-assertion')
    expect(window.location.search).toBe('?fixture=negative')
    wrapper.unmount()
  })

  it('keeps the shared Runs shell and viewport origin stable when returning to Catalog', async () => {
    const wrapper = mount(App)
    await waitFor(wrapper, '[data-testid="status-gate"]')
    document.documentElement.scrollTop = 120
    document.body.scrollTop = 120

    await wrapper.get('[data-testid="catalog-return"]').trigger('click')
    await flushPromises()

    expect(wrapper.get('.app-shell').classes()).toEqual(expect.arrayContaining([
      'app-shell--runs',
      'app-shell--catalog',
    ]))
    expect(wrapper.get('.app-shell').classes()).not.toContain('app-shell--run-detail')
    expect(document.documentElement.scrollTop).toBe(0)
    expect(document.body.scrollTop).toBe(0)
    wrapper.unmount()
  })

  it('commits the shared Catalog return on primary pointerdown and keeps click as the keyboard fallback', async () => {
    const pointerWrapper = mount(App, { attachTo: document.body })
    await waitFor(pointerWrapper, '[data-testid="status-gate"]')

    const pointerDown = new Event('pointerdown', { bubbles: true })
    Object.defineProperties(pointerDown, {
      isPrimary: { value: true },
      pointerType: { value: 'mouse' },
      button: { value: 0 },
    })
    pointerWrapper.get('[data-testid="catalog-return"]').element.dispatchEvent(pointerDown)
    await flushPromises()

    expect(pointerWrapper.find('[data-testid="status-gate"]').exists()).toBe(false)
    expect(pointerWrapper.find('[data-testid="run-catalog"]').exists()).toBe(true)
    expect(window.location.search).toBe('')

    const catalogAction = pointerWrapper.get('[data-testid="fixture-positive"]')
    const clickThrough = new MouseEvent('click', { bubbles: true, cancelable: true, detail: 1 })
    expect(catalogAction.element.dispatchEvent(clickThrough)).toBe(false)
    await flushPromises()
    expect(pointerWrapper.find('[data-testid="run-catalog"]').exists()).toBe(true)
    expect(window.location.search).toBe('')
    pointerWrapper.unmount()

    window.history.replaceState({}, '', '/?fixture=negative')
    const keyboardWrapper = mount(App)
    await waitFor(keyboardWrapper, '[aria-label="验收结论：FAIL"]')

    await keyboardWrapper.get('[data-testid="catalog-return"]').trigger('click')
    await flushPromises()

    expect(keyboardWrapper.find('[aria-label="验收结论：FAIL"]').exists()).toBe(false)
    expect(keyboardWrapper.find('[data-testid="run-catalog"]').exists()).toBe(true)
    expect(window.location.search).toBe('')
    keyboardWrapper.unmount()
  })

  it('keeps the destination surface mounted while a Run is being verified', async () => {
    const wrapper = mount(App)
    await waitFor(wrapper, '[data-testid="status-gate"]')
    await wrapper.get('[data-testid="catalog-return"]').trigger('click')
    await waitFor(wrapper, '[data-testid="fixture-negative"]')

    const fetchMock = vi.mocked(globalThis.fetch)
    const fixtureFetch = fetchMock.getMockImplementation()!
    let continueNegative!: () => void
    const negativeGate = new Promise<void>((resolve) => {
      continueNegative = resolve
    })
    fetchMock.mockImplementation(async (input) => {
      const url = new URL(typeof input === 'string' ? input : input instanceof URL ? input.href : input.url)
      if (url.pathname.includes('/fixtures/m2-negative/')) await negativeGate
      return fixtureFetch(input)
    })

    await wrapper.get('[data-testid="fixture-negative"]').trigger('click')
    await flushPromises()
    expect(wrapper.get('.app-shell').classes()).toContain('app-shell--run-detail')
    expect(wrapper.find('[data-testid="run-detail-loading"]').exists()).toBe(true)
    expect(wrapper.find('[data-testid="run-catalog"]').exists()).toBe(false)
    expect(wrapper.find('[data-testid="fixture-negative"]').exists()).toBe(false)

    continueNegative()
    await waitFor(wrapper, '[aria-label="验收结论：FAIL"]')
    await wrapper.get('[data-testid="catalog-return"]').trigger('click')
    expect(wrapper.find('[data-testid="fixture-negative"]').exists()).toBe(true)
    expect(wrapper.find('[data-testid="status-gate"]').exists()).toBe(false)
    wrapper.unmount()
  })

  it('loads the explicit review samples without weakening local-file privacy routes', async () => {
    window.history.replaceState({}, '', '/?fixture=pairing&sample=supported')
    const pairing = mount(App)
    await waitFor(pairing, '[data-testid="paired-analysis-view"]')
    expect(pairing.get('[data-testid="paired-analysis-status"]').text()).toContain('SUPPORTED')
    pairing.unmount()

    window.history.replaceState({}, '', '/?fixture=comparison&sample=drift')
    const comparison = mount(App)
    await waitFor(comparison, '[data-testid="comparison-view"]')
    expect(comparison.get('[data-testid="comparison-status"]').text()).toContain('DRIFT')
    comparison.unmount()
  })

  it('keeps each local import focus target in its relevant public view', async () => {
    const wrapper = mount(App)
    await waitFor(wrapper, '[data-testid="status-gate"]')
    await wrapper.get('[data-testid="catalog-return"]').trigger('click')
    await waitFor(wrapper, '[data-testid="runs-toolstrip"]')

    const inputs = wrapper.findAll('.local-import input[type="file"]')
    expect(inputs).toHaveLength(1)
    for (const input of inputs) {
      expect(input.element.parentElement).toBeInstanceOf(HTMLLabelElement)
      expect(input.attributes('aria-label')).toMatch(/^选择本地 VeriTrail /)
    }

    await selectPublicView(wrapper, 'comparison')
    expect(wrapper.get('[data-testid="local-comparison-input"]').element.parentElement).toBeInstanceOf(HTMLLabelElement)
    expect(wrapper.find('[data-testid="run-catalog"]').exists()).toBe(false)
    expect(window.location.search).toBe('?view=comparison')

    await selectPublicView(wrapper, 'pairing')
    expect(wrapper.get('[data-testid="local-pairing-input"]').element.parentElement).toBeInstanceOf(HTMLLabelElement)

    await selectPublicView(wrapper, 'batch')
    expect(wrapper.get('[data-testid="local-batch-input"]').element.parentElement).toBeInstanceOf(HTMLLabelElement)
    expect(wrapper.get('.app-shell').classes()).toContain('app-shell--batch')
    expect(wrapper.get('.app-shell').classes()).not.toContain('app-shell--inner')

    wrapper.unmount()
  })

  it('moves focus to the history destination without stealing focus on initial load', async () => {
    const host = document.createElement('div')
    document.body.append(host)
    const wrapper = mount(App, { attachTo: host })
    await waitFor(wrapper, '[data-testid="status-gate"]')
    expect(document.activeElement?.id).not.toBe('view-runs-title')

    await selectPublicView(wrapper, 'comparison')
    expect(document.activeElement?.id).toBe('view-comparison-title')

    window.history.replaceState({}, '', '/')
    window.dispatchEvent(new PopStateEvent('popstate'))
    await waitFor(wrapper, '[data-testid="view-runs-title"]')
    await flushPromises()
    expect(document.activeElement?.id).toBe('view-runs-title')

    window.history.replaceState({}, '', '/?view=comparison')
    window.dispatchEvent(new PopStateEvent('popstate'))
    await waitFor(wrapper, '[data-testid="view-comparison-title"]')
    await flushPromises()
    expect(document.activeElement?.id).toBe('view-comparison-title')

    wrapper.unmount()
    host.remove()
  })

  it('keeps demo fixtures and the local evidence directory as separate Runs source groups', async () => {
    const wrapper = mount(App)
    await waitFor(wrapper, '[data-testid="status-gate"]')
    await wrapper.get('[data-testid="catalog-return"]').trigger('click')
    await waitFor(wrapper, '[data-testid="runs-toolstrip"]')

    const toolstrip = wrapper.get('[data-testid="runs-toolstrip"]')
    expect(toolstrip.get('[role="group"]').attributes('aria-label')).toBe('示例证据')
    expect(toolstrip.get('[data-testid="fixture-positive"]').text()).toBe('正向证据')
    expect(toolstrip.get('[data-testid="fixture-negative"]').text()).toBe('负向证据')
    expect(toolstrip.get('[data-testid="fixture-invalid"]').text()).toBe('校验损坏包')
    expect(toolstrip.get('[data-testid="local-bundle-input"]').element.parentElement).toBeInstanceOf(HTMLLabelElement)
    wrapper.unmount()
  })

  it('contains an invalid bundle and recovers through the explicit retry', async () => {
    const wrapper = mount(App)
    await waitFor(wrapper, '[data-testid="status-gate"]')
    await wrapper.get('[data-testid="catalog-return"]').trigger('click')
    await waitFor(wrapper, '[data-testid="fixture-invalid"]')
    await wrapper.get('[data-testid="fixture-invalid"]').trigger('click')
    await waitFor(wrapper, '[data-testid="error-state"]')

    expect(wrapper.get('[data-testid="error-state"]').attributes('data-state-kind')).toBe('invalid')
    expect(wrapper.get('[data-testid="error-state"]').text()).toContain('没有据此改写 Run 的 Verdict')

    const fetchMock = vi.mocked(globalThis.fetch)
    const fixtureFetch = fetchMock.getMockImplementation()!
    let continuePositive!: () => void
    const positiveGate = new Promise<void>((resolve) => {
      continuePositive = resolve
    })
    fetchMock.mockImplementation(async (input) => {
      const url = new URL(typeof input === 'string' ? input : input instanceof URL ? input.href : input.url)
      if (url.pathname.includes('/fixtures/m2-positive/')) await positiveGate
      return fixtureFetch(input)
    })

    await wrapper.get('[data-testid="retry-positive"]').trigger('click')
    await flushPromises()
    expect(wrapper.get('.app-shell').classes()).toContain('app-shell--run-detail')
    expect(wrapper.find('[data-testid="run-detail-loading"]').exists()).toBe(true)
    expect(wrapper.find('[data-testid="run-catalog"]').exists()).toBe(false)
    continuePositive()
    await waitFor(wrapper, '[aria-label="验收结论：PASS"]')
    expect(wrapper.find('[aria-label="验收结论：PASS"]').exists()).toBe(true)
    wrapper.unmount()
  })

  it('keeps the Catalog owner visible while an invalid fixture is being verified', async () => {
    const wrapper = mount(App)
    await waitFor(wrapper, '[data-testid="status-gate"]')
    await wrapper.get('[data-testid="catalog-return"]').trigger('click')
    await waitFor(wrapper, '[data-testid="fixture-invalid"]')

    const fetchMock = vi.mocked(globalThis.fetch)
    const fetchImplementation = fetchMock.getMockImplementation()!
    let releaseInvalidFetch!: () => void
    const invalidFetchGate = new Promise<void>((resolve) => {
      releaseInvalidFetch = resolve
    })
    fetchMock.mockImplementation(async (input) => {
      const url = new URL(
        typeof input === 'string' ? input : input instanceof URL ? input.href : input.url,
        window.location.href,
      )
      if (url.pathname.includes('/fixtures/m2-invalid/')) await invalidFetchGate
      return fetchImplementation(input)
    })

    await wrapper.get('[data-testid="fixture-invalid"]').trigger('click')
    await flushPromises()

    const shellClasses = wrapper.get('.app-shell').classes()
    const mainBusy = wrapper.get('#main-content').attributes('aria-busy')
    const sourceBusy = wrapper.get('[data-testid="fixture-invalid"]').attributes('aria-busy')
    const renderedLegacyLoading = wrapper.find('[data-testid="loading-state"]').exists()
    const renderedLegacyCourt = wrapper.find('.state-court').exists()
    releaseInvalidFetch()
    await waitFor(wrapper, '[data-testid="error-state"]')

    expect(shellClasses).toContain('app-shell--catalog')
    expect(mainBusy).toBe('true')
    expect(sourceBusy).toBe('true')
    expect(renderedLegacyLoading).toBe(false)
    expect(renderedLegacyCourt).toBe(false)
    expect(wrapper.get('[data-testid="error-state"]').classes()).toContain('run-error-court')
    expect(wrapper.find('.state-court').exists()).toBe(false)
    wrapper.unmount()
  })

  it('closes the invalid bundle court from both the source toggle and stop seal', async () => {
    const host = document.createElement('div')
    document.body.append(host)
    const wrapper = mount(App, { attachTo: host })
    await waitFor(wrapper, '[data-testid="status-gate"]')
    await wrapper.get('[data-testid="catalog-return"]').trigger('click')
    await waitFor(wrapper, '[data-testid="fixture-invalid"]')
    const trigger = wrapper.get('[data-testid="fixture-invalid"]')

    await trigger.trigger('click')
    await waitFor(wrapper, '[data-testid="error-state"]')
    expect(trigger.attributes('aria-expanded')).toBe('true')

    await trigger.trigger('click')
    await flushPromises()
    expect(wrapper.find('[data-testid="error-state"]').exists()).toBe(false)
    expect(trigger.attributes('aria-expanded')).toBe('false')
    expect(window.location.search).toBe('?view=runs')

    await trigger.trigger('click')
    await waitFor(wrapper, '[data-testid="dismiss-invalid-state"]')
    await wrapper.get('[data-testid="dismiss-invalid-state"]').trigger('click')
    await flushPromises()
    expect(wrapper.find('[data-testid="error-state"]').exists()).toBe(false)
    expect(document.activeElement).toBe(trigger.element)
    expect(window.location.search).toBe('?view=runs')
    wrapper.unmount()
    host.remove()
  })

  it('keeps local-file privacy reselect distinct from a corrupt evidence package', async () => {
    window.history.replaceState({}, '', '/?fixture=batch')
    const wrapper = mount(App)
    await waitFor(wrapper, '[data-testid="error-state"]')

    const state = wrapper.get('[data-testid="error-state"]')
    expect(state.attributes('data-state-kind')).toBe('privacy')
    expect(state.text()).toContain('BATCH_RESELECT_REQUIRED')
    expect(state.text()).toContain('为保护隐私')
    expect(state.find('[data-testid="batch-analysis-view"]').exists()).toBe(false)
    wrapper.unmount()
  })

  it('imports a local Comparison only after manifest verification', async () => {
    const wrapper = mount(App)
    await waitFor(wrapper, '[data-testid="status-gate"]')
    await selectPublicView(wrapper, 'comparison')
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
    expect(wrapper.get('.app-shell').classes()).toContain('app-shell--comparison')
    expect(wrapper.get('.app-shell').classes()).not.toContain('app-shell--inner')

    await wrapper.get('[data-testid="comparison-open-differences"]').trigger('click')
    expect(window.location.search).toBe('?fixture=comparison&panel=differences')
    expect(wrapper.get('[data-testid="comparison-differences"]').text()).toContain('没有差异')
    await wrapper.get('[data-testid="comparison-panel-return-bottom"]').trigger('click')
    expect(window.location.search).toBe('?fixture=comparison')
    expect(wrapper.get('[data-testid="comparison-status"]').text()).toContain('MATCH')
    wrapper.unmount()
  })

  it('imports a local PairedAnalysis only after plan seal and manifest verification', async () => {
    const wrapper = mount(App)
    await waitFor(wrapper, '[data-testid="status-gate"]')
    await selectPublicView(wrapper, 'pairing')
    expect(wrapper.get('.app-shell').classes()).toContain('app-shell--pairing')
    expect(wrapper.get('.app-shell').classes()).not.toContain('app-shell--inner')
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
    expect(wrapper.get('.site-footer__seal').text()).toContain('验')

    await wrapper.get('[data-testid="pairing-open-sources"]').trigger('click')
    expect(window.location.search).toBe('?fixture=pairing&panel=sources')
    expect(wrapper.get('[data-testid="paired-sources"]').text()).toContain('unit-treatment')
    await wrapper.get('[data-testid="pairing-panel-return"]').trigger('click')
    expect(window.location.search).toBe('?fixture=pairing')
    expect(wrapper.get('[data-testid="paired-analysis-status"]').text()).toContain('SUPPORTED')
    await wrapper.get('.site-footer__seal').trigger('click')
    expect(window.location.search).toBe('?view=runs')
    wrapper.unmount()
  })

  it('keeps Pairing empty and reselect states inside the Pairing visual owner', async () => {
    const wrapper = mount(App)
    await waitFor(wrapper, '[data-testid="status-gate"]')
    await selectPublicView(wrapper, 'pairing')

    expect(wrapper.find('[data-testid="pairing-entry-state"]').exists()).toBe(true)
    expect(wrapper.get('[data-testid="pairing-empty"]').text()).toContain('四象待入册')
    expect(wrapper.find('.view-introduction').exists()).toBe(false)
    expect(wrapper.find('.state-court').exists()).toBe(false)
    expect(wrapper.find('.error-court').exists()).toBe(false)
    wrapper.unmount()

    window.history.replaceState({}, '', '/?fixture=pairing')
    const reloaded = mount(App)
    await waitFor(reloaded, '[data-testid="error-state"]')

    expect(reloaded.find('[data-testid="pairing-entry-state"]').exists()).toBe(true)
    expect(reloaded.get('[data-testid="error-state"]').text()).toContain('PAIRING_RESELECT_REQUIRED')
    expect(reloaded.find('.view-introduction').exists()).toBe(false)
    expect(reloaded.find('.state-court').exists()).toBe(false)
    expect(reloaded.find('.error-court').exists()).toBe(false)
    reloaded.unmount()
  })

  it('imports four explicit BatchAnalysis files and keeps local files ephemeral', async () => {
    const wrapper = mount(App)
    await waitFor(wrapper, '[data-testid="status-gate"]')
    await selectPublicView(wrapper, 'batch')
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
