# Authoring protocol 0.1

The bundled helper accepts one strict outer intake object for `candidate` and `draft`.
The authoring protocol remains `0.1`; the nested Answers object selects its own frozen
contract:

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
    "schema_version": "0.2",
    "preset": "static-site",
    "workspace_id": "explicit-id",
    "question": "Explicit acceptance question",
    "subject": {},
    "static_site": {},
    "browser": {},
    "budgets": {},
    "timeouts": {},
    "random_seed": 0
  }
}
```

The supported combinations are:

| Answers | Preset | Runtime block |
| --- | --- | --- |
| `0.1` or `0.2` | `single-webapp` | `application` |
| `0.2` | `static-site` | `static_site` |

`answers` must satisfy its packaged Starter schema and runtime validation. The helper does
not add defaults. For both presets, the user must explicitly confirm:

- the ordinary absolute subject root, working directory, and watch roots;
- one fixed IPv4 loopback port and an existing trusted local `.exe`;
- the browser start URL and same allowed origin;
- exactly one desktop and one mobile viewport;
- at least one decisive `expect_visible` or `expect_text` business check;
- screenshot safety acknowledgement;
- every budget, timeout, and the random seed.

`single-webapp` additionally requires structured application arguments, health path, and
expected status. `static-site` additionally requires an existing ordinary `.htm`/`.html`
entry file inside the working directory, a CPython console executable, expected status 200,
and explicit `requires_build = false` and `requires_remote_assets = false`. The Starter then
derives the fixed `python -m http.server <port> --bind 127.0.0.1` argument vector; neither the
Skill nor the user may add a repository command or build step.

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
A build marker prevents the inspector from recommending `static-site`; it does not prove
that `single-webapp` is supported. If the bounded filename scan is incomplete, the inspector
returns no preset candidate and asks the user to narrow the repository root or explicitly
confirm the complete supported topology. A capped public-filename list never suppresses the
separate build-marker fact.

Starter subprocess output is accepted only when the frozen JSON `outcome` agrees with the
process exit code (`OK`/zero or `ERROR`/nonzero). Any disagreement is an unsupported protocol,
not a successful authoring result.
