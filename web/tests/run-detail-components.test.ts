import { mount } from '@vue/test-utils'
import { describe, expect, it } from 'vitest'
import RunBoundary from '../src/components/RunBoundary.vue'
import RunOverview from '../src/components/RunOverview.vue'
import type { VerdictReport } from '../src/domain/types'
import { minimalReport } from './support'

describe('Run detail disclosures', () => {
  it('keeps long overview fields reversible instead of permanently clipping them', async () => {
    const report = minimalReport({
      baseline: { id: 'a-deliberately-long-baseline-identifier-for-disclosure', status: 'VALID' },
    }) as VerdictReport
    const wrapper = mount(RunOverview, { props: { report } })
    const trigger = wrapper.get('.overview-expand')

    expect(trigger.attributes('aria-expanded')).toBe('false')
    await trigger.trigger('click')
    expect(trigger.attributes('aria-expanded')).toBe('true')
    expect(wrapper.get('#overview-facts').classes()).toContain('overview-grid--expanded')
    await trigger.trigger('click')
    expect(trigger.attributes('aria-expanded')).toBe('false')
  })

  it('previews bounded boundary rows and restores the complete list on demand', async () => {
    const report = minimalReport({
      reproduction_steps: ['step 1', 'step 2', 'step 3', 'step 4', 'step 5'],
    }) as VerdictReport
    const wrapper = mount(RunBoundary, { props: { report } })
    const trigger = wrapper.get('.boundary-show-all')

    expect(wrapper.findAll('#boundary-ledger ol').at(0)?.findAll('li')).toHaveLength(3)
    expect(trigger.attributes('aria-expanded')).toBe('false')
    await trigger.trigger('click')
    expect(wrapper.findAll('#boundary-ledger ol').at(0)?.findAll('li')).toHaveLength(5)
    expect(trigger.text()).toContain('收起')
    await trigger.trigger('click')
    expect(wrapper.findAll('#boundary-ledger ol').at(0)?.findAll('li')).toHaveLength(3)
  })
})
