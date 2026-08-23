# VeriTrail Starter 0.1

`veritrail-starter` is the independent, fail-closed DRAFT authoring entry for
VeriTrail Core 0.12.x. The first development slice supports only the frozen
`single-webapp` preset on Windows 11.

It can inspect explicit answers, create deterministic unsealed Profile/Plan drafts,
validate a local authoring workspace, and print a manual Core handoff. It never seals,
runs, approves a Preview, or decides a Verdict.

## Development usage

```powershell
python -m pip install --editable .
python -m pip install --editable .\starter
veritrail-starter doctor --answers C:\absolute\path\answers.json
veritrail-starter init --preset single-webapp --answers C:\absolute\path\answers.json
veritrail-starter validate --workspace C:\absolute\subject\.veritrail
veritrail-starter review --workspace C:\absolute\subject\.veritrail
veritrail-starter handoff --workspace C:\absolute\subject\.veritrail
```

Every command writes exactly one versioned JSON result to stdout. `handoff` validates
the DRAFT and points at a PowerShell file that only **prints** manual Core commands.
It does not execute those commands.

The input contract is packaged at
`veritrail_starter/schemas/answers-0.1.schema.json`. Runtime validation is stricter
than the structural JSON Schema: it also checks ordinary local paths, reparse points,
loopback identity, secret-like content, cross-field relationships, Core compatibility,
and the presence of an explicit business assertion.

The generated `.veritrail/` directory is local authoring state. Keep the whole
directory out of source control: it contains absolute subject facts and local tool
bindings. Copying it into a Bundle or treating it as a sealed contract is unsupported.

The normative contract is
[`docs/59-starter-single-webapp-contract.md`](../docs/59-starter-single-webapp-contract.md).
