# VeriTrail GitHub Evidence Plugin

This package is the independent P1 Structured GitHub API Collector. It derives a
sealed, read-only observation request from a VeriTrail `AcceptancePlan 0.1`,
collects only the selected GitHub REST projections, normalizes source facts, and
emits standard VeriTrail `Evidence 0.1`.

The package does not modify GitHub, evaluate acceptance assertions, collect
browser-rendered content, or import VeriTrail private implementation symbols.

See the repository-level P1 contract before using or changing this package:
[`docs/83-p1-structured-github-api-collector-contract.md`](../../docs/83-p1-structured-github-api-collector-contract.md).

## Reference vertical slice

Install Core and the plugin from the repository, then collect the immutable
public reference coordinate:

```powershell
python -m pip install --editable ../..
python -m pip install --editable .
veritrail-github-collect `
  --plan examples/acceptance-plan.json `
  --observation-spec-id github-api `
  --request-id reference-001 `
  --output github-evidence.json
```

The optional credential is read only from `VERITRAIL_GITHUB_TOKEN` at runtime;
there is intentionally no token command-line option. Anonymous collection is
the default. The resulting file is standard `Evidence 0.1`; VeriTrail Core,
not this plugin, owns assertion evaluation and the final Verdict.
