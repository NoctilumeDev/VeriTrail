# VeriTrail GitHub Evidence Plugin

This package contains independently bounded, read-only capabilities:

- the base P1 Structured GitHub API Collector; and
- the optional P2 GitHub Public Render Collector; and
- the offline P3 handoff manifest contract, create-new publisher, and exact
  snapshot verifier.

Both derive sealed observation requests from a VeriTrail `AcceptancePlan 0.1`,
retain source-specific facts, and emit separate standard VeriTrail
`Evidence 0.1` artifacts. P1 reads selected GitHub REST projections. P2 observes
fixed public GitHub render surfaces through an explicitly installed, matching
Chromium runtime.

The P3 manifest remains a thin artifact-selection boundary. Its publisher
retains paired side outcomes without copying Plan, session, coverage, facts, or
Verdict-like fields. Its verifier safely imports each selected Evidence file
once, checks the canonical Evidence digest and collector role, and returns those
same Core-owned `ImportedEvidence` snapshots. It does not interpret Plan/spec
binding, session integrity, coverage, assertions, or Verdict.

The package does not modify GitHub, evaluate acceptance assertions, join P1 and
P2 facts, or import VeriTrail private implementation symbols. VeriTrail Core,
not either Collector, owns sufficiency, cross-Evidence integrity, assertions,
and the final Verdict.

See the repository-level contracts before using or changing these capabilities:

- [`docs/83-p1-structured-github-api-collector-contract.md`](../../docs/83-p1-structured-github-api-collector-contract.md)
- [`docs/89-p2-public-render-collector-contract.md`](../../docs/89-p2-public-render-collector-contract.md)
- [`docs/92-p3-core-handoff-contract.md`](../../docs/92-p3-core-handoff-contract.md)

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
there is intentionally no token command-line option. Anonymous P1 collection is
the default.

P1 remains the base installation and does not require a browser dependency.
The P2 public-render capability is installed explicitly with the `render`
extra:

```powershell
python -m pip install ".[render]"
python -m playwright install chromium
```

Importing the package and running the P1 collector or CLI must continue to work
when Playwright is absent. Installing the extra does not install Chromium as a
Collector side effect: the operator or build pipeline must preinstall the exact
bundled browser before collection. P2 loads Playwright only inside its own
capability boundary, never downloads a browser at runtime, and never falls back
to a system browser.

P2 is intentionally imported from its explicit capability modules rather than
the browser-free P1/P3-contract top-level package surface:

```python
from pathlib import Path

from veritrail_github.public_render_collector import PublicRenderCollector
from veritrail_github.public_render_contracts import derive_public_render_request
from veritrail_github.publisher import publish_evidence

request = derive_public_render_request(
    plan,
    "github-public-readme",
    "render-request-001",
)
result = PublicRenderCollector().collect(plan, request)
publish_evidence(Path("github-render-evidence.json"), result.artifact)
```

The thin paired coordinator can give one P1 and one P2 collection a shared,
plugin-created session identity and fixed P1-then-P2 order. It still publishes
two Evidence files and never turns correlation into an atomic-snapshot claim.
