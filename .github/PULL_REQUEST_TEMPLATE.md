## Intent

Describe the single user-visible problem this pull request closes. Link the reproducible issue or contract.

## Scope and boundaries

- Change level: `L0_DOCS` / `L1_COMPONENT` / `L2_CONTRACT` / `L3_SYSTEM`
- Affected owners and consumers:
- Explicit non-goals:
- Frozen contracts, tags, and release coordinates that remain unchanged:

## Executable evidence

List the exact commands and real acceptance paths you ran. Distinguish automated checks from browser,
process, packaging, release-download, or other end-to-end evidence.

```text
command -> observed result
```

## Negative and boundary behavior

Describe at least one relevant failure, rejection, cleanup, resource, trust, or unsupported-path check. If no
such check applies, explain why.

## Public contract and compatibility

State whether README, START_HERE, schemas, CLI help, examples, CI, SECURITY, release notes, or public metadata
changed. Explain any versioning consequence. Do not reinterpret immutable evidence from an older release.

## Checklist

- [ ] This pull request has one coherent intent.
- [ ] I ran the repository-declared gates for every changed layer and recorded the results above.
- [ ] I added or updated deterministic regression coverage when behavior changed.
- [ ] I checked the relevant negative and boundary paths.
- [ ] I performed real browser/process/package/release acceptance when automated tests alone were insufficient.
- [ ] Public documentation and version coordinates match the executable facts.
- [ ] No secret, personal data, machine-specific path, unredacted trace, or generated runtime artifact is committed.
- [ ] The change does not silently broaden Core, Starter, Authoring Skill, Workbench, or Verdict authority.
