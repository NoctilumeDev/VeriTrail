# R1 Fact / Relation stage applicability capability identity correction audit

> Status: `CORRECTION_AUDIT_CANDIDATE / IMPLEMENTATION_FEASIBILITY_STOP_CONDITION_TRIGGERED`
>
> Exact source world: `main@0a94b32f464f896b86de1cef18dc88dc126225be`
>
> This document preserves the frozen history of
> [the interoperability correction contract](290-r1-fact-handoff-relation-exact-input-interoperability-correction-contract.md)
> and its [freeze publication](291-r1-fact-handoff-relation-exact-input-interoperability-correction-contract-freeze-publication.md).
> It records one new counterexample discovered by the required post-freeze `CONTROL LOOP`. It does not edit those historical
> bytes, implement a successor, or restore the stopped composition authorization.

## 1. CONTROL LOOP coordinate and authority

The current protected branch, local checkout, and remote branch all resolve to:

```text
0a94b32f464f896b86de1cef18dc88dc126225be
```

The only open pull requests at the start of this audit were dependency updates. No semantic pull request had already implemented
the correction. The upstream state therefore remained:

```text
R1_FACT_HANDOFF_RELATION_EXACT_INPUT_INTEROPERABILITY_CORRECTION_CONTRACT_FROZEN
R1_FACT_HANDOFF_RELATION_EXACT_INPUT_INTEROPERABILITY_CORRECTION_FEASIBILITY_NOT_STARTED
R1_FACT_HANDOFF_RELATION_EXACT_INPUT_INTEROPERABILITY_CORRECTION_IMPLEMENTATION_NOT_STARTED
R1_FACT_HANDOFF_RELATION_EXACT_INPUT_INTEROPERABILITY_CORRECTION_IMPLEMENTATION_NOT_AUTHORIZED
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_IMPLEMENTATION_STOP_CONDITION_TRIGGERED
R1_REVIEW_SLICE_SET_COVERAGE_MANIFEST_SUCCESSOR_NOT_SELECTED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
```

Doc 291 section 6 requires a fresh feasibility review before any successor implementation. That review found a narrower frozen
contract identity problem before runtime construction began. No product diff had been created.

## 2. Counterexample: the frozen Fact-stage capability does not exist

Doc 290 section 5 freezes the minimum stage owner mapping as:

```text
FACT stage
    owns review-fact-derivation requirement

RELATION stage
    owns review-relation-derivation requirement
```

At this exact main, `review-fact-derivation` occurs only in that sentence. It is absent from runtime, tests, Schema, Profile,
Policy fixtures, Provider descriptors, and all other tracked documentation.

The actual Fact-stage provider requirement identities are:

```text
python-ast             required
python-ast-advisory    optional, when declared
```

The actual Relation-stage requirement identity is:

```text
review-relation-derivation    required
```

The mismatch is material because doc 290 also requires the applicability projection to bind the complete identities of both
partition sides. In this contract, a capability string is not an informal label that an implementation may silently reinterpret.

## 3. Mechanical worlds

The read-only audit constructed three complete sealed Policy worlds through the current generic `DerivationInputSet` validator.
All three Policy documents were structurally valid and had fresh canonical digests.

| Policy world | Generic Policy admission | Current Fact applicability | Current Relation requirement |
| --- | --- | --- | --- |
| `python-ast + review-relation-derivation` | ACCEPTED | REJECTED: `unqualified requiredness` | ACCEPTED |
| `python-ast + python-ast-advisory + review-relation-derivation` | ACCEPTED | REJECTED: `unqualified requiredness` | ACCEPTED |
| literal doc 290: `review-fact-derivation + review-relation-derivation` | ACCEPTED | REJECTED: `unqualified requiredness` | REJECTED |

The first two rows reproduce the known same-Policy seam: current Fact applicability rejects an otherwise valid Relation
requirement. The third row is the new counterexample: applying the frozen Fact owner literally does not identify an existing Fact
requirement and makes neither stage admissible.

Therefore the next implementation cannot truthfully claim conformance by choosing any of these shortcuts:

```text
review-fact-derivation is only prose
review-fact-derivation aliases python-ast
the implementation may infer the intended owner
the current Fact worker implicitly supplies the missing identity
```

None of those relations is frozen or represented in repository truth.

## 4. Fresh four-cell audit and retained setup failure

The audit ran on CPython 3.10.6 and 3.13.13, in normal and `-O` modes. All four fresh attempt-2 semantic reports are byte-equivalent
after excluding the Python observation coordinates:

```text
f2319f6300b878cf2d8dec8c4291bf514c8cc2dd83afa816bc228e7f012412e7
```

Audit script SHA-256:

```text
f5f2073d5f3fe4fd5d1ff7dec6ea353ec94fe54ca1436e721a3e50bed057b80e
```

Closeout summary SHA-256:

```text
2b15bcad00bec95d320d3a2e807a7d40aa01243eedf177cc2e18849ae0a02caa
```

Attempt 1 supplied a hand-authored 64 MiB transport limit outside the frozen execution-cell range. It stopped before the intended
applicability call with `FrameProtocolError`. That observation is retained as `AUDIT_HARNESS_SETUP_ERROR`; attempt 2 uses the
repository's unchanged `DEFAULT_TRANSPORT_LIMITS` and a new observation identity.

