import { mount } from '@vue/test-utils'
import { describe, expect, it } from 'vitest'
import CrossAxisNavigation from '../src/components/CrossAxisNavigation.vue'

describe('CrossAxisNavigation', () => {
  it('keeps direction targets out of the focus order until the center expands them', async () => {
    const wrapper = mount(CrossAxisNavigation, {
      props: { currentView: 'runs', expanded: false },
      attachTo: document.body,
    })

    const center = wrapper.get('[data-testid="cross-axis-toggle"]')
    expect(center.attributes('aria-expanded')).toBe('false')
    expect(wrapper.find('[data-testid="cross-axis-runs"]').exists()).toBe(false)

    await center.trigger('click')
    expect(wrapper.emitted('toggle')).toEqual([[true]])

    await wrapper.setProps({ expanded: true })
    const order = wrapper.findAll('button').map((button) => button.attributes('data-testid'))
    expect(order).toEqual([
      'cross-axis-toggle',
      'cross-axis-runs',
      'cross-axis-batch',
      'cross-axis-comparison',
      'cross-axis-pairing',
    ])
    wrapper.unmount()
  })

  it('moves arrow focus by geometry and returns Esc focus to the center', async () => {
    const wrapper = mount(CrossAxisNavigation, {
      props: { currentView: 'comparison', expanded: true },
      attachTo: document.body,
    })

    const north = wrapper.get('[data-testid="cross-axis-runs"]')
    await north.trigger('keydown', { key: 'ArrowRight' })
    expect(document.activeElement).toBe(wrapper.get('[data-testid="cross-axis-batch"]').element)

    const batch = wrapper.get('[data-testid="cross-axis-batch"]')
    await batch.trigger('keydown', { key: 'Escape' })
    expect(wrapper.emitted('toggle')).toContainEqual([false])
    await Promise.resolve()
    expect(document.activeElement).toBe(wrapper.get('[data-testid="cross-axis-toggle"]').element)
    wrapper.unmount()
  })

  it('emits the selected fixed public view without creating another state', async () => {
    const wrapper = mount(CrossAxisNavigation, {
      props: { currentView: 'runs', expanded: true },
    })

    await wrapper.get('[data-testid="cross-axis-pairing"]').trigger('click')
    expect(wrapper.emitted('select')).toEqual([['pairing']])
    wrapper.unmount()
  })
})
