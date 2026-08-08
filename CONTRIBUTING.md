# Contributing to VeriTrail

VeriTrail is in early v0 implementation. M0 freezes the sealed-plan-to-verdict-bundle contract and M1
adds a bounded resource preflight; later milestones remain gated. Contributions should close the active milestone or strengthen its product,
experimental-integrity, evidence, security, and acceptance boundaries before broadening scope.

## Before proposing code

1. Read `README.md` and the numbered documents under `docs/`.
2. State the user problem and the evidence required to prove the change works.
3. Identify the primary variable, controlled variables, resource budget, stop conditions, and hard invariants.
4. Explain why the change belongs in the first vertical slice rather than a future adapter.

## Pull requests

- Keep each pull request focused on one coherent change.
- Do not commit secrets, raw customer data, authentication material, machine-specific paths, or unredacted traces.
- Include deterministic checks and real-run evidence appropriate to the change.
- Do not describe planned or mocked behavior as implemented.
- If an experiment changes multiple primary variables, mark its conclusion `INCONCLUSIVE` instead of claiming causality.

## Generated evidence

Runtime artifacts are ignored by default. Only minimal, deterministic, redacted fixtures may be committed,
and each fixture must document its provenance and expected assertions.
