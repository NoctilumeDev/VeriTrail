import { mount } from '@vue/test-utils'
import { nextTick } from 'vue'
import { describe, expect, it, vi } from 'vitest'
import BrowserEvidence from '../src/components/BrowserEvidence.vue'
import type { EvidenceDocument } from '../src/domain/types'

const evidence: EvidenceDocument = {
  schema_version: '0.1',
  evidence_type: 'browser.session',
  source: 'unit',
  captured_at: '2026-08-09T00:00:00Z',
  facts: {
    capture_complete: true,
    cleanup_complete: true,
    unexpected_console_error_count: 1,
    page_error_count: 0,
    unexpected_http_error_count: 1,
    viewport_runs: [
      {
        name: 'mobile',
        width: 390,
        height: 844,
        is_mobile: true,
        status: 'PASSED',
        horizontal_overflow_px: 0,
        step_count: 1,
        network_request_count: 1,
      },
    ],
    steps: [
      { step_id: 'open', action: 'goto', status: 'PASSED', viewport: 'mobile', elapsed_ms: 8 },
      {
        step_id: 'negative-check',
        action: 'expect',
        status: 'FAILED',
        viewport: 'mobile',
        elapsed_ms: 16,
        error: 'Synthetic assertion failure must remain visible.',
      },
    ],
    console: [{ level: 'error', text: 'synthetic failure', viewport: 'mobile' }],
    network: [
      {
        sequence: 1,
        method: 'GET',
        url: 'http://localhost:18765/missing.json',
        status: 404,
        viewport: 'mobile',
        resource_type: 'fetch',
        finished: true,
      },
    ],
    screenshots: [
      {
        path: 'screenshots/mobile-negative.png',
        name: 'negative-state',
        viewport: 'mobile',
        size: 2048,
        sha256: 'a'.repeat(64),
      },
    ],
  },
}

describe('BrowserEvidence', () => {
  it('keeps the overview finite and emits a full-page handoff', async () => {
    const summaryEvidence = structuredClone(evidence)
    summaryEvidence.facts.steps = Array.from({ length: 5 }, (_, index) => ({
      step_id: `step-${index + 1}`,
      action: 'expect',
      status: 'PASSED',
      viewport: 'mobile',
      elapsed_ms: index,
    }))
    summaryEvidence.facts.viewport_runs = Array.from({ length: 4 }, (_, index) => ({
      name: `viewport-${index + 1}`,
      width: 390 + index,
      height: 844,
      is_mobile: true,
      status: 'PASSED',
      horizontal_overflow_px: 0,
      step_count: 1,
      network_request_count: 1,
    }))
    const wrapper = mount(BrowserEvidence, {
      props: { evidence: summaryEvidence, imageUrls: {}, summary: true },
    })

    expect(wrapper.findAll('.timeline__entry')).toHaveLength(3)
    expect(wrapper.findAll('.viewport-chip')).toHaveLength(2)
    await wrapper.get('[data-open-run-panel="browser"]').trigger('click')
    expect(wrapper.emitted('showAll')).toHaveLength(1)
    wrapper.unmount()
  })

  it('exposes the evidence court with keyboard tabs and durable failure facts', async () => {
    const wrapper = mount(BrowserEvidence, {
      props: { evidence, imageUrls: { 'screenshots/mobile-negative.png': 'blob:unit-screenshot' } },
    })
    const tabs = wrapper.findAll('[role="tab"]')

    expect(wrapper.get('[data-testid="browser-summary"]').text()).toContain('浏览器采集摘要')
    expect(wrapper.get('[data-testid="browser-summary"]').text()).toContain('异常事实')
    expect(tabs).toHaveLength(4)
    expect(tabs.map((tab) => tab.attributes('tabindex'))).toEqual(['0', '-1', '-1', '-1'])
    await tabs[0]!.trigger('keydown', { key: 'ArrowRight' })
    await nextTick()
    expect(tabs.map((tab) => tab.attributes('tabindex'))).toEqual(['-1', '0', '-1', '-1'])
    expect(wrapper.get('[aria-labelledby="tab-console"] .log--error').text()).toContain('synthetic failure')
    await tabs[2]!.trigger('click')
    expect(wrapper.get('[aria-labelledby="tab-network"] .network-row--error').text()).toContain('404')
    await tabs[0]!.trigger('click')
    expect(wrapper.get('.timeline__entry--failed').text()).toContain('Synthetic assertion failure')
  })

  it('restores focus to the screenshot trigger after native dialog closure', async () => {
    const showModal = vi.fn()
    Object.defineProperty(HTMLDialogElement.prototype, 'showModal', {
      configurable: true,
      value: showModal,
    })
    const wrapper = mount(BrowserEvidence, {
      attachTo: document.body,
      props: { evidence, imageUrls: { 'screenshots/mobile-negative.png': 'blob:unit-screenshot' } },
    })
    const tabs = wrapper.findAll('[role="tab"]')

    await tabs[3]!.trigger('click')
    const trigger = wrapper.get('[data-testid="browser-screenshot-trigger"]')
    await trigger.trigger('click')
    expect(showModal).toHaveBeenCalledTimes(1)
    expect(wrapper.get('dialog').text()).toContain('negative-state')
    await wrapper.get('dialog').trigger('close')
    await nextTick()
    expect(document.activeElement).toBe(trigger.element)
    wrapper.unmount()
  })

  it('treats absent browser evidence as an explicit absence rather than a pass', () => {
    const wrapper = mount(BrowserEvidence, { props: { evidence: null, imageUrls: {} } })

    expect(wrapper.get('[data-testid="browser-empty"]').attributes('data-state-kind')).toBe('no-browser')
    expect(wrapper.get('[data-testid="browser-empty"]').text()).toContain('不等于浏览器检查通过')
    wrapper.unmount()
  })
})