As an independent product baseline, these four modules ran in the same four cells:

```text
test_fact_fulfillment
test_relation_derivation
test_relation_observation_qualification
test_relation_set_admission
```

Each cell reported:

```text
Ran 77 tests
OK (skipped=1)
```

The counterexample is therefore not a newly observed product regression. It is a contract-to-runtime identity contradiction that
the existing regression suite is not designed to reject.

One later PowerShell hash-listing command used `-LiteralPath` with a wildcard and failed before enumeration. It is retained as an
`OPERATOR_COMMAND_SETUP_ERROR`; the corrected enumeration did not alter audit output.

## 5. Minimal correction boundary

The evidence supports one narrow owner map for a future contract correction:

```text
FACT stage applicable requirements
    python-ast
    python-ast-advisory, if present

RELATION stage applicable requirements
    review-relation-derivation

requirements(P)
    = applicable_requirements(stage)
      disjoint-union non_applicable_requirements(stage)
```

This map is compatible with the existing Provider descriptors and with both actual combined Policy worlds. It retains every
requirement in the exact Policy and does not let either stage discharge the other stage's responsibility.

The future correction must still decide and freeze the corrected contract identity/version. This audit does not silently edit doc
290, invent an alias, or pre-authorize runtime. It reopens only the capability-owner identity in doc 290 section 5. The following
remain unchanged:

- complete sealed Policy and `policy_digest` remain the exact world;
- complete authoritative FactSet and same-attempt handoff history remain the Relation operand;
- per accepted product/path MODULE closure remains required;
- obligation projection remains total, bidirectionally reconciled, cardinality-preserving, and unique;
- known-empty, missing, blocked, and unknown remain distinct;
- live claim and continuation never follow from equal bytes or equal semantic digests;
- legacy domain/request identities remain immutable;
- all `FRIC-001..018` falsifiers and the `UNKNOWN / UNSAT` boundary remain in force.

## 6. Current ruling

| Question | Ruling |
| --- | --- |
| Is doc 290 / 291 frozen history preserved? | **Yes** |
| Can corrected successor feasibility proceed under the literal section 5 owner map? | **No** |
| Does `review-fact-derivation` name a current Policy capability? | **No** |
| Can it be silently treated as an alias for `python-ast`? | **No** |
| Is the actual owner map mechanically identifiable? | **Yes: `python-ast`, optional `python-ast-advisory`, and `review-relation-derivation`** |
| Did runtime or tests change? | **No** |
| Did implementation start or receive authority? | **No** |
| Did persistence, manifest, Coverage, or public Review start? | **No** |

Current candidate state:

```text
R1_FACT_HANDOFF_RELATION_EXACT_INPUT_INTEROPERABILITY_CORRECTION_CONTRACT_FROZEN_HISTORY_PRESERVED
R1_FACT_HANDOFF_RELATION_STAGE_APPLICABILITY_CAPABILITY_IDENTITY_COUNTEREXAMPLE
R1_FACT_HANDOFF_RELATION_EXACT_INPUT_INTEROPERABILITY_CORRECTION_IMPLEMENTATION_FEASIBILITY_STOP_CONDITION_TRIGGERED
R1_FACT_HANDOFF_RELATION_STAGE_APPLICABILITY_CAPABILITY_IDENTITY_CORRECTION_AUDIT_CANDIDATE
R1_FACT_HANDOFF_RELATION_EXACT_INPUT_INTEROPERABILITY_CORRECTION_IMPLEMENTATION_NOT_STARTED
R1_FACT_HANDOFF_RELATION_EXACT_INPUT_INTEROPERABILITY_CORRECTION_IMPLEMENTATION_NOT_AUTHORIZED
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_IMPLEMENTATION_STOP_CONDITION_TRIGGERED
R1_REVIEW_SLICE_SET_COVERAGE_MANIFEST_SUCCESSOR_NOT_SELECTED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
```

## 7. Candidate qualification and stop line

This candidate's tracked scope is limited to `README.md`, `AGENTS.md`, `docs/milestones.md`, and this new document. Doc 290, doc
291, runtime, tests, workflows, Schema, manifest, fixtures, Profile, Policy, vectors, corpus, and doc 292 must retain their base
bytes.

Final bytes must pass the declared Markdown, link, marker, byte-continuity, `git diff --check`, baseline, four-cell audit, and
read-only hygiene gates. Qualification then remains:

```text
final docs-only audit bytes / declared local gates
    -> original PR required gates
    -> separately approved exact-head protected merge
    -> new exact-main Public CI + Browser Smoke
    -> fresh anonymous installed-product README / this document / milestones readback
    -> independent Core / source-byte / Bundle / identity / retained-history reconciliation
    -> qualified correction audit history
    -> return CONTROL LOOP
```

Even after those gates close, the only possible next seam is a separate docs-only minimal contract correction candidate for the
stage-owner identity. This audit does not authorize successor runtime, restore composition A–J, choose a manifest or persistence
route, start Coverage/public Review, run the post-R1 Benchmark, or start R2/R3.
