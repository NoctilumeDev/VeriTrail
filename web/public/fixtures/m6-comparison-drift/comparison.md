# VeriTrail Rerun Comparison

- Comparison: `cmp_b360d395a4e2a592761f22d4`
- Rule: `rerun-semantic/0.1`
- Status: **DRIFT**
- Comparable: `true`

## Sources

- Baseline: `m6-minimal-pass-20260809` — `COMPLETED` / `PASS`
- Repeat: `m6-minimal-fail-20260809` — `COMPLETED` / `FAIL`
- Plan: `m0-fixture-pass` / `90235a18c59e9f30cd2aa519d281a4fdb18f04e83bdf2fcc5ff98770dba8a2b8`

## Reasons

- `RERUN_SEMANTIC_DRIFT` — 冻结语义投影存在 7 处差异。

## Differences

- `/assertions/suite-completed-successfully/actual` — baseline `true`; repeat `false`
- `/assertions/suite-completed-successfully/status` — baseline `"PASS"`; repeat `"FAIL"`
- `/assertions/suite-has-zero-failures/actual` — baseline `0`; repeat `1`
- `/assertions/suite-has-zero-failures/status` — baseline `"PASS"`; repeat `"FAIL"`
- `/evidence_shape` — baseline `[{"attachments":[],"evidence_type":"automated.test-summary","parser_version":"evidence-json/0.1","redacted":true,"redacted_fields":1,"redaction_rule_version":"privacy/0.1","retention":"local-default","source":"VeriTrail deterministic fixture"}]`; repeat `[{"attachments":[],"evidence_type":"automated.test-summary","parser_version":"evidence-json/0.1","redacted":false,"redacted_fields":0,"redaction_rule_version":"privacy/0.1","retention":"local-default","source":"VeriTrail deterministic failure fixture"}]`
- `/reason_codes` — baseline `["ALL_DECISIVE_ASSERTIONS_PASSED"]`; repeat `["DECISIVE_ASSERTION_FAILED"]`
- `/verdict` — baseline `"PASS"`; repeat `"FAIL"`

## Boundary

- MATCH 表示 M6 冻结语义投影一致，不等于来源 Run 的 Verdict 为 PASS。
- 本比较不支持不同 Plan 的处理组因果归因。
- 未进入 sealed assertion 或 Evidence 形态的原始业务事实不在本结论范围内。
