# VeriTrail run `m2-freeze-negative`

- Execution status: `COMPLETED`
- Verdict: `FAIL`
- Plan: `m2-browser-negative@1`
- Plan SHA-256: `2c4c2d27347b86eefc25f892f633fb73a89a2633d13c8339b29fe0f753ce246f`
- Baseline: `m2-browser-negative-baseline` (`VALID`)
- Random seed: `20260809`
- Created at: `2026-08-08T23:12:36.275467Z`

## Reasons

- `DECISIVE_ASSERTION_FAILED` — "3 hard or degradation-boundary assertion(s) failed."

## Assertions

| ID | Severity | Status | Actual | Expected |
| --- | --- | --- | --- | --- |
| "preflight-complete" | HARD | PASS | true | true |
| "browser-capture-complete" | HARD | PASS | true | true |
| "console-errors-zero" | HARD | FAIL | 4 | 0 |
| "page-errors-zero" | HARD | FAIL | 2 | 0 |
| "http-errors-zero" | HARD | FAIL | 2 | 0 |

## Evidence

- `runtime.preflight` — `f8072726b55f818d12f720b6ce291e673b0ae7b811ef3d048c4d2e6188ff229c` (2086 bytes, redactions: 0, decision: PROCEED)
- `browser.session` — `1c2983e17d525b3679f9ae89d96e2fba4eb2da1f52d38f13af7edab2fa6b648a` (5864 bytes, redactions: 0, attachments: 2)

## Evidence gaps and contamination

- None detected by the active deterministic rule set.

## Applicability boundary

- Subject: `{"id": "veritrail-browser-fixture", "source_ref": "examples/browser/site", "version": "negative-1"}`
- Primary variable: `{"name": "fixture_variant", "role": "PRIMARY", "source": "sealed-plan", "value": "negative"}`
- Load model: `{"in_flight_requests": 1, "virtual_users": 1}`
- Resource budget: `{"max_artifact_bytes": 5242880}`
- Change scope: `{"consumers": ["browser-adapter", "verdict-engine", "json-report", "markdown-report"], "expected_blast_radius": "Plan 0.3 browser negative-path evidence and deterministic verdict", "level": "L2_CONTRACT", "owner": "VeriTrail Core / Browser Adapter"}`

## Reproduction and cleanup

1. "Serve examples/browser/site on loopback port 18765."
2. "Run browser-capture with this negative plan and a unique Run ID."
3. "Confirm Console, page, and HTTP failures are present and Verdict is FAIL."

Cleanup:

1. "Close the Playwright browser and every context."
2. "Stop the loopback fixture server and verify port 18765 is released."
3. "Verify no .veritrail-* staging directory remains."
