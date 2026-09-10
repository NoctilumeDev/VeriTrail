# R1 Schema 0.1 compatibility corpus

This directory is the data-only compatibility corpus for the frozen R1 Schema and canonical-identity contract.
It contains no SourceSnapshot importer, parser, relation producer, slice engine, coverage producer, CLI, Provider, or
runtime capability.

- `valid-complete/` is one internally consistent synthetic COMPLETE bundle. Every Artifact is canonical JSON followed
  by exactly one LF; `manifest.json` binds its exact bytes and semantic identity.
- `identity-vectors/` stores full identity envelopes, expected canonical UTF-8 bytes as lowercase hex, and expected
  SHA-256 digests. The files are split only to keep individual vectors reviewable.
- `compatibility-cases.json` gives each of the twenty frozen compatibility obligations an exact data coordinate.

JSON Schema proves document shape. Tests separately recompute canonical bytes, semantic/file digests, fixed ordering,
references, set equations, status joins, and path rules. Passing Schema validation alone never means that an Artifact
is semantically conformant or that a repository has been understood.
