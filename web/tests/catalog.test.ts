import { flushPromises, mount } from '@vue/test-utils'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import App from '../src/App.vue'
import { CatalogLoadError, validateCatalog } from '../src/domain/catalog'
import type { CatalogResponse } from '../src/domain/types'
import { createBootstrapBundle, createMinimalBundle } from './support'

const catalogRunId = `cr_${'1'.repeat(24)}`
let catalogPlanSha = 'a'.repeat(64)

function catalogResponse(runCount = 1): CatalogResponse {
  return {
    schema_version: '0.1',
    catalog: {
      catalog_id: `cat_${'2'.repeat(24)}`,
      build_status: 'COMPLETED',
      read_only: true,
      run_count: runCount,
      issue_count: 0,
      duplicate_count: 0,
    },
    pagination: { page: 1, page_size: 50, total_items: runCount, total_pages: runCount ? 1 : 0 },
    runs: runCount
      ? [
          {
            catalog_run_id: catalogRunId,
            run_id: 'unit-run',
            created_at: '2026-08-09T00:00:00Z',
            execution_status: 'COMPLETED',
            verdict: 'PASS',
            plan: { id: 'unit-plan', version: 1, sha256: catalogPlanSha },
            bundle: {
              sha256: 'b'.repeat(64),
              file_count: 3,
              total_bytes: 2048,
              duplicate_count: 0,
              base_url: `/api/v1/runs/${catalogRunId}/bundle/`,
            },
          },
        ]
      : [],
    issues: [],
    issues_truncated: false,
  }
}

async function waitFor(wrapper: ReturnType<typeof mount>, selector: string) {
  for (let attempt = 0; attempt < 40; attempt += 1) {
    await flushPromises()
    if (wrapper.find(selector).exists()) return
    await new Promise((resolve) => setTimeout(resolve, 0))
  }
  throw new Error(`Timed out waiting for ${selector}`)
}

