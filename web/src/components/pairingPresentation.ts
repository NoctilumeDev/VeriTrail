import type { PairingRole } from '../domain/types'

export const PAIRING_ROLES: PairingRole[] = [
  'BASELINE',
  'TREATMENT',
  'RESTORED_BASELINE',
  'NEGATIVE_CONTROL',
]

export const PAIRING_ROLE_META: Record<PairingRole, { chinese: string; english: string }> = {
  BASELINE: { chinese: '基线', english: 'Baseline' },
  TREATMENT: { chinese: '处理', english: 'Treatment' },
  RESTORED_BASELINE: { chinese: '复归基线', english: 'Restored baseline' },
  NEGATIVE_CONTROL: { chinese: '负控', english: 'Negative control' },
}

export function pairingValue(value: unknown): string {
  if (typeof value === 'string') return value
  return JSON.stringify(value)
}

export function pairingShortHash(value: string): string {
  return `${value.slice(0, 12)}…${value.slice(-8)}`
}

export function pairingDisplayDate(value: string): string {
  const date = new Date(value)
  return Number.isNaN(date.valueOf())
    ? value
    : date.toLocaleString('zh-CN', { hour12: false, timeZone: 'Asia/Shanghai' })
}
