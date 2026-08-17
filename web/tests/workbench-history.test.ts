import { describe, expect, it, vi } from 'vitest'
import {
  createWorkbenchHistory,
  type WorkbenchHistoryWindow,
} from '../src/navigation/workbenchHistory'

class FakeHistoryWindow implements WorkbenchHistoryWindow {
  readonly location: Pick<Location, 'href'>
  readonly pushes: Array<{ state: unknown; url: string }> = []
  readonly history: Pick<History, 'pushState'>
  private readonly popStateListeners = new Set<EventListener>()

  constructor(href: string) {
    this.location = { href }
    this.history = {
      pushState: (state: unknown, _unused: string, url?: string | URL | null) => {
        const nextUrl = url === undefined || url === null
          ? new URL(this.location.href)
          : new URL(url.toString(), this.location.href)
        this.location.href = nextUrl.href
        this.pushes.push({ state, url: nextUrl.href })
      },
    }
  }

  addEventListener(type: 'popstate', listener: EventListener): void {
    if (type === 'popstate') this.popStateListeners.add(listener)
  }

  removeEventListener(type: 'popstate', listener: EventListener): void {
    if (type === 'popstate') this.popStateListeners.delete(listener)
  }

  emitPopState(): void {
    const event = new PopStateEvent('popstate')
    for (const listener of this.popStateListeners) listener(event)
  }

  get popStateListenerCount(): number {
    return this.popStateListeners.size
  }
}

describe('createWorkbenchHistory', () => {
  it('reads the current route from the injected window', () => {
    const browserWindow = new FakeHistoryWindow(
      'https://example.test/workbench?fixture=pairing&sample=supported&panel=sources',
    )
    const history = createWorkbenchHistory(browserWindow)

    expect(history.current()).toMatchObject({
      kind: 'pairing',
      publicView: 'pairing',
      pairingPanel: 'sources',
      pairingSample: 'supported',
    })
  })

  it('pushes matching history state and URL, then reads the new route', () => {
    const browserWindow = new FakeHistoryWindow(
      'https://example.test/workbench?keep=1&fixture=negative#evidence',
    )
    const history = createWorkbenchHistory(browserWindow)

    history.push({ kind: 'comparison', sample: 'drift', panel: 'differences' })

    expect(browserWindow.pushes).toEqual([
      {
        state: {
          fixture: 'comparison',
          sample: 'drift',
          panel: 'differences',
        },
        url: 'https://example.test/workbench?keep=1&fixture=comparison&sample=drift&panel=differences#evidence',
      },
    ])
    expect(history.current()).toMatchObject({
      kind: 'comparison',
      publicView: 'comparison',
      comparisonPanel: 'differences',
      comparisonSample: 'drift',
    })
  })

  it('subscribes and unsubscribes from injected popstate events', () => {
    const browserWindow = new FakeHistoryWindow('https://example.test/workbench')
    const history = createWorkbenchHistory(browserWindow)
    const listener = vi.fn()

    const unsubscribe = history.subscribe(listener)
    expect(browserWindow.popStateListenerCount).toBe(1)

    browserWindow.emitPopState()
    expect(listener).toHaveBeenCalledTimes(1)

    unsubscribe()
    expect(browserWindow.popStateListenerCount).toBe(0)
    browserWindow.emitPopState()
    expect(listener).toHaveBeenCalledTimes(1)
  })

  it('does not synthesize popstate when pushing a route', () => {
    const browserWindow = new FakeHistoryWindow('https://example.test/workbench')
    const history = createWorkbenchHistory(browserWindow)
    const listener = vi.fn()
    const unsubscribe = history.subscribe(listener)

    history.push({ kind: 'view', view: 'batch' })

    expect(listener).not.toHaveBeenCalled()
    expect(browserWindow.pushes).toHaveLength(1)
    expect(history.current()).toMatchObject({
      kind: 'analysis-view',
      publicView: 'batch',
    })

    browserWindow.emitPopState()
    expect(listener).toHaveBeenCalledTimes(1)
    unsubscribe()
  })
})