describe('Catalog API 0.1', () => {
  let bundle: Map<string, Blob>

  beforeEach(async () => {
    window.history.replaceState({}, '', '/?view=runs')
    bundle = await createMinimalBundle()
    catalogPlanSha = (JSON.parse(await bundle.get('report.json')!.text()) as {
      plan: { sha256: string }
    }).plan.sha256
  })

  afterEach(() => vi.restoreAllMocks())

  function installCatalogFetch(response: CatalogResponse, forcedBundleError?: string) {
    return vi.spyOn(globalThis, 'fetch').mockImplementation(async (input) => {
      const url = new URL(typeof input === 'string' ? input : input instanceof URL ? input.href : input.url, window.location.href)
      if (url.pathname === '/api/v1/catalog') {
        return {
          ok: true,
          status: 200,
          blob: async () => new Blob([JSON.stringify(response)]),
        } as Response
      }
      const catalogPrefix = `/api/v1/runs/${catalogRunId}/bundle/`
      if (url.pathname.startsWith(catalogPrefix)) {
        const path = url.pathname.slice(catalogPrefix.length)
        if (forcedBundleError && path === 'report.json') {
          return {
            ok: false,
            status: 409,
            blob: async () =>
              new Blob([
                JSON.stringify({
                  schema_version: '0.1',
                  error: { code: forcedBundleError, message: 'server message is not trusted' },
                }),
              ]),
          } as Response
        }
        const body = bundle.get(path)
        return {
          ok: Boolean(body),
          status: body ? 200 : 404,
          blob: async () => body ?? new Blob(['missing']),
        } as Response
      }
      if (url.pathname.includes('/fixtures/m2-positive/')) {
        const path = url.pathname.split('/fixtures/m2-positive/')[1]!
        const body = bundle.get(path)
        return {
          ok: Boolean(body),
          status: body ? 200 : 404,
          blob: async () => body ?? new Blob(['missing']),
        } as Response
      }
      return { ok: false, status: 404, blob: async () => new Blob(['missing']) } as Response
    })
  }

  it('validates the fixed same-origin bundle route', () => {
    expect(validateCatalog(catalogResponse()).runs[0]?.catalog_run_id).toBe(catalogRunId)
    const invalid = catalogResponse()
    invalid.runs[0]!.bundle.base_url = 'https://example.invalid/bundle/'
    expect(() => validateCatalog(invalid)).toThrowError(CatalogLoadError)
  })

  it('shows a valid empty Catalog without turning it into PENDING', async () => {
    installCatalogFetch(catalogResponse(0))
    const wrapper = mount(App)
    await waitFor(wrapper, '[data-testid="catalog-empty"]')
    expect(wrapper.get('[data-testid="catalog-empty"]').text()).toContain('目录有效，暂无 Run')
    expect(wrapper.get('[data-testid="catalog-empty"]').text()).toContain('不是 Run 的 PENDING')
    wrapper.unmount()
  })

  it('keeps Run identity, execution, verdict, and plan facts in a stable visible column order', async () => {
    installCatalogFetch(catalogResponse())
    const wrapper = mount(App)
    await waitFor(wrapper, '[data-testid="catalog-columns"]')

    expect(wrapper.get('[data-testid="catalog-columns"]').text()).toBe(
      'Run / 时间运行状态验收结论Plan / 目录事实',
    )
    const row = wrapper.get('[data-catalog-run-id]')
    expect(row.find('.catalog-run__identity').text()).toContain('unit-run')
    expect(row.find('.catalog-run__id-tooltip').text()).toBe('Run：unit-run · Plan：unit-plan · v1')
    expect(row.find('.catalog-run__execution').text()).toContain('COMPLETED')
    expect(row.find('.catalog-run__verdict').text()).toContain('PASS')
    expect(row.find('.catalog-run__facts').text()).toContain('unit-plan · v1')
    expect([...row.element.children].map((child) => child.className)).toEqual([
      'catalog-run__identity',
      'catalog-run__execution',
      'catalog-run__verdict',
      'catalog-run__facts',
    ])
    wrapper.unmount()
  })

  it('selects a Catalog Run, fully revalidates its Bundle, and returns focus', async () => {
    installCatalogFetch(catalogResponse())
    const host = document.createElement('div')
    document.body.append(host)
    const wrapper = mount(App, { attachTo: host })
    await waitFor(wrapper, '[data-catalog-run-id]')
    await wrapper.get('[data-catalog-run-id]').trigger('click')
    await waitFor(wrapper, '[data-testid="catalog-return"]')
    expect(document.activeElement?.id).toBe('run-detail-title')
    expect(wrapper.get('[data-testid="run-summary"]').text()).toContain('本地目录 · unit-run')
    expect(window.location.search).toBe(`?run=${catalogRunId}`)
    await wrapper.get('[data-testid="catalog-return"]').trigger('click')
    await flushPromises()
    expect(document.activeElement?.getAttribute('data-catalog-run-id')).toBe(catalogRunId)
    wrapper.unmount()
    host.remove()
  })

  it('keeps a direct Run URL on the detail surface while the Catalog is still loading', async () => {
    window.history.replaceState({}, '', `/?run=${catalogRunId}`)
    installCatalogFetch(catalogResponse())
    const fetchMock = vi.mocked(globalThis.fetch)
    const fetchImplementation = fetchMock.getMockImplementation()!
    let releaseCatalogFetch!: () => void
    const catalogFetchGate = new Promise<void>((resolve) => {
      releaseCatalogFetch = resolve
    })
    fetchMock.mockImplementation(async (input) => {
      const url = new URL(
        typeof input === 'string' ? input : input instanceof URL ? input.href : input.url,
        window.location.href,
      )
      if (url.pathname === '/api/v1/catalog') await catalogFetchGate
      return fetchImplementation(input)
    })

    const wrapper = mount(App)
    expect(wrapper.get('.app-shell').classes()).toContain('app-shell--run-detail')
    expect(wrapper.find('[data-testid="run-detail-loading"]').exists()).toBe(true)
    expect(wrapper.find('[data-testid="run-catalog"]').exists()).toBe(false)

    releaseCatalogFetch()
    await waitFor(wrapper, '[data-testid="status-gate"]')
    expect(wrapper.get('[data-testid="run-summary"]').text()).toContain('unit-run')
    wrapper.unmount()
  })

  it('enters the detail verification surface without retaining the Catalog ledger', async () => {
    installCatalogFetch(catalogResponse())
    const wrapper = mount(App)
    await waitFor(wrapper, '[data-catalog-run-id]')

    const fetchMock = vi.mocked(globalThis.fetch)
    const fetchImplementation = fetchMock.getMockImplementation()!
    let releaseBundleFetch!: () => void
    const bundleFetchGate = new Promise<void>((resolve) => {
      releaseBundleFetch = resolve
    })
    fetchMock.mockImplementation(async (input) => {
      const url = new URL(
        typeof input === 'string' ? input : input instanceof URL ? input.href : input.url,
        window.location.href,
      )
      if (url.pathname.startsWith(`/api/v1/runs/${catalogRunId}/bundle/`)) await bundleFetchGate
      return fetchImplementation(input)
    })

    await wrapper.get('[data-catalog-run-id]').trigger('click')
    await flushPromises()

    const shellClasses = wrapper.get('.app-shell').classes()
    const renderedDetailLoading = wrapper.find('[data-testid="run-detail-loading"]').exists()
    const renderedCatalog = wrapper.find('[data-testid="run-catalog"]').exists()
    const renderedLegacyLoading = wrapper.find('[data-testid="loading-state"]').exists()
    const renderedLegacyCourt = wrapper.find('.state-court').exists()
    releaseBundleFetch()
    await waitFor(wrapper, '[data-testid="catalog-return"]')

    expect(shellClasses).toContain('app-shell--run-detail')
    expect(renderedDetailLoading).toBe(true)
    expect(renderedCatalog).toBe(false)
    expect(renderedLegacyLoading).toBe(false)
    expect(renderedLegacyCourt).toBe(false)
    expect(wrapper.get('.app-shell').classes()).toContain('app-shell--run-detail')
    wrapper.unmount()
  })

  it('opens complete Run ledgers as page states instead of nested scroll regions', async () => {
    installCatalogFetch(catalogResponse())
    const wrapper = mount(App)
    await waitFor(wrapper, '[data-catalog-run-id]')
    await wrapper.get('[data-catalog-run-id]').trigger('click')
    await waitFor(wrapper, '[data-open-run-panel="assertions"]')

    await wrapper.get('[data-open-run-panel="assertions"]').trigger('click')
    await flushPromises()
    expect(window.location.search).toBe(`?run=${catalogRunId}&panel=assertions`)
    expect(wrapper.get('#run-detail-panel-title').text()).toBe('确定性断言')
    expect(wrapper.find('[data-testid="run-summary"]').exists()).toBe(false)
    expect(wrapper.get('[data-testid="run-panel-return-bottom"]').text()).toContain('返回 Run 详情')

    await wrapper.get('[data-testid="run-panel-return-bottom"]').trigger('click')
    await flushPromises()
    expect(window.location.search).toBe(`?run=${catalogRunId}`)
    expect(wrapper.get('[data-testid="run-summary"]').text()).toContain('unit-run')
    wrapper.unmount()
  })

  it('restores the URL-owned panel after a failed Catalog Run retry', async () => {
    window.history.replaceState({}, '', `/?run=${catalogRunId}&panel=assertions`)
    installCatalogFetch(catalogResponse())
    const fetchMock = vi.mocked(globalThis.fetch)
    const fetchImplementation = fetchMock.getMockImplementation()!
    let failReport = true
    fetchMock.mockImplementation(async (input) => {
      const url = new URL(
        typeof input === 'string' ? input : input instanceof URL ? input.href : input.url,
        window.location.href,
      )
      if (
        failReport &&
        url.pathname === `/api/v1/runs/${catalogRunId}/bundle/report.json`
      ) {
        return {
          ok: false,
          status: 409,
          blob: async () => new Blob([JSON.stringify({
            schema_version: '0.1',
            error: { code: 'BUNDLE_CHANGED', message: 'untrusted' },
          })]),
        } as Response
      }
      return fetchImplementation(input)
    })

    const wrapper = mount(App)
    await waitFor(wrapper, '[data-testid="error-state"]')
    expect(window.location.search).toBe(`?run=${catalogRunId}&panel=assertions`)

    failReport = false
    const retryButton = wrapper.get('[data-testid="retry-catalog-run"]')
    await retryButton.trigger('click')
    expect((retryButton.element as HTMLButtonElement).disabled).toBe(true)
    await retryButton.trigger('click')
    await waitFor(wrapper, '#run-detail-panel-title')
    expect(wrapper.get('#run-detail-panel-title').text()).toBe('确定性断言')
    expect(window.location.search).toBe(`?run=${catalogRunId}&panel=assertions`)
    wrapper.unmount()
  })

  it('keeps applicability expansion reversible and labels both states', async () => {
    installCatalogFetch(catalogResponse())
    const wrapper = mount(App)
    await waitFor(wrapper, '[data-catalog-run-id]')
    await wrapper.get('[data-catalog-run-id]').trigger('click')
    await waitFor(wrapper, 'details.applicability')

    const details = wrapper.get('details.applicability')
    expect(details.get('summary').text()).toBe('展开适用边界与资源预算')

    ;(details.element as HTMLDetailsElement).open = true
    await details.trigger('toggle')
    expect(details.get('summary').text()).toBe('收起适用边界与资源预算')

    ;(details.element as HTMLDetailsElement).open = false
    await details.trigger('toggle')
    expect(details.get('summary').text()).toBe('展开适用边界与资源预算')
    wrapper.unmount()
  })

  it('uses the footer seal as one consistent return-to-catalog action', async () => {
    installCatalogFetch(catalogResponse())
    const wrapper = mount(App)
    await waitFor(wrapper, '[data-catalog-run-id]')
    await wrapper.get('[data-catalog-run-id]').trigger('click')
    await waitFor(wrapper, '[data-testid="run-summary"]')

    await wrapper.get('[aria-label="返回本地 Run 目录"]').trigger('click')
    await flushPromises()
    expect(window.location.search).toBe('')
    expect(wrapper.find('[data-testid="run-catalog"]').exists()).toBe(true)
    expect(wrapper.find('[data-testid="run-summary"]').exists()).toBe(false)
    wrapper.unmount()
  })

  it('reads M10 runtime.bootstrap through the generic evidence ledger without re-adjudication', async () => {
    bundle = await createBootstrapBundle()
    const response = catalogResponse()
    response.runs[0]!.run_id = 'm10-workbench-readback'
    response.runs[0]!.plan = {
      id: 'm10-workbench-plan',
      version: 1,
      sha256: (JSON.parse(await bundle.get('report.json')!.text()) as {
        plan: { sha256: string }
      }).plan.sha256,
    }
    installCatalogFetch(response)
    const wrapper = mount(App)
    await waitFor(wrapper, '[data-catalog-run-id]')
    await wrapper.get('[data-catalog-run-id]').trigger('click')
    await waitFor(wrapper, '[data-testid="evidence-ledger"]')

    expect(wrapper.get('[data-testid="run-summary"]').text()).toContain(
      '本地目录 · m10-workbench-readback',
    )
    expect(wrapper.get('[data-testid="evidence-ledger"]').text()).toContain('runtime.bootstrap')
    expect(wrapper.get('[data-testid="assertion-list"]').text()).toContain(
      'bootstrap-cleanup-complete',
    )
    expect(wrapper.get('[data-testid="status-gate"]').text()).toContain('COMPLETED')
    expect(wrapper.get('[data-testid="status-gate"]').text()).toContain('PASS')
    expect(wrapper.get('[data-testid="integrity-status"]').text()).toContain('已核验')
    expect(wrapper.find('[data-testid="error-state"]').exists()).toBe(false)
    wrapper.unmount()
  })

  it('clears trusted details when a selected source Bundle changes', async () => {
    installCatalogFetch(catalogResponse())
    const wrapper = mount(App)
    await waitFor(wrapper, '[data-catalog-run-id]')
    const report = bundle.get('report.json')!
    bundle.set('report.json', new Blob([`${await report.text()} `]))
    await wrapper.get('[data-catalog-run-id]').trigger('click')
    await waitFor(wrapper, '[data-testid="error-state"]')
    expect(wrapper.find('[data-testid="status-gate"]').exists()).toBe(false)
    expect(wrapper.get('[data-testid="error-state"]').text()).toContain('没有据此改写 Run 的 Verdict')
    wrapper.unmount()
  })

  it('preserves the stable API error code without trusting its free-text message', async () => {
    installCatalogFetch(catalogResponse(), 'BUNDLE_CHANGED')
    const wrapper = mount(App)
    await waitFor(wrapper, '[data-catalog-run-id]')
    await wrapper.get('[data-catalog-run-id]').trigger('click')
    await waitFor(wrapper, '[data-testid="error-state"]')
    expect(wrapper.get('[data-testid="error-state"] code').text()).toBe('BUNDLE_CHANGED')
    expect(wrapper.get('[data-testid="error-state"]').text()).toContain('源 Bundle 已在索引后发生变化')
    expect(wrapper.get('[data-testid="error-state"]').text()).not.toContain('server message is not trusted')
    wrapper.unmount()
  })
})
