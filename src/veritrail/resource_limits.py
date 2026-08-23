from __future__ import annotations


# These ceilings are part of the public bundle boundary. They are deliberately
# independent from a caller-authored Plan so an untrusted Plan cannot expand
# the verifier's memory, file-count, or retained-output budget.
MAX_ARTIFACT_BYTES = 10 * 1024 * 1024
MAX_BUNDLE_FILES = 256
MAX_BUNDLE_BYTES = 64 * 1024 * 1024

# Reserve room for sealed-plan.json, sealed-profile.json, evidence-manifest.json,
# report.json, report.md, and bundle-manifest.json. A bundle without a profile
# simply retains one unused slot.
MAX_EVIDENCE_COMPONENT_FILES = MAX_BUNDLE_FILES - 6
