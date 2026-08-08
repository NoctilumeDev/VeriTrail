# Contributing to VeriTrail

VeriTrail is currently in the planning stage. Contributions should strengthen the product boundary,
experimental integrity, evidence model, security model, or acceptance criteria before broadening scope.

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
