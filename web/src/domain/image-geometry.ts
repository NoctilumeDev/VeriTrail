export const MAX_IMAGE_WIDTH = 8192
export const MAX_IMAGE_HEIGHT = 8192
export const MAX_IMAGE_PIXELS = 16_777_216
export const MAX_IMAGE_DECODED_BYTES = 64 * 1024 * 1024

const PNG_SIGNATURE = [137, 80, 78, 71, 13, 10, 26, 10]
const PNG_BIT_DEPTHS = new Map<number, Set<number>>([
  [0, new Set([1, 2, 4, 8, 16])],
  [2, new Set([8, 16])],
  [3, new Set([1, 2, 4, 8])],
  [4, new Set([8, 16])],
  [6, new Set([8, 16])],
])
const JPEG_SOF_MARKERS = new Set([
  0xc0, 0xc1, 0xc2, 0xc3, 0xc5, 0xc6, 0xc7, 0xc9, 0xca, 0xcb, 0xcd, 0xce, 0xcf,
])
const CRC32_TABLE = (() => {
  const table = new Uint32Array(256)
  for (let index = 0; index < table.length; index += 1) {
    let value = index
    for (let bit = 0; bit < 8; bit += 1) {
      value = (value >>> 1) ^ (value & 1 ? 0xedb88320 : 0)
    }
    table[index] = value >>> 0
  }
  return table
})()

export type ImageGeometryErrorCode = 'INVALID_IMAGE' | 'IMAGE_GEOMETRY_LIMIT'

export class ImageGeometryError extends Error {
  readonly code: ImageGeometryErrorCode

  constructor(code: ImageGeometryErrorCode, message: string) {
    super(message)
    this.name = 'ImageGeometryError'
    this.code = code
  }
}

export interface ImageGeometry {
  width: number
  height: number
  pixels: number
  decodedBytes: number
}

function invalid(message: string): never {
  throw new ImageGeometryError('INVALID_IMAGE', message)
}

function readU16(bytes: Uint8Array, offset: number): number {
  return bytes[offset]! * 0x100 + bytes[offset + 1]!
}

function readU32(bytes: Uint8Array, offset: number): number {
  return (
    bytes[offset]! * 0x1000000 +
    bytes[offset + 1]! * 0x10000 +
    bytes[offset + 2]! * 0x100 +
    bytes[offset + 3]!
  )
}

function boundedGeometry(width: number, height: number): ImageGeometry {
  if (width <= 0 || height <= 0) invalid('图片宽高必须为正数。')
  if (width > MAX_IMAGE_WIDTH || height > MAX_IMAGE_HEIGHT) {
    throw new ImageGeometryError(
      'IMAGE_GEOMETRY_LIMIT',
      `图片宽高超过 ${MAX_IMAGE_WIDTH}×${MAX_IMAGE_HEIGHT} 的固定上限。`,
    )
  }
  const pixels = width * height
  const decodedBytes = pixels * 4
  if (pixels > MAX_IMAGE_PIXELS || decodedBytes > MAX_IMAGE_DECODED_BYTES) {
    throw new ImageGeometryError(
      'IMAGE_GEOMETRY_LIMIT',
      '图片总像素或预计解码内存超过固定上限。',
    )
  }
  return { width, height, pixels, decodedBytes }
}

function crc32(bytes: Uint8Array, start: number, end: number): number {
  let crc = 0xffffffff
  for (let index = start; index < end; index += 1) {
    crc = (crc >>> 8) ^ CRC32_TABLE[(crc ^ bytes[index]!) & 0xff]!
  }
  return (crc ^ 0xffffffff) >>> 0
}

function parsePng(bytes: Uint8Array): ImageGeometry {
  if (
    bytes.length < PNG_SIGNATURE.length ||
    PNG_SIGNATURE.some((value, index) => bytes[index] !== value)
  ) {
    invalid('PNG 签名无效。')
  }

  let offset = PNG_SIGNATURE.length
  let geometry: ImageGeometry | undefined
  let sawIdat = false
  let sawIend = false
  let chunkIndex = 0
  while (offset < bytes.length) {
    if (bytes.length - offset < 12) invalid('PNG 数据块头被截断。')
    const length = readU32(bytes, offset)
    const typeStart = offset + 4
    const payloadStart = offset + 8
    const payloadEnd = payloadStart + length
    const chunkEnd = payloadEnd + 4
    if (chunkEnd > bytes.length) invalid('PNG 数据块负载被截断。')
    const typeBytes = bytes.subarray(typeStart, payloadStart)
    if (
      typeBytes.length !== 4 ||
      [...typeBytes].some((value) => !((value >= 65 && value <= 90) || (value >= 97 && value <= 122)))
    ) {
      invalid('PNG 数据块类型无效。')
    }
    const type = String.fromCharCode(...typeBytes)
    if (crc32(bytes, typeStart, payloadEnd) !== readU32(bytes, payloadEnd)) {
      invalid('PNG 数据块 CRC 无效。')
    }

    if (chunkIndex === 0) {
      if (type !== 'IHDR' || length !== 13) invalid('PNG 必须以 13 字节 IHDR 开始。')
      const width = readU32(bytes, payloadStart)
      const height = readU32(bytes, payloadStart + 4)
      const bitDepth = bytes[payloadStart + 8]!
      const colorType = bytes[payloadStart + 9]!
      const compression = bytes[payloadStart + 10]!
      const filtering = bytes[payloadStart + 11]!
      const interlace = bytes[payloadStart + 12]!
      if (!PNG_BIT_DEPTHS.get(colorType)?.has(bitDepth)) {
        invalid('PNG IHDR 位深或颜色类型无效。')
      }
      if (compression !== 0 || filtering !== 0 || (interlace !== 0 && interlace !== 1)) {
        invalid('PNG IHDR 压缩、过滤或隔行参数无效。')
      }
      geometry = boundedGeometry(width, height)
    } else if (type === 'IHDR') {
      invalid('PNG 包含重复 IHDR。')
    }

    if (type === 'IDAT') sawIdat = true
    if (type === 'IEND') {
      if (length !== 0 || chunkEnd !== bytes.length) invalid('PNG IEND 无效或不是末块。')
      sawIend = true
      break
    }
    offset = chunkEnd
    chunkIndex += 1
  }
  if (!geometry || !sawIdat || !sawIend) invalid('PNG 缺少 IHDR、IDAT 或 IEND。')
  return geometry
}

