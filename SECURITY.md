# Security Policy

## Current status

VeriTrail is a pre-release v0 implementation with M0 through M3 frozen and no supported public release.
The Python evidence core, bounded resource/browser adapters, and read-only Vue evidence workbench exist;
SQLite, a local API, command orchestration, accounts, cloud sync, and a complete self-hosted loop remain
future work.

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
- Command execution, if introduced later, requires structured arguments, explicit preview, an auditable allowlist and bounded time/resources.
- Sensitive headers and values must be redacted before persistence or export.
- Reports must render imported content as data, not executable HTML.
- The M3 workbench rejects absolute/traversal/confusable paths, undeclared or duplicate files, unknown
  versions, size/count overrun, hash mismatch, missing references, and attachments other than verified
  PNG/JPEG. It does not use `v-html`, remote URL import, CDN assets, or persistence for local selections.
- Attachment object URLs must be revoked on bundle switch, component teardown, and any later validation
  failure; invalid bundles must not expose a partial Report/Verdict view.
- Local APIs must bind to loopback by default and must not silently expose evidence over the network.
- AI output, if introduced later, is advisory and cannot determine acceptance verdicts or bypass deterministic guards.
