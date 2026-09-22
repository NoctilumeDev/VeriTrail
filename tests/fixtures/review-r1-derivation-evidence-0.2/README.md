# DerivationEvidence 0.2 admission corpus

This independent corpus exercises the frozen RelationSet admission and public
qualification binding contract.

- `valid-consistent/` binds a `QUALIFIED / CONSISTENT` private composition to
  an exact RelationSet and a non-null admission witness.
- `valid-conflicting/` binds a `QUALIFIED / CONFLICTING` composition without
  selecting a winner or creating a Slice.
- `valid-interrupted-null/` preserves the fail-closed non-completed shape:
  `relation_admission` is `null` and every final reported identity array is
  empty.
- `compatibility-cases.json` declares single-variable negative vectors.
- `identity-vectors.json` freezes the 0.2 Evidence identity domain, canonical
  artifact SHA-256 values, and the positive admission identities.

The corpus does not grant publication authority and does not add a Manifest
role or ninth file.
