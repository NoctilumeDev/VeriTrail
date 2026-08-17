export class SameOriginFixtureError extends Error {
  constructor(message: string) {
    super(message)
    this.name = 'SameOriginFixtureError'
  }
}

export async function fetchSameOriginFixture(
  basePath: string,
  fileNames: readonly string[],
): Promise<Map<string, Blob>> {
  const baseUrl = new URL(basePath.endsWith('/') ? basePath : `${basePath}/`, window.location.href)
  if (baseUrl.origin !== window.location.origin) {
    throw new SameOriginFixtureError('审阅夹具必须来自当前工作台。')
  }

  const entries = await Promise.all(fileNames.map(async (fileName) => {
    const fileUrl = new URL(fileName, baseUrl)
    if (fileUrl.origin !== baseUrl.origin || !fileUrl.pathname.startsWith(baseUrl.pathname)) {
      throw new SameOriginFixtureError('审阅夹具文件路径越过了固定目录。')
    }
    const response = await fetch(fileUrl, { credentials: 'same-origin' })
    if (!response.ok) {
      throw new SameOriginFixtureError(`审阅夹具文件读取失败：${fileName}`)
    }
    return [fileName, await response.blob()] as const
  }))

  return new Map(entries)
}
