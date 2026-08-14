# Gate A single-application example

This target-neutral fixture exercises the M11 `SINGLE_APPLICATION` contract without
using any selected real target's content or project-specific behavior.

- `profile-positive.json` starts one owned loopback HTTP application.
- The three failure Profiles select early exit, readiness timeout, and owner mismatch
  through structured arguments to the same helper.
- `plan-positive.json` is the public base Plan. `authority-set.json` preregisters
  the Browser-negative and lifecycle-failure Plan identities, exact Profile, and
  expected sealed digests.
- Each generated Plan authority binds exactly one sealed Profile identity.
- `tool-bindings.json` is intentionally not committed because its Python executable
  path is machine-local. Create it with one `python-application` binding.

The committed Profiles and Plans are drafts. Seal each Profile first, verify that its
digest matches the corresponding Plan reference, then seal the Plan before running.
