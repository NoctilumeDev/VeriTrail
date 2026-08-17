# VeriTrail Paired Counterfactual Analysis

- Analysis: `pair_a24d66ea58300514d61fe531`
- Pairing plan: `m7-forced-failure-counterfactual` / `5ec3936f8c4448c9960b5bc078306ca627eaad1381a88ae8ae9e07fca8bcadf0`
- Rule: `paired-counterfactual/0.1`
- Status: **SUPPORTED**
- Attributable: `true`

## Sources

- BASELINE: `m7-paired-baseline-20260809` — `COMPLETED` / `PASS` — primary `"nominal"`
- TREATMENT: `m7-paired-treatment-20260809` — `COMPLETED` / `FAIL` — primary `"forced_failure"`
- RESTORED_BASELINE: `m7-paired-restored-20260809` — `COMPLETED` / `PASS` — primary `"nominal"`
- NEGATIVE_CONTROL: `m7-paired-negative-control-20260809` — `COMPLETED` / `PASS` — primary `"negative_control"`

## Reasons

- `PAIRED_EFFECT_SUPPORTED` — 处理效果出现、恢复后消失且负对照未复制该效果。

## Outcomes

### `suite-completed-successfully`

- BASELINE: expected `true`; actual `true`; match `true`
- TREATMENT: expected `false`; actual `false`; match `true`
- RESTORED_BASELINE: expected `true`; actual `true`; match `true`
- NEGATIVE_CONTROL: expected `true`; actual `true`; match `true`

### `suite-has-zero-failures`

- BASELINE: expected `0`; actual `0`; match `true`
- TREATMENT: expected `1`; actual `1`; match `true`
- RESTORED_BASELINE: expected `0`; actual `0`; match `true`
- NEGATIVE_CONTROL: expected `0`; actual `0`; match `true`

## Unplanned assertion drift

- None.

## Boundary

- SUPPORTED applies only to the four immutable Runs and exact sealed Plans named by this PairingPlan.
- PairedAnalysis does not replace any source Run Verdict.
- PairingPlan 0.1 does not provide statistical significance or repeated-run aggregation.
