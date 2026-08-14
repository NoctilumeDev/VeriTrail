import { describe, expect, it, vi } from 'vitest'
import {
  BundleLoadError,
  loadBundleFromBlobs,
  normalizeBundlePath,
  sha256Hex,
} from '../src/domain/bundle'
import {
  createMinimalBundle,
  createSealedPlan,
  createSingleApplicationBootstrapBundle,
  minimalReport,
} from './support'

describe('Bundle Loader', () => {
  it('verifies a Report 0.1 bundle without browser evidence', async () => {
    const loaded = await loadBundleFromBlobs(await createMinimalBundle(), 'unit')

    expect(loaded.report.execution_status).toBe('COMPLETED')
    expect(loaded.report.verdict).toBe('PASS')
    expect(loaded.integrity).toEqual({
      verified: true,
      authorityVerified: false,
      verifiedFiles: 3,
      totalBytes: expect.any(Number),
    })
    expect(loaded.evidenceByPath).toEqual({})
    loaded.release()
  })

  it('preserves Plan 0.7 single-application bootstrap facts without a dependency placeholder', async () => {
    const entries = await createSingleApplicationBootstrapBundle()
    const loaded = await loadBundleFromBlobs(entries, 'unit-single-application')
    const evidence = loaded.evidenceByPath['evidence/runtime.bootstrap.json']!
    const facts = evidence.facts as {
      nodes: Array<{ node_id: string; role: string }>
      start_order: { sealed: string[]; actual: string[] }
      teardown_order: { sealed: string[]; attempted: string[]; completed: string[] }
      resource_observation: {
        application_peak_rss_mb: number
        dependency_peak_rss_mb: number | null
      }
    }
    const authority = JSON.parse(await entries.get('sealed-plan.json')!.text()) as {
      schema_version: string
    }

    expect(authority.schema_version).toBe('0.7')
    expect(loaded.report.primary_variable).toMatchObject({
      name: 'project_bootstrap_topology',
      value: 'veritrail_managed_windows_c1_single_application',
    })
    expect(evidence.source).toBe('VeriTrail bootstrap-lifecycle/0.3')
    expect(facts.nodes).toEqual([{ node_id: 'application', role: 'APPLICATION' }])
    expect(facts.start_order).toEqual({ sealed: ['application'], actual: ['application'] })
    expect(facts.teardown_order).toEqual({
      sealed: ['application'],
      attempted: ['application'],
      completed: ['application'],
    })
    expect(facts.resource_observation).toEqual({
      application_peak_rss_mb: 32,
      dependency_peak_rss_mb: null,
    })
    expect(loaded.evidenceManifest.artifacts[0]!.attachments.map((item) => item.logical_name)).toEqual([
      'bootstrap-application-stdout',
      'bootstrap-application-stderr',
    ])
    expect(facts.nodes.some((node) => node.role === 'DEPENDENCY')).toBe(false)
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

  it('rejects a bundle whose sealed Plan is missing', async () => {
    const entries = await createMinimalBundle()
    entries.delete('sealed-plan.json')

    await expect(loadBundleFromBlobs(entries, 'unit')).rejects.toMatchObject({
      code: 'MISSING_REFERENCE',
    })
  })

  it('rejects a valid but different sealed Plan after manifest hashes are updated', async () => {
    const entries = await createMinimalBundle()
    const replacement = await createSealedPlan('different-plan', 1)
    entries.set('sealed-plan.json', replacement.blob)
    const manifest = JSON.parse(await entries.get('bundle-manifest.json')!.text()) as {
      files: Array<{ path: string; sha256: string; size: number }>
    }
    const authorityEntry = manifest.files.find((file) => file.path === 'sealed-plan.json')!
    authorityEntry.sha256 = await sha256Hex(replacement.blob)
    authorityEntry.size = replacement.blob.size
    entries.set('bundle-manifest.json', new Blob([JSON.stringify(manifest)]))

    await expect(loadBundleFromBlobs(entries, 'unit')).rejects.toMatchObject({
      code: 'AUTHORITY_MISMATCH',
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

  it('rejects semantically unbounded browser evidence despite valid file hashes', async () => {
    const authority = await createSealedPlan('unit-plan', 1)
    const evidenceBlob = new Blob([
      JSON.stringify({
        schema_version: '0.1',
        evidence_type: 'browser.session',
        source: 'unit',
        captured_at: '2026-08-13T00:00:00Z',
        facts: {
          viewport_runs: [],
          steps: [],
          console: Array.from({ length: 501 }, () => ({ level: 'log' })),
          page_errors: [],
          network: [],
          screenshots: [],
          viewport_count: 0,
          screenshot_count: 0,
        },
      }),
    ])
    const artifact = {
      evidence_type: 'browser.session',
      path: 'evidence/browser.json',
      sha256: await sha256Hex(evidenceBlob),
      size: evidenceBlob.size,
      redacted: true,
      redacted_fields: 0,
      redaction_rule_version: '0.1',
      parser_version: '0.1',
      captured_at: '2026-08-13T00:00:00Z',
      source: 'unit',
      source_name: 'unit-browser',
      retention: 'ephemeral',
      attachments: [],
    }
    const reportBlob = new Blob([
      JSON.stringify(minimalReport({
        plan: { id: 'unit-plan', version: 1, sha256: authority.digest },
        evidence: [artifact],
      })),
    ])
    const evidenceManifestBlob = new Blob([
      JSON.stringify({
        schema_version: '0.1',
        run_id: 'unit-run',
        artifacts: [artifact],
        duplicate_inputs_ignored: [],
      }),
    ])
    const entries = new Map<string, Blob>([
      ['report.json', reportBlob],
      ['evidence-manifest.json', evidenceManifestBlob],
      ['evidence/browser.json', evidenceBlob],
      ['sealed-plan.json', authority.blob],
    ])
    const files = await Promise.all(
      [...entries].map(async ([path, blob]) => ({
        path,
        sha256: await sha256Hex(blob),
        size: blob.size,
      })),
    )
    entries.set(
      'bundle-manifest.json',
      new Blob([JSON.stringify({ schema_version: '0.1', run_id: 'unit-run', files })]),
    )

    await expect(loadBundleFromBlobs(entries, 'unit')).rejects.toMatchObject({
      code: 'EVIDENCE_LIMIT',
    })
  })

  it('accepts hashed UTF-8 command output without treating it as an image', async () => {
    const authority = await createSealedPlan('unit-plan', 1)
    const outputBlob = new Blob(['sanitized command output\n'], {
      type: 'text/plain; charset=utf-8',
    })
    const evidenceBlob = new Blob([
      JSON.stringify({
        schema_version: '0.1',
        evidence_type: 'runtime.command',
        source: 'unit',
        captured_at: '2026-08-11T00:00:00Z',
        facts: {},
      }),
    ])
    const attachment = {
      logical_name: 'command-stdout',
      media_type: 'text/plain; charset=utf-8',
      path: 'attachments/command/stdout.txt',
      sha256: await sha256Hex(outputBlob),
      size: outputBlob.size,
    }
    const artifact = {
      evidence_type: 'runtime.command',
      path: 'evidence/001-runtime.command.json',
      sha256: await sha256Hex(evidenceBlob),
      size: evidenceBlob.size,
      redacted: true,
      redacted_fields: 0,
      redaction_rule_version: '0.1',
      parser_version: '0.1',
      captured_at: '2026-08-11T00:00:00Z',
      source: 'unit',
      source_name: 'generated-command.json',
      retention: 'ephemeral',
      attachments: [attachment],
    }
    const reportBlob = new Blob([JSON.stringify(minimalReport({
      plan: { id: 'unit-plan', version: 1, sha256: authority.digest },
      evidence: [artifact],
    }))])
    const evidenceManifestBlob = new Blob([
      JSON.stringify({
        schema_version: '0.1',
        run_id: 'unit-run',
        artifacts: [artifact],
        duplicate_inputs_ignored: [],
      }),
    ])
    const entries = new Map<string, Blob>([
      ['report.json', reportBlob],
      ['evidence-manifest.json', evidenceManifestBlob],
      ['evidence/001-runtime.command.json', evidenceBlob],
      ['attachments/command/stdout.txt', outputBlob],
      ['sealed-plan.json', authority.blob],
    ])
    const files = await Promise.all(
      [...entries].map(async ([path, blob]) => ({
        path,
        sha256: await sha256Hex(blob),
        size: blob.size,
      })),
    )
    entries.set(
      'bundle-manifest.json',
      new Blob([JSON.stringify({ schema_version: '0.1', run_id: 'unit-run', files })]),
    )

    const loaded = await loadBundleFromBlobs(entries, 'unit')

    expect(loaded.evidenceManifest.artifacts[0]?.attachments).toEqual([attachment])
    expect(loaded.imageUrls).toEqual({})
    loaded.release()
  })

  it('revokes attachment object URLs when a later evidence document is invalid', async () => {
    const authority = await createSealedPlan('unit-plan', 1)
    const attachmentBlob = new Blob([new Uint8Array([137, 80, 78, 71])], { type: 'image/png' })
    const firstEvidenceBlob = new Blob([
      JSON.stringify({
        schema_version: '0.1',
        evidence_type: 'browser.session',
        source: 'unit',
        captured_at: '2026-08-09T00:00:00Z',
        facts: {
          viewport_runs: [],
          steps: [],
          console: [],
          page_errors: [],
          network: [],
          screenshots: [],
          viewport_count: 0,
          screenshot_count: 0,
        },
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
      JSON.stringify(minimalReport({
        plan: { id: 'unit-plan', version: 1, sha256: authority.digest },
        evidence: artifacts,
      })),
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
      ['sealed-plan.json', authority.blob],
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
