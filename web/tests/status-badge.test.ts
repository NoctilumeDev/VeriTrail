import { mount } from '@vue/test-utils'
import { describe, expect, it } from 'vitest'
import StatusBadge from '../src/components/StatusBadge.vue'
import type { ExecutionStatus, Verdict } from '../src/domain/types'

describe('StatusBadge', () => {
  it.each<ExecutionStatus>(['PLANNED', 'RUNNING', 'COMPLETED', 'ABORTED', 'ERROR'])(
    'gives ExecutionStatus %s a non-colour label and symbol',
    (value) => {
      const wrapper = mount(StatusBadge, { props: { dimension: 'execution', value } })

      expect(wrapper.attributes('aria-label')).toBe(`运行状态：${value}`)
      expect(wrapper.get('.status-badge__icon').text()).not.toBe('')
      expect(wrapper.text()).toContain(value)
    },
  )

  it.each<Verdict>(['PASS', 'FAIL', 'INCONCLUSIVE', 'PENDING'])(
    'gives Verdict %s a separate non-colour label and symbol',
    (value) => {
      const wrapper = mount(StatusBadge, { props: { dimension: 'verdict', value } })

      expect(wrapper.attributes('aria-label')).toBe(`验收结论：${value}`)
      expect(wrapper.get('.status-badge__icon').text()).not.toBe('')
      expect(wrapper.text()).toContain(value)
    },
  )
})
