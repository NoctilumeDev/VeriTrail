# GitHub Evidence state-bound authority maintenance contract

> Status: `CONTRACT_FROZEN / IMPLEMENTED / NOT_A_RELEASE_CLAIM`
>
> Baseline: `main@5892908cdd2a47cf89d10ea2f0504c1af6c6d70b`
>
> Impact: `L2_CONTRACT + L3_SYSTEM`; GitHub Evidence only. Core, Review Attention,
> Workbench, Verdict semantics, and the published `github-evidence-v0.1.0` artifacts do
> not change.

## 1. Trigger and retained observations

This maintenance is driven by real GitHub observations, not a hypothetical schema
extension:

- PR `#153` is merged. Under REST API version `2026-03-10`, its pull-request payload no
  longer contains `merge_commit_sha`; the existing normalizer converted the missing
  field to `null` while reporting `coverage=COMPLETE`.
- The same PR timeline contains one explicit `merged` event, event
  `31473900287`, whose `commit_id` is
  `5892908cdd2a47cf89d10ea2f0504c1af6c6d70b`.
- workflow run `35457915755` has two attempts on the same source SHA. Attempt 1 contains
  one failed job and attempt 2 is successful. `check-runs?filter=all` returns 22 Check
  Runs from both attempts under the same Check Suite.
- the run's eight retained Actions artifacts were created during attempt 1. The artifact
  API binds each artifact to the workflow run and head SHA, but does not identify the
  producer job or attempt. The mutable workflow-run resource now reports attempt 2.

These observations establish four separate identities:

```text
commit-associated Check Run
!= GitHub Actions workflow run
!= workflow run attempt
!= Actions artifact producer
```

## 2. Existing protections that remain correct

The current plugin already requires an exact lowercase commit SHA in the sealed
observation spec. Evidence binds the exact Plan digest and observation-spec digest.
An Evidence artifact collected for one target SHA cannot satisfy a Plan for another SHA;
the real cross-Plan check remains `INCONCLUSIVE`.

The pull-request projection also retains head SHA, base SHA, merged state, and merge
coordinate separately. A branch name, PR display state, Check display name, or current
repository head never substitutes for the exact target commit.

## 3. Corrective contract

### 3.1 Merged PR identity

For `pull_request.merge` under API `2026-03-10`:

1. the pull-request payload remains authoritative for PR number, state, `merged`,
   `merged_at`, head SHA, and base SHA;
2. when `merged=true`, the collector must additionally read the bounded PR timeline;
3. exactly one `merged` timeline event owns `merge_commit_sha`, event ID, and event
   observation time;
4. zero or multiple merged-event candidates retain a cardinality conflict and make
   coverage non-complete;
5. a missing pull-request response field must never be represented as an observed
   nullable merge commit;
6. the target commit, PR head, and final merge commit remain descriptive coordinates.
   The plugin does not invent a Verdict-like relation among them.

### 3.2 Check Run identity

`checks.observed_runs` remains a commit-scoped observation of Check API objects. Each
Check Run must retain, when available:

- exact Check Run ID and Check Suite ID;
- producer app ID and slug;
- external ID;
- a bounded credential-free HTTPS details URL, with query and fragment removed and an
  explicit redaction marker;
- GitHub Actions workflow-run and job IDs only when mechanically derivable from an exact
  repository-matching GitHub Actions details path.

The historical `run_id` and `suite_id` fields remain readable aliases for existing 0.1
consumers, but they identify Check API objects. They do not identify a GitHub Actions
workflow run or attempt.

The Check Runs endpoint does not expose `run_attempt`. The normalized GitHub Actions
coordinate therefore records `run_attempt=null`. It must not infer the attempt from
timestamps, list order, Check Run IDs, the current workflow-run resource, or a successful
rerun.

### 3.3 Explicit non-claims

This patch does not add workflow-run, attempt-specific job, or Actions-artifact
projections. It does not claim:

```text
22 Check Runs on one SHA == one coherent workflow attempt
artifact.workflow_run.head_sha == artifact bytes were built only from that SHA
current workflow run attempt == artifact producer attempt
workflow run association == producer job identity
```

Those capabilities require a separate exact-coordinate contract. At minimum, an
attempt-aware request would bind both `workflow_run_id` and `run_attempt` and use the
attempt-specific jobs endpoint. Actions artifacts must remain run-associated with
producer attempt/job explicitly unavailable unless GitHub or a separately verified
provenance artifact supplies that relation.

## 4. Version and compatibility

The normalized fact projection changes, so
`normalization_semantics_version` advances from `github-rest-facts/0.2` to
`github-rest-facts/0.3`. The source distribution becomes `0.1.1.dev0`; the immutable
published `0.1.0` tag, Release, wheels, checksums, and historical Evidence remain
unchanged and readable.

## 5. Acceptance matrix

The implementation candidate must prove:

1. a merged PR without `merge_commit_sha` in its PR payload obtains the exact commit from
   one timeline merged event;
2. zero or multiple merged events retain facts but yield `PARTIAL` coverage;
3. an unmerged PR does not require a timeline probe and retains no merge identity;
4. Check Run and Check Suite identities are explicit while legacy aliases remain equal;
5. query/fragment material in a details URL is not persisted;
6. GitHub Actions run/job IDs are derived only from a matching GitHub repository path,
   and attempt remains unknown;
7. the real PR `#153` projection is `COMPLETE` and resolves the final merge commit;
8. the real rerun commit retains both attempts' Check Runs without claiming an attempt;
9. plugin tests pass on Python 3.10 and 3.13 in normal and optimized mode;
10. Core, Workbench, Browser Smoke, wheel-only installation, and the immutable 0.1.0
    release-asset verification remain unchanged.

The patch stops here. It does not create an Actions provenance subsystem, attestations,
GraphQL collection, mutable-branch selection, GitHub writes, a new Release, or a new Core
operator.
