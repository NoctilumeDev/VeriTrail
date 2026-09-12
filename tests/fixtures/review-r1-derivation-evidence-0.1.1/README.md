# R1 DerivationEvidence 0.1.1 compatibility corpus

This corpus freezes `R1-DE-CV-001..010` for the additive DerivationEvidence Schema correction.
The three positive cases carry the complete document, the canonical UTF-8 bytes of the
`veritrail.review.derivation-evidence/0.1` identity envelope, and the expected semantic digest.

Negative cases are single-variable mutations of a named positive case. `SCHEMA_REJECT` means the
Draft 2020-12 root rejects the mutation. `CONFORMANCE_REJECT` means the document remains structurally
valid but violates the frozen cross-object rule that the memory-budget diagnostic must name the run
that contains the same diagnostic tuple.

The DIAGNOSTIC manifest is a test-only specimen. It proves the frozen four-file manifest shape can
bind the exact corrected Evidence bytes; it does not create a new manifest version or authorize
runtime publication.