function parseJpeg(bytes: Uint8Array): ImageGeometry {
  if (bytes.length < 4 || bytes[0] !== 0xff || bytes[1] !== 0xd8) {
    invalid('JPEG SOI 标记无效。')
  }

  let offset = 2
  let geometry: ImageGeometry | undefined
  let inScan = false
  while (offset < bytes.length) {
    if (inScan) {
      const markerStart = bytes.indexOf(0xff, offset)
      if (markerStart < 0 || markerStart + 1 >= bytes.length) invalid('JPEG 扫描流被截断。')
      const marker = bytes[markerStart + 1]!
      if (marker === 0x00) {
        offset = markerStart + 2
        continue
      }
      if (marker === 0xff) {
        offset = markerStart + 1
        continue
      }
      if (marker >= 0xd0 && marker <= 0xd7) {
        offset = markerStart + 2
        continue
      }
      offset = markerStart
      inScan = false
      continue
    }

    if (bytes[offset] !== 0xff) invalid('JPEG 标记前缀无效。')
    while (offset < bytes.length && bytes[offset] === 0xff) offset += 1
    if (offset >= bytes.length) invalid('JPEG 标记被截断。')
    const marker = bytes[offset]!
    offset += 1
    if (marker === 0x00) invalid('JPEG 扫描外出现转义字节。')
    if (marker === 0xd9) {
      if (!geometry || offset !== bytes.length) invalid('JPEG EOI 缺少元数据或不是末标记。')
      return geometry
    }
    if (marker === 0xd8) invalid('JPEG 包含意外 SOI。')
    if (marker === 0x01 || (marker >= 0xd0 && marker <= 0xd7)) continue
    if (bytes.length - offset < 2) invalid('JPEG 段长度被截断。')
    const segmentLength = readU16(bytes, offset)
    if (segmentLength < 2 || offset + segmentLength > bytes.length) {
      invalid('JPEG 段无效或被截断。')
    }
    const payloadStart = offset + 2
    const payloadEnd = offset + segmentLength

    if (JPEG_SOF_MARKERS.has(marker)) {
      if (segmentLength < 8) invalid('JPEG SOF 段过短。')
      const precision = bytes[payloadStart]!
      const height = readU16(bytes, payloadStart + 1)
      const width = readU16(bytes, payloadStart + 3)
      const components = bytes[payloadStart + 5]!
      if ((precision !== 8 && precision !== 12) || components === 0) {
        invalid('JPEG SOF 精度或分量数无效。')
      }
      if (segmentLength !== 8 + 3 * components) invalid('JPEG SOF 分量元数据无效。')
      const nextGeometry = boundedGeometry(width, height)
      if (
        geometry &&
        (geometry.width !== nextGeometry.width || geometry.height !== nextGeometry.height)
      ) {
        invalid('JPEG 包含冲突的 SOF 宽高。')
      }
      geometry = nextGeometry
    }

    offset = payloadEnd
    if (marker === 0xda) {
      if (!geometry) invalid('JPEG 在 SOF 宽高之前开始扫描。')
      inScan = true
    }
  }
  return invalid('JPEG 缺少最终 EOI。')
}

export function parseImageGeometry(bytes: Uint8Array, mediaType: string): ImageGeometry {
  if (mediaType === 'image/png') return parsePng(bytes)
  if (mediaType === 'image/jpeg') return parseJpeg(bytes)
  return invalid(`不支持的图片类型：${mediaType}`)
}

export async function validateImageGeometry(blob: Blob, mediaType: string): Promise<ImageGeometry> {
  return parseImageGeometry(new Uint8Array(await blob.arrayBuffer()), mediaType)
}
