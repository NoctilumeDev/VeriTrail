# VeriTrail run `m2-freeze-pass`

- Execution status: `COMPLETED`
- Verdict: `PASS`
- Plan: `m2-browser-smoke@1`
- Plan SHA-256: `2a16769446e4eb617ab4fdd51b7b1eda9c7266654d5a991106416c9488c91fd7`
- Baseline: `m2-browser-fixture-baseline` (`VALID`)
- Random seed: `20260809`
- Created at: `2026-08-08T23:12:33.906696Z`

## Reasons

- `ALL_DECISIVE_ASSERTIONS_PASSED` — "All required evidence is present and every decisive assertion passed."

## Assertions

| ID | Severity | Status | Actual | Expected |
| --- | --- | --- | --- | --- |
| "preflight-complete" | HARD | PASS | true | true |
| "browser-capture-complete" | HARD | PASS | true | true |
| "browser-steps-pass" | HARD | PASS | true | true |
| "console-errors-zero" | HARD | PASS | 0 | 0 |
| "page-errors-zero" | HARD | PASS | 0 | 0 |
| "failed-requests-zero" | HARD | PASS | 0 | 0 |
| "http-errors-zero" | HARD | PASS | 0 | 0 |
| "duplicate-writes-zero" | HARD | PASS | 0 | 0 |
| "horizontal-overflow-zero" | HARD | PASS | 0 | 0 |
| "viewport-coverage" | HARD | PASS | 2 | 2 |
| "screenshot-coverage" | HARD | PASS | 2 | 2 |

## Evidence

- `runtime.preflight` — `2bef4e2dfd14904a2635aff4b2ba8de6571f00fedfd38f180b747796174920aa` (2086 bytes, redactions: 0, decision: PROCEED)
- `browser.session` — `6cc89b89e25007cbb06f91531ee509fd6d049cb6ae0b677e53ec31d7e3eefcb3` (6140 bytes, redactions: 0, attachments: 2)

## Evidence gaps and contamination

- None detected by the active deterministic rule set.

## Applicability boundary

- Subject: `{"id": "veritrail-browser-fixture", "source_ref": "examples/browser/site", "version": "healthy-1"}`
- Primary variable: `{"name": "fixture_variant", "role": "PRIMARY", "source": "sealed-plan", "value": "healthy"}`
- Load model: `{"in_flight_requests": 1, "virtual_users": 1}`
- Resource budget: `{"max_artifact_bytes": 5242880}`
- Change scope: `{"consumers": ["plan-validator", "browser-adapter", "artifact-store", "verdict-engine", "json-report", "markdown-report"], "expected_blast_radius": "Plan 0.3, browser.session evidence, attachment manifests, CLI and reports", "level": "L2_CONTRACT", "owner": "VeriTrail Core / Browser Adapter"}`

## Reproduction and cleanup

1. "Serve examples/browser/site on loopback port 18765."
2. "Run browser-capture with this sealed plan and a unique Run ID."
3. "Verify both viewport timelines, browser facts, screenshots and manifests."

Cleanup:

1. "Close the Playwright browser and every context."
2. "Stop the loopback fixture server and verify port 18765 is released."
3. "Verify no .veritrail-* staging directory remains."
