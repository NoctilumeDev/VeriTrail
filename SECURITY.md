# Security Policy

## Current status

VeriTrail Core 0.12.0 is the frozen v0 release: M0 through M14 are complete, and the annotated `v0.12.0`
tag and Release assets have been read back from GitHub. The independently versioned Starter and Authoring Skill
entry layers are released at `0.2.0`. They support only the bounded `single-webapp` and `static-site` DRAFT paths
and cannot execute Core seal/run, approve a Preview, or issue or modify a Verdict. Starter handoff only emits
human-review instructions; the Skill stops before that handoff. The Skill reads only bounded public filenames
and filesystem metadata, treats repository content as untrusted data, and stops after Starter
`doctor/init/validate/review`. The repository includes the deterministic
Python evidence core, bounded resource/browser adapters, a read-only Vue workbench, rebuildable SQLite
Catalog and loopback API, deterministic Comparison/Pairing/Batch analysis, a trusted Windows ONESHOT
runner, and the Windows 11/C1 one-node and two-node bootstrap candidates. It does not claim support for untrusted code,
arbitrary Shell, cross-platform bootstrap, accounts, cloud sync, or production isolation.

## Reporting a vulnerability

Do not include secrets, personal data, exploit payloads, or unredacted evidence artifacts in a public issue.
Use GitHub's private vulnerability reporting flow when it is available. If it is unavailable, open a minimal
public issue requesting a private contact channel without disclosing the vulnerability details.

## High-risk surfaces

The project treats the following as security-sensitive by design:

- process creation and command arguments;
- browser cookies, tokens, Authorization headers and request bodies;
- environment variables and local configuration;
- filesystem paths and evidence artifact contents;
- database connection information and production-like records;
- imported reports that may contain active HTML or untrusted links.
- local evidence bundle paths, manifests, hashes, attachments, and browser object URLs.

## Required safeguards

- v0 must not execute arbitrary Shell strings.
- Command execution uses structured arguments, explicit digest approval, local executable bindings, Windows
  Job ownership and bounded time/process/memory/output resources; it remains limited to trusted code.
- Sensitive headers and values must be redacted before persistence or export.
- Reports must render imported content as data, not executable HTML.
- The M12 workbench rejects absolute/traversal/confusable paths, undeclared or duplicate files, unknown
  versions, size/count overrun, hash mismatch, missing references, and attachments other than verified
  PNG/JPEG or bounded UTF-8 text. It does not use `v-html`, remote URL import, CDN assets, or persistence
  for local selections.
- Attachment object URLs must be revoked on bundle switch, component teardown, and any later validation
  failure; invalid bundles must not expose a partial Report/Verdict view.
- Local APIs must bind to loopback by default and must not silently expose evidence over the network.
- A Bundle hash proves byte integrity, not truthful authorship. Catalog ingestion must independently derive
  Verdict from the sealed Plan and verified Evidence. Direct Workbench imports must remain visibly labelled
  as self-reported unless loaded through an independently verified Catalog.
- Browser HTTP and WebSocket traffic is limited to sealed loopback origins; Service Workers are blocked in
  managed capture. Screenshots are unredacted pixels and M10 requires explicit operator acknowledgement.
- AI output, if introduced later, is advisory and cannot determine acceptance verdicts or bypass deterministic guards.
