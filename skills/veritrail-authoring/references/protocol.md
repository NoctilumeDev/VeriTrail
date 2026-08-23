# Authoring protocol 0.1

The bundled helper accepts one strict intake object for `candidate` and `draft`:

```json
{
  "schema_version": "0.1",
  "repository_root": "C:\\absolute\\subject",
  "topology": {
    "managed_nodes": 1,
    "uses_shell": false,
    "uses_container_or_vm": false,
    "uses_remote_dependency": false,
    "requires_secret": false,
    "loopback_only": true
  },
  "answers": {
    "schema_version": "0.1",
    "preset": "single-webapp",
    "workspace_id": "explicit-id",
    "question": "Explicit acceptance question",
    "subject": {},
    "application": {},
    "browser": {},
    "budgets": {},
    "timeouts": {},
    "random_seed": 0
  }
}
```

`answers` must satisfy the packaged Starter Answers 0.1 schema and runtime validation. The
helper does not add defaults. In particular, the user must explicitly confirm:

- the ordinary absolute subject root and trusted local `.exe`;
- structured arguments, working directory, and watch roots;
- one fixed IPv4 loopback port and health path;
- the browser start URL and same allowed origin;
- exactly one desktop and one mobile viewport;
- at least one decisive `expect_visible` or `expect_text` business check;
- screenshot safety acknowledgement;
- every budget, timeout, and the random seed.

The helper emits exactly one canonical JSON object. States are limited to:

- `NEEDS_USER_INPUT`
- `NO_MATCHING_PRESET`
- `STARTER_VERSION_UNSUPPORTED`
- `STARTER_VALIDATION_FAILED`
- `CANDIDATE_READY`
- `DRAFT_READY_FOR_HUMAN_REVIEW`

No state is a product Verdict. Candidate output may contain normalized Answers only after
Starter validation has rejected secret-like content and unsafe paths. `draft` creates only a
Starter-owned `.veritrail` workspace, validates it, requests the deterministic human review,
and stops.

## Explicit unsupported topology

Return `NO_MATCHING_PRESET` without generating Profile or Plan when any confirmation says:

- managed node count is not exactly one;
- shell or script-host execution is required;
- a container, VM, WSL, or remote execution is required;
- a remote dependency or database is required;
- a secret is required;
- traffic cannot remain on explicit IPv4 loopback.

Repository markers such as a Compose filename are only `OBSERVED` candidates. They never
become topology facts until the user confirms whether the supported path depends on them.
