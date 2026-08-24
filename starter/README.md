# VeriTrail Starter 0.2.0 (development)

`veritrail-starter` is the independent, fail-closed DRAFT authoring entry for
VeriTrail Core 0.12.x. Version 0.2.0 keeps the frozen `single-webapp`
preset and adds the independently contracted `static-site` preset on Windows 11.

It can inspect explicit answers, create deterministic unsealed Profile/Plan drafts,
validate a local authoring workspace, and print a manual Core handoff. It never seals,
runs, approves a Preview, or decides a Verdict. It is an authoring entry, not a
second evaluator.

## Released installation

Starter 0.1.0 remains the latest published release while 0.2.0 is developed in
source. The released wheel is distributed from the GitHub Release named
`VeriTrail Starter 0.1.0`; it is not published to PyPI. Verify the downloaded
files against `SHA256SUMS-starter.txt`, then install the frozen Core wheel and
the Starter wheel into a clean virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install `
  https://github.com/NoctilumeDev/VeriTrail/releases/download/v0.12.0/veritrail-0.12.0-py3-none-any.whl `
  https://github.com/NoctilumeDev/VeriTrail/releases/download/starter-v0.1.0/veritrail_starter-0.1.0-py3-none-any.whl
```

The source distribution is provided for independent build verification. It is
not a reason to install the repository in editable mode.

## Authoring usage

```powershell
veritrail-starter doctor --answers C:\absolute\path\answers.json
veritrail-starter init --preset single-webapp --answers C:\absolute\path\answers.json
veritrail-starter init --preset static-site --answers C:\absolute\path\static-answers.json
veritrail-starter validate --workspace C:\absolute\subject\.veritrail
veritrail-starter review --workspace C:\absolute\subject\.veritrail
```

Every command writes exactly one versioned JSON result to stdout. `handoff` is
available for an advanced human operator after review; it only validates the
DRAFT and points at a PowerShell file that **prints** manual Core commands. It
does not execute those commands. The Authoring Skill cannot call `handoff`.

The input contracts are packaged at
`veritrail_starter/schemas/answers-0.1.schema.json` and
`veritrail_starter/schemas/answers-0.2.schema.json`. Answers 0.1 remains the frozen
`single-webapp` contract; Answers 0.2 adds the preset-specific `static-site` block.
Runtime validation is stricter
than the structural JSON Schema: it also checks ordinary local paths, reparse points,
loopback identity, secret-like content, cross-field relationships, Core compatibility,
and the presence of an explicit business assertion.

The generated `.veritrail/` directory is local authoring state. Keep the whole
directory out of source control: it contains absolute subject facts and local tool
bindings. Copying it into a Bundle or treating it as a sealed contract is unsupported.

The normative preset contracts are
[`docs/59-starter-single-webapp-contract.md`](../docs/59-starter-single-webapp-contract.md)
and [`docs/66-starter-static-site-contract.md`](../docs/66-starter-static-site-contract.md).
Release packaging and readback are governed by
[`docs/63-entry-layer-e1-release-contract.md`](../docs/63-entry-layer-e1-release-contract.md).
