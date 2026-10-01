import {
  buildWorkbenchUrl,
  historyStateForRoute,
  parseWorkbenchRoute,
  type WorkbenchRouteSnapshot,
  type WorkbenchRouteTarget,
} from '../domain/workbenchRoute'

export interface WorkbenchHistoryWindow {
  readonly location: Pick<Location, 'href'>
  readonly scrollY: number
  readonly history: Pick<History, 'back' | 'pushState' | 'replaceState' | 'state'>
  addEventListener(type: 'popstate', listener: EventListener): void
  removeEventListener(type: 'popstate', listener: EventListener): void
}

export interface WorkbenchHistory {
  current(): WorkbenchRouteSnapshot
  savedScrollY(): number | null
  push(target: WorkbenchRouteTarget, returnScrollY?: number): void
  returnTo(target: WorkbenchRouteTarget): 'history' | 'fallback'
  subscribe(listener: () => void): () => void
}

const RETURN_URL_STATE_KEY = '__veritrail_return_url'
const SCROLL_Y_STATE_KEY = '__veritrail_scroll_y'

function recordState(state: unknown): Record<string, unknown> {
  return state !== null && typeof state === 'object'
    ? { ...(state as Record<string, unknown>) }
    : {}
}

export function createWorkbenchHistory(
  browserWindow: WorkbenchHistoryWindow = window,
): WorkbenchHistory {
  return {
    current() {
      return parseWorkbenchRoute(browserWindow.location.href)
    },
    savedScrollY() {
      const value = browserWindow.history.state?.[SCROLL_Y_STATE_KEY]
      return typeof value === 'number' && Number.isFinite(value) && value >= 0
        ? value
        : null
    },
    push(target, returnScrollY = browserWindow.scrollY) {
      const url = buildWorkbenchUrl(browserWindow.location.href, target)
      browserWindow.history.replaceState(
        {
          ...recordState(browserWindow.history.state),
          [SCROLL_Y_STATE_KEY]: returnScrollY,
        },
        '',
        browserWindow.location.href,
      )
      browserWindow.history.pushState(
        {
          ...historyStateForRoute(target),
          [RETURN_URL_STATE_KEY]: browserWindow.location.href,
        },
        '',
        url,
      )
    },
    returnTo(target) {
      const url = buildWorkbenchUrl(browserWindow.location.href, target)
      const returnUrl = browserWindow.history.state?.[RETURN_URL_STATE_KEY]
      if (
        typeof returnUrl === 'string'
        && new URL(returnUrl, browserWindow.location.href).href === url.href
      ) {
        browserWindow.history.back()
        return 'history'
      }
      browserWindow.history.replaceState(historyStateForRoute(target), '', url)
      return 'fallback'
    },
    subscribe(listener) {
      const handlePopState: EventListener = () => listener()
      browserWindow.addEventListener('popstate', handlePopState)
      return () => browserWindow.removeEventListener('popstate', handlePopState)
    },
  }
}
