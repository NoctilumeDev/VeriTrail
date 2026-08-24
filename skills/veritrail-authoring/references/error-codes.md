# Starter error interpretation

Preserve every code exactly as returned by Starter.

| Starter code/status | Skill state | Meaning |
| --- | --- | --- |
| doctor `NEEDS_INPUT` | `NEEDS_USER_INPUT` | Authoring or host facts are incomplete; do not repair automatically. |
| doctor `UNSUPPORTED` | `NO_MATCHING_PRESET` | The frozen preset does not cover this host or topology. |
| `INVALID_INPUT` | `STARTER_VALIDATION_FAILED` | The explicit candidate violates its selected Answers contract. |
| `OUTPUT_CONFLICT` | `STARTER_VALIDATION_FAILED` | `.veritrail` already exists; never overwrite or merge it. |
| `UNSUPPORTED` | `STARTER_VALIDATION_FAILED` | Starter rejected a concrete Answers candidate as outside the preset. |
| `CORE_INCOMPATIBLE` | `STARTER_VERSION_UNSUPPORTED` | Stop; do not attempt migration or fallback. |
| `NEEDS_INPUT` | `NEEDS_USER_INPUT` | Ask only for the missing explicit facts. |
| `WORKSPACE_INVALID` | `STARTER_VALIDATION_FAILED` | Do not repair in place; preserve the workspace for review. |
| `ENVIRONMENT_NOT_READY` | `NEEDS_USER_INPUT` | Report the missing environment fact without installing or changing the host. |
| unknown output/version | `STARTER_VERSION_UNSUPPORTED` | Fail closed; the Skill knows only its pinned Starter 0.2 and authoring protocol. |

Never convert one of these states into Core `PASS`, `FAIL`, `PENDING`, or `INCONCLUSIVE`.
