# Security Policy

## Current status

VeriTrail is in the planning stage and has no supported release. The security boundaries in this document
are requirements for the first implementation, not claims about code that does not yet exist.

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

## Required safeguards

- v0 must not execute arbitrary Shell strings.
- Command execution, if introduced later, requires structured arguments, explicit preview, an auditable allowlist and bounded time/resources.
- Sensitive headers and values must be redacted before persistence or export.
- Reports must render imported content as data, not executable HTML.
- Local APIs must bind to loopback by default and must not silently expose evidence over the network.
- AI output, if introduced later, is advisory and cannot determine acceptance verdicts or bypass deterministic guards.
