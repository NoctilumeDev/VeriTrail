import { describe, expect, it } from 'vitest'

import {
  ImageGeometryError,
  parseImageGeometry,
  validateImageGeometry,
} from '../src/domain/image-geometry'
import { createTestPng } from './support'

function u16(value: number): Uint8Array {
  return new Uint8Array([(value >>> 8) & 0xff, value & 0xff])
}

function concatBytes(...parts: Uint8Array[]): Uint8Array {
  const result = new Uint8Array(parts.reduce((total, part) => total + part.length, 0))
  let offset = 0
  for (const part of parts) {
    result.set(part, offset)
    offset += part.length
  }
  return result
}

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

function writeU32(bytes: Uint8Array, offset: number, value: number): void {
  bytes[offset] = (value >>> 24) & 0xff
  bytes[offset + 1] = (value >>> 16) & 0xff
  bytes[offset + 2] = (value >>> 8) & 0xff
  bytes[offset + 3] = value & 0xff
}

function crc32(bytes: Uint8Array, start: number, end: number): number {
  let crc = 0xffffffff
  for (let index = start; index < end; index += 1) {
    crc = (crc >>> 8) ^ CRC32_TABLE[(crc ^ bytes[index]!) & 0xff]!
  }
  return (crc ^ 0xffffffff) >>> 0
}

function createPngWithLargeAncillaryChunk(payloadSize: number): Uint8Array {
  const original = createTestPng()
  const firstChunkEnd = 8 + 12 + 13
  const chunkSize = 12 + payloadSize
  const result = new Uint8Array(original.length + chunkSize)
  result.set(original.subarray(0, firstChunkEnd), 0)
  writeU32(result, firstChunkEnd, payloadSize)
  const typeStart = firstChunkEnd + 4
  result.set(new TextEncoder().encode('tEXt'), typeStart)
  const payloadEnd = typeStart + 4 + payloadSize
  writeU32(result, payloadEnd, crc32(result, typeStart, payloadEnd))
  result.set(original.subarray(firstChunkEnd), payloadEnd + 4)
  return result
}

function createPngWithCorruptedIdatCrc(): Uint8Array {
  const result = createTestPng()
  const firstChunkEnd = 8 + 12 + 13
  const idatPayloadStart = firstChunkEnd + 8
  result[idatPayloadStart] ^= 1
  return result
}

function createTestJpeg(width: number, height: number): Uint8Array {
  const sof = concatBytes(
    new Uint8Array([8]),
    u16(height),
    u16(width),
    new Uint8Array([1, 1, 0x11, 0]),
  )
  const scan = new Uint8Array([1, 1, 0, 0, 63, 0])
  return concatBytes(
    new Uint8Array([0xff, 0xd8, 0xff, 0xc0]),
    u16(sof.length + 2),
    sof,
    new Uint8Array([0xff, 0xda]),
    u16(scan.length + 2),
    scan,
    new Uint8Array([0, 0xff, 0xd9]),
  )
}

describe('image geometry policy', () => {
  it('accepts ordinary PNG and JPEG screenshots', async () => {
    expect(parseImageGeometry(createTestPng(1920, 1080), 'image/png')).toMatchObject({
      width: 1920,
      height: 1080,
      pixels: 2_073_600,
    })
    await expect(
      validateImageGeometry(
        new Blob([createTestJpeg(1280, 720).buffer as ArrayBuffer], { type: 'image/jpeg' }),
        'image/jpeg',
      ),
    ).resolves.toMatchObject({ width: 1280, height: 720, pixels: 921_600 })
  })

  it.each([
    [createTestPng(8193, 1), 'image/png'],
    [createTestPng(4097, 4097), 'image/png'],
    [createTestJpeg(8193, 1), 'image/jpeg'],
  ] as const)('rejects oversized geometry before browser decoding', (bytes, mediaType) => {
    expect(() => parseImageGeometry(bytes, mediaType)).toThrowError(ImageGeometryError)
    try {
      parseImageGeometry(bytes, mediaType)
    } catch (error) {
      expect(error).toMatchObject({ code: 'IMAGE_GEOMETRY_LIMIT' })
    }
  })

  it.each([
    [new Uint8Array([137, 80, 78, 71, 13, 10, 26, 10]), 'image/png'],
    [createTestPng().subarray(0, createTestPng().length - 4), 'image/png'],
    [createPngWithCorruptedIdatCrc(), 'image/png'],
    [new Uint8Array([0xff, 0xd8, 0xff, 0xd9]), 'image/jpeg'],
    [createTestJpeg(1, 1).subarray(0, createTestJpeg(1, 1).length - 2), 'image/jpeg'],
  ] as const)('rejects malformed image bytes with a matching media type', (bytes, mediaType) => {
    expect(() => parseImageGeometry(bytes, mediaType)).toThrowError(ImageGeometryError)
    try {
      parseImageGeometry(bytes, mediaType)
    } catch (error) {
      expect(error).toMatchObject({ code: 'INVALID_IMAGE' })
    }
  })

  it('validates a large PNG chunk without multiplying work per byte', { timeout: 10_000 }, () => {
    const png = createPngWithLargeAncillaryChunk(48 * 1024 * 1024)
    const startedAt = performance.now()

    expect(parseImageGeometry(png, 'image/png')).toMatchObject({ width: 1, height: 1 })
    expect(performance.now() - startedAt).toBeLessThan(2_000)
  })
})
