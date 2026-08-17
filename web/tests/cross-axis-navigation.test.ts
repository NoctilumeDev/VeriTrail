import { mount } from '@vue/test-utils'
import { describe, expect, it } from 'vitest'
import CrossAxisNavigation from '../src/components/CrossAxisNavigation.vue'

describe('CrossAxisNavigation', () => {
  it('keeps all four fixed public views directly reachable in document order', () => {
    const wrapper = mount(CrossAxisNavigation, {
      props: { currentView: 'runs' },
      attachTo: document.body,
    })

    const order = wrapper.findAll('button').map((button) => button.attributes('data-testid'))
    expect(order).toEqual([
      'cross-axis-pairing',
      'cross-axis-runs',
      'cross-axis-batch',
      'cross-axis-comparison',
    ])
    expect(wrapper.get('[data-testid="cross-axis-runs"]').attributes('aria-current')).toBe('page')
    wrapper.unmount()
  })

  it('moves arrow focus by the fixed visual order and supports Home and End', async () => {
    const wrapper = mount(CrossAxisNavigation, {
      props: { currentView: 'comparison' },
      attachTo: document.body,
    })

    const north = wrapper.get('[data-testid="cross-axis-runs"]')
    await north.trigger('keydown', { key: 'ArrowRight' })
    expect(document.activeElement).toBe(wrapper.get('[data-testid="cross-axis-batch"]').element)

    const batch = wrapper.get('[data-testid="cross-axis-batch"]')
    await batch.trigger('keydown', { key: 'End' })
    expect(document.activeElement).toBe(wrapper.get('[data-testid="cross-axis-comparison"]').element)

    const comparison = wrapper.get('[data-testid="cross-axis-comparison"]')
    await comparison.trigger('keydown', { key: 'Home' })
    expect(document.activeElement).toBe(wrapper.get('[data-testid="cross-axis-pairing"]').element)
    wrapper.unmount()
  })

  it('emits the selected fixed public view without creating another state', async () => {
    const wrapper = mount(CrossAxisNavigation, {
      props: { currentView: 'runs' },
    })

    await wrapper.get('[data-testid="cross-axis-pairing"]').trigger('click')
    expect(wrapper.emitted('select')).toEqual([['pairing']])
    wrapper.unmount()
  })
})
