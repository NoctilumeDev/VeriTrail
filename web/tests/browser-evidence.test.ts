import { mount } from '@vue/test-utils'
import { describe, expect, it } from 'vitest'
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
    screenshots: [],
  },
}

describe('BrowserEvidence', () => {
  it('exposes tabs with keyboard semantics and preserves failure facts', async () => {
    const wrapper = mount(BrowserEvidence, { props: { evidence, imageUrls: {} } })
    const tabs = wrapper.findAll('[role="tab"]')

    expect(tabs).toHaveLength(4)
    await tabs[0]!.trigger('keydown', { key: 'ArrowRight' })
    expect(wrapper.get('[aria-labelledby="tab-console"]').text()).toContain('synthetic failure')
    await tabs[2]!.trigger('click')
    expect(wrapper.get('[aria-labelledby="tab-network"]').text()).toContain('404')
  })
})
