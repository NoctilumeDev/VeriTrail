import {
  buildWorkbenchUrl,
  historyStateForRoute,
  parseWorkbenchRoute,
  type WorkbenchRouteSnapshot,
  type WorkbenchRouteTarget,
} from '../domain/workbenchRoute'

export interface WorkbenchHistoryWindow {
  readonly location: Pick<Location, 'href'>
  readonly history: Pick<History, 'pushState'>
  addEventListener(type: 'popstate', listener: EventListener): void
  removeEventListener(type: 'popstate', listener: EventListener): void
}

export interface WorkbenchHistory {
  current(): WorkbenchRouteSnapshot
  push(target: WorkbenchRouteTarget): void
  subscribe(listener: () => void): () => void
}

export function createWorkbenchHistory(
  browserWindow: WorkbenchHistoryWindow = window,
): WorkbenchHistory {
  return {
    current() {
      return parseWorkbenchRoute(browserWindow.location.href)
    },
    push(target) {
      const url = buildWorkbenchUrl(browserWindow.location.href, target)
      browserWindow.history.pushState(historyStateForRoute(target), '', url)
    },
    subscribe(listener) {
      const handlePopState: EventListener = () => listener()
      browserWindow.addEventListener('popstate', handlePopState)
      return () => browserWindow.removeEventListener('popstate', handlePopState)
    },
  }
}
