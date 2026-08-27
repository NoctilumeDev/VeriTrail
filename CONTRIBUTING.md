# Contributing to VeriTrail

VeriTrail Core `0.12.0` remains the immutable M14 baseline, and Core `0.12.2` is the current released
maintenance coordinate. The independently versioned Starter and Authoring Skill entry layers are released
at `0.2.0` and support two bounded DRAFT-only presets: `single-webapp` and `static-site`. They cannot execute
Core seal/run, approve a Preview, or issue or modify a Verdict; the Skill also stops before Starter's
human-reviewed handoff.

The latest publicly released Core coordinate is `0.12.2`. Its bounded producer fix, release notes, protected
tag, public assets, clean-install verification, and readback are recorded in
`docs/74-core-demo-catalog-binding-maintenance-contract.md` through
`docs/76-core-v0.12.2-release-readback-facts.md`. Any later change to the Core payload must first introduce a
new unreleased version coordinate and bounded contract; it must not keep building changed Core bytes as an
already published version or move or rewrite any immutable Core release tag.

Contributions are welcome when they fix a reproducible defect, strengthen a declared gate, improve public
reproducibility, or propose a separately versioned bounded capability. Do not silently broaden a frozen
contract or describe planned, mocked, or advisory behavior as implemented evidence.

All participation is governed by the repository's [Code of Conduct](CODE_OF_CONDUCT.md). Security findings
must follow the private reporting path in [SECURITY.md](SECURITY.md), not a public Issue.

## Before proposing code

1. Read `README.md`, `START_HERE.md`, and the numbered documents relevant to the change. Automated
   contributors must also follow `AGENTS.md`.
2. State the user-visible problem and the executable evidence that would prove it closed.
3. Identify the affected layer:
   - `L0_DOCS`: prose, examples, and public navigation only;
   - `L1_COMPONENT`: one bounded implementation component;
   - `L2_CONTRACT`: a public schema, CLI, workflow, compatibility, or collaboration contract;
   - `L3_SYSTEM`: behavior crossing Core, Starter, Skill, Workbench, or release boundaries.
4. Name the primary variable, controlled variables, resource budget, stop conditions, and hard invariants
   when the change affects an experiment or acceptance conclusion.
5. Explain why the change fits an existing frozen contract or provide a new bounded contract and version
   coordinate. Core `v0.12.0`, Core `v0.12.1`, Core `v0.12.2`, and all published entry-layer release
   coordinates are immutable facts.

## Pull requests

- Keep each pull request focused on one coherent intent.
- Link a reproducible issue or describe the exact failure path in the pull request.
- Include positive, negative, and boundary checks appropriate to the change.
- Record the commands actually run and distinguish automated checks from real browser or real-process
  evidence. A green CI run is necessary but is not a substitute for relevant end-to-end evidence.
- Update README, contracts, examples, and public version or release coordinates in the same change when
  their claims are affected.
- Do not commit secrets, raw customer data, authentication material, machine-specific paths, unredacted
  traces, or generated runtime artifacts.
- If an experiment changes multiple primary variables, mark its conclusion `INCONCLUSIVE` instead of
  claiming causality.

## Repository-declared gates

Run the gates for every layer you changed. The public CI workflow is authoritative; the following commands
are the normal local equivalents.

### Core, Starter, and Authoring Skill

```powershell
python -m unittest -v
python -m unittest discover -s starter/tests -v
python -O -m unittest discover -s starter/tests -v
python -m unittest discover -s skills/veritrail-authoring/tests -v
python -O -m unittest discover -s skills/veritrail-authoring/tests -v
python scripts/authoring_skill_acceptance.py
python scripts/authoring_skill_acceptance.py --preset static-site
```

### Workbench

```powershell
Set-Location web
npm ci --registry=https://registry.npmjs.org
npm test
npm run lint
npm run build
npm audit --audit-level=moderate --registry=https://registry.npmjs.org
```

Changes to browser behavior, process ownership, packaging, or public release assets also require the
corresponding real acceptance path documented in the repository and used by `.github/workflows/`.

## Generated evidence

Runtime artifacts are ignored by default. Only minimal, deterministic, redacted fixtures may be committed,
and each fixture must document its provenance, scope, and expected assertions. Evidence from a different
commit, platform, Plan, or resource boundary must not be reused as proof for the current change.
