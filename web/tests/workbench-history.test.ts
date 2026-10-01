import { describe, expect, it, vi } from 'vitest'
import {
  createWorkbenchHistory,
  type WorkbenchHistoryWindow,
} from '../src/navigation/workbenchHistory'

class FakeHistoryWindow implements WorkbenchHistoryWindow {
  readonly location: Pick<Location, 'href'>
  scrollY = 0
  readonly pushes: Array<{ state: unknown; url: string }> = []
  readonly replacements: Array<{ state: unknown; url: string }> = []
  readonly history: Pick<History, 'back' | 'pushState' | 'replaceState' | 'state'>
  backCalls = 0
  private readonly popStateListeners = new Set<EventListener>()

  constructor(href: string) {
    this.location = { href }
    let state: unknown = null
    this.history = {
      get state() {
        return state
      },
      pushState: (nextState: unknown, _unused: string, url?: string | URL | null) => {
        const nextUrl = url === undefined || url === null
          ? new URL(this.location.href)
          : new URL(url.toString(), this.location.href)
        this.location.href = nextUrl.href
        state = nextState
        this.pushes.push({ state: nextState, url: nextUrl.href })
      },
      replaceState: (nextState: unknown, _unused: string, url?: string | URL | null) => {
        const nextUrl = url === undefined || url === null
          ? new URL(this.location.href)
          : new URL(url.toString(), this.location.href)
        this.location.href = nextUrl.href
        state = nextState
        this.replacements.push({ state: nextState, url: nextUrl.href })
      },
      back: () => {
        this.backCalls += 1
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
    browserWindow.scrollY = 384
    const history = createWorkbenchHistory(browserWindow)

    history.push({ kind: 'comparison', sample: 'drift', panel: 'differences' })

    expect(browserWindow.pushes).toEqual([
      {
        state: {
          fixture: 'comparison',
          sample: 'drift',
          panel: 'differences',
          __veritrail_return_url: 'https://example.test/workbench?keep=1&fixture=negative#evidence',
        },
        url: 'https://example.test/workbench?keep=1&fixture=comparison&sample=drift&panel=differences#evidence',
      },
    ])
    expect(browserWindow.replacements).toEqual([
      {
        state: { __veritrail_scroll_y: 384 },
        url: 'https://example.test/workbench?keep=1&fixture=negative#evidence',
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

  it('returns through browser history when the requested parent is the recorded source', () => {
    const browserWindow = new FakeHistoryWindow(
      'https://example.test/workbench?keep=1',
    )
    const history = createWorkbenchHistory(browserWindow)

    history.push({ kind: 'run', catalogRunId: 'run-1' })
    expect(history.returnTo({ kind: 'catalog' })).toBe('history')
    expect(browserWindow.backCalls).toBe(1)
    expect(browserWindow.replacements).toHaveLength(1)
  })

  it('reads only a finite non-negative scroll checkpoint from history state', () => {
    const browserWindow = new FakeHistoryWindow('https://example.test/workbench')
    const history = createWorkbenchHistory(browserWindow)

    expect(history.savedScrollY()).toBeNull()
    browserWindow.history.replaceState({ __veritrail_scroll_y: 275 }, '', browserWindow.location.href)
    expect(history.savedScrollY()).toBe(275)
    browserWindow.history.replaceState({ __veritrail_scroll_y: -1 }, '', browserWindow.location.href)
    expect(history.savedScrollY()).toBeNull()
  })

  it('stores an explicitly captured pre-transition scroll checkpoint', () => {
    const browserWindow = new FakeHistoryWindow('https://example.test/workbench?fixture=pairing')
    browserWindow.scrollY = 900
    const history = createWorkbenchHistory(browserWindow)

    history.push({ kind: 'pairing', panel: 'sources' }, 420)

    expect(browserWindow.replacements[0]?.state).toEqual({ __veritrail_scroll_y: 420 })
  })

  it('replaces a direct deep link with the safe fallback instead of leaving the app', () => {
    const browserWindow = new FakeHistoryWindow(
      'https://example.test/workbench?run=run-1',
    )
    const history = createWorkbenchHistory(browserWindow)

    expect(history.returnTo({ kind: 'catalog' })).toBe('fallback')
    expect(browserWindow.backCalls).toBe(0)
    expect(browserWindow.replacements).toEqual([
      {
        state: {},
        url: 'https://example.test/workbench',
      },
    ])
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
