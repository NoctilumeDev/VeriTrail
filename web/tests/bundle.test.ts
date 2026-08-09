import { describe, expect, it, vi } from 'vitest'
import {
  BundleLoadError,
  loadBundleFromBlobs,
  normalizeBundlePath,
  sha256Hex,
} from '../src/domain/bundle'
import { createMinimalBundle, minimalReport } from './support'

describe('Bundle Loader', () => {
  it('verifies a Report 0.1 bundle without browser evidence', async () => {
    const loaded = await loadBundleFromBlobs(await createMinimalBundle(), 'unit')

    expect(loaded.report.execution_status).toBe('COMPLETED')
    expect(loaded.report.verdict).toBe('PASS')
    expect(loaded.integrity).toEqual({ verified: true, verifiedFiles: 2, totalBytes: expect.any(Number) })
    expect(loaded.evidenceByPath).toEqual({})
    loaded.release()
  })

  it.each(['../report.json', '/report.json', 'C:/report.json', 'folder\\report.json', 'folder//report.json'])(
    'rejects unsafe path %s',
    (path) => {
      expect(() => normalizeBundlePath(path)).toThrowError(BundleLoadError)
    },
  )

  it('rejects a hash mismatch before displaying report facts', async () => {
    const entries = await createMinimalBundle()
    entries.set('report.json', new Blob(['{}']))

    await expect(loadBundleFromBlobs(entries, 'unit')).rejects.toMatchObject({ code: 'SIZE_MISMATCH' })
  })

  it('rejects an unknown report version even when integrity is valid', async () => {
    const entries = await createMinimalBundle({ schema_version: '9.9' })

    await expect(loadBundleFromBlobs(entries, 'unit')).rejects.toMatchObject({ code: 'UNSUPPORTED_VERSION' })
  })

  it('rejects undeclared local files', async () => {
    const entries = await createMinimalBundle()
    entries.set('extra.json', new Blob(['{}']))

    await expect(loadBundleFromBlobs(entries, 'unit')).rejects.toMatchObject({ code: 'UNDECLARED_FILE' })
  })

  it('rejects duplicate paths in the bundle manifest', async () => {
    const entries = await createMinimalBundle()
    const manifest = JSON.parse(await entries.get('bundle-manifest.json')!.text()) as {
      files: Array<Record<string, unknown>>
    }
    manifest.files.push({ ...manifest.files.find((file) => file.path === 'report.json')! })
    entries.set('bundle-manifest.json', new Blob([JSON.stringify(manifest)]))

    await expect(loadBundleFromBlobs(entries, 'unit')).rejects.toMatchObject({
      code: 'DUPLICATE_PATH',
    })
  })

  it('rejects a declared file that is missing from the selected bundle', async () => {
    const entries = await createMinimalBundle()
    entries.delete('report.json')

    await expect(loadBundleFromBlobs(entries, 'unit')).rejects.toMatchObject({
      code: 'MISSING_REFERENCE',
    })
  })

  it('stops before parsing when the selection exceeds 256 files', async () => {
    const entries = await createMinimalBundle()
    for (let index = 0; index < 255; index += 1) {
      entries.set(`extra/${index}.json`, new Blob(['{}']))
    }

    await expect(loadBundleFromBlobs(entries, 'unit')).rejects.toMatchObject({ code: 'FILE_LIMIT' })
  })

  it('stops before parsing a file larger than 10 MiB', async () => {
    const entries = await createMinimalBundle()
    entries.set('oversized.bin', new Blob([new Uint8Array(10 * 1024 * 1024 + 1)]))

    await expect(loadBundleFromBlobs(entries, 'unit')).rejects.toMatchObject({ code: 'FILE_SIZE_LIMIT' })
  })

  it('uses Web Crypto SHA-256 deterministically', async () => {
    await expect(sha256Hex(new Blob(['veritrail']))).resolves.toBe(
      '14e47fb57c93e3c11aed5834546eec7de31a35934072dd7ef3178dd479a7165d',
    )
  })

  it('revokes attachment object URLs when a later evidence document is invalid', async () => {
    const attachmentBlob = new Blob([new Uint8Array([137, 80, 78, 71])], { type: 'image/png' })
    const firstEvidenceBlob = new Blob([
      JSON.stringify({
        schema_version: '0.1',
        evidence_type: 'browser.session',
        source: 'unit',
        captured_at: '2026-08-09T00:00:00Z',
        facts: {},
      }),
    ])
    const invalidEvidenceBlob = new Blob([
      JSON.stringify({
        schema_version: '0.1',
        evidence_type: 'wrong.type',
        source: 'unit',
        captured_at: '2026-08-09T00:00:00Z',
        facts: {},
      }),
    ])
    const attachment = {
      logical_name: 'unit screenshot',
      media_type: 'image/png',
      path: 'attachments/unit.png',
      sha256: await sha256Hex(attachmentBlob),
      size: attachmentBlob.size,
    }
    const artifact = async (evidenceType: string, path: string, blob: Blob, attachments: unknown[]) => ({
      evidence_type: evidenceType,
      path,
      sha256: await sha256Hex(blob),
      size: blob.size,
      redacted: true,
      redacted_fields: 0,
      redaction_rule_version: '0.1',
      parser_version: '0.1',
      captured_at: '2026-08-09T00:00:00Z',
      source: 'unit',
      source_name: 'unit',
      retention: 'ephemeral',
      attachments,
    })
    const artifacts = [
      await artifact('browser.session', 'evidence/first.json', firstEvidenceBlob, [attachment]),
      await artifact('runtime.preflight', 'evidence/invalid.json', invalidEvidenceBlob, []),
    ]
    const reportBlob = new Blob([
      JSON.stringify(minimalReport({ evidence: artifacts })),
    ])
    const evidenceManifestBlob = new Blob([
      JSON.stringify({
        schema_version: '0.1',
        run_id: 'unit-run',
        artifacts,
        duplicate_inputs_ignored: [],
      }),
    ])
    const dataFiles = new Map<string, Blob>([
      ['report.json', reportBlob],
      ['evidence-manifest.json', evidenceManifestBlob],
      ['evidence/first.json', firstEvidenceBlob],
      ['evidence/invalid.json', invalidEvidenceBlob],
      ['attachments/unit.png', attachmentBlob],
    ])
    const files = await Promise.all(
      [...dataFiles].map(async ([path, blob]) => ({
        path,
        sha256: await sha256Hex(blob),
        size: blob.size,
      })),
    )
    dataFiles.set(
      'bundle-manifest.json',
      new Blob([JSON.stringify({ schema_version: '0.1', run_id: 'unit-run', files })]),
    )
    const createUrl = vi.spyOn(URL, 'createObjectURL').mockReturnValue('blob:unit')
    const revokeUrl = vi.spyOn(URL, 'revokeObjectURL').mockImplementation(() => undefined)

    await expect(loadBundleFromBlobs(dataFiles, 'unit')).rejects.toMatchObject({
      code: 'REFERENCE_MISMATCH',
    })
    expect(createUrl).toHaveBeenCalledTimes(1)
    expect(revokeUrl).toHaveBeenCalledWith('blob:unit')
    createUrl.mockRestore()
    revokeUrl.mockRestore()
  })
})
