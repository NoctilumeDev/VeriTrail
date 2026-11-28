"""Private 0.1 owner for one complete Review Attention R1 composition.

This module deliberately has no public package export.  It does not observe
Reality, change sealed obligations, persist a product artifact, or issue a
Core Verdict.  It only owns the one-shot application assembly frozen by the
versioned global-composition contract.
"""

from __future__ import annotations

import copy
import hashlib
import json
import threading
from enum import Enum
from typing import Callable, Mapping, Sequence

from veritrail_review import _derivation_evidence_manifest_carrier_successor as carrier
from veritrail_review import (
    _derivation_evidence_manifest_carrier_conformance as carrier_conformance,
)
from veritrail_review import _fact_fulfillment as fact
from veritrail_review import _fact_relation_transition as transition
from veritrail_review import _negative_world_coverage_authority_recovery as negative
from veritrail_review import _post_terminal_fact_dual_successor as dual
from veritrail_review import _relation_transition_slice_composition as positive
from veritrail_review import _review_derivation_manifest_0_2 as manifest02
from veritrail_review import _review_derivation_manifest_0_2_conformance as manifest_conformance
from veritrail_review import _unified_review_coverage_output_admission as unified
from veritrail_review._execution_cell import DEFAULT_TRANSPORT_LIMITS
from veritrail_review._execution_cell_binding import ProviderBinding
from veritrail_review._execution_cell_protocol import (
    ExecutionCellTransportSafetyLimits,
)
from veritrail_review._fact_fulfillment_binding import closed_fact_bindings
from veritrail_review._parse_fulfillment import OwnedParseFulfillmentClosure
from veritrail_review._review_coverage_ledger_conformance import (
    LEDGER_DIGEST_DOMAIN,
    ROOT_CHAIN_DOMAIN,
)
from veritrail_review.budget import BudgetContext, BudgetState, OwnedPhaseResult
from veritrail_review.canonical import canonical_json_bytes, semantic_digest
from veritrail_review.derivation_input_contracts import DerivationInputSet


AUTHORITY_CONTRACT = "R1_GLOBAL_REVIEW_COMPOSITION_AUTHORITY_0_1"
OWNER_IDENTITY = "veritrail.review.global-composition-owner/0.1"
ATTEMPT_BINDING_FUNCTION = "r1-global-review-attempt-binding/0.1"
COMPOSITION_FUNCTION = "r1-global-review-composition/0.1"
ADMISSION_FUNCTION = "r1-global-review-composition-admission/0.1"
RESULT_IDENTITY = "veritrail.review.global-composition-result/0.1"

_CANDIDATE_IDENTITY = "veritrail.review.global-composition-candidate/0.1"
_CANDIDATE_SEAL_DOMAIN = "veritrail.review.global-composition-candidate-seal/0.1"
_ROSTER_IDENTITY = "veritrail.review.global-composition-provider-roster/0.1"
_CLEANUP_IDENTITY = "veritrail.review.global-composition-cleanup/0.1"
_RESULT_TOKEN = object()
_CANDIDATE_TOKEN = object()

_CONTINUITY_VERSIONS = {
    "contract_function": "r1-same-attempt-derivation-evidence-continuity/0.1",
    "private_continuity_domain": "SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_0_1",
    "binding_identity": "r1-same-attempt-derivation-evidence-continuity-binding/0.1",
    "profile_identity": "r1-same-attempt-derivation-evidence-continuity-profile/0.1",
    "wire_identity": "r1-same-attempt-derivation-evidence-continuity-private-wire/0.1",
    "branch_projection_function": "r1-derivation-evidence-continuity-branch-projection/0.1",
}
_CONTINUITY_AUTHORITY_CEILING = {
    "private_same_attempt_continuity": True,
    "exact_discriminated_one_shot_branch": True,
    "controller_timing_provenance_original_execution_only": True,
    "legacy_evidence_0_2": False,
    "public_evidence_schema": False,
    "manifest": False,
    "persistence": False,
    "public_review": False,
    "core_verdict": False,
    "global_composition_authority": False,
    "r2_r6": False,
}

_NORMAL_ROUTE = "RELATION_HANDOFF"
_NEGATIVE_ROUTE = "FACT_TO_COVERAGE_EXACT_INPUT_SUCCESSOR_0_2"
_NEGATIVE_WORLDS = frozenset(
    {
        "ZERO_PARSE_DENOMINATOR",
        "ALL_PARSE_REJECTED",
        "PROJECTION_BLOCKED",
        "REQUIRED_PROVIDER_NON_SUCCESS",
    }
)
_VERSION_DOCUMENT = {
    "authority_contract": AUTHORITY_CONTRACT,
    "owner_identity": OWNER_IDENTITY,
    "attempt_binding_function": ATTEMPT_BINDING_FUNCTION,
    "composition_function": COMPOSITION_FUNCTION,
    "admission_function": ADMISSION_FUNCTION,
    "result_identity": RESULT_IDENTITY,
}
_INPUT_DIGEST_FIELDS = (
    "source_snapshot_digest",
    "policy_digest",
    "analysis_scope_digest",
    "slice_policy_digest",
    "derivation_profile_digest",
)
_INPUT_BYTE_FIELDS = (
    "source_snapshot_canonical_bytes",
    "review_policy_canonical_bytes",
    "derivation_profile_canonical_bytes",
)


class GlobalCompositionState(str, Enum):
    BOUND = "BOUND"
    RUNNING = "RUNNING"
    CANDIDATE_READY = "CANDIDATE_READY"
    ADMITTED = "ADMITTED"
    REVOKED = "REVOKED"


class GlobalCompositionFailureFamily(str, Enum):
    VERSION_REJECTED = "GLOBAL_COMPOSITION_VERSION_REJECTED"
    INPUT_BINDING_REJECTED = "GLOBAL_COMPOSITION_INPUT_BINDING_REJECTED"
    PROVIDER_ROSTER_REJECTED = "GLOBAL_COMPOSITION_PROVIDER_ROSTER_REJECTED"
    WORLD_SPLICE_REJECTED = "GLOBAL_COMPOSITION_WORLD_SPLICE_REJECTED"
    PARTIAL_RESULT_REJECTED = "GLOBAL_COMPOSITION_PARTIAL_RESULT_REJECTED"
    LATE_MUTATION_REJECTED = "GLOBAL_COMPOSITION_LATE_MUTATION_REJECTED"
    FOREIGN_CONTEXT_REJECTED = "GLOBAL_COMPOSITION_FOREIGN_CONTEXT_REJECTED"
    COMPONENT_VERSION_REJECTED = "GLOBAL_COMPOSITION_COMPONENT_VERSION_REJECTED"
    RESOURCE_CLEANUP_FAILED = "GLOBAL_COMPOSITION_RESOURCE_CLEANUP_FAILED"
    REPLAY_REJECTED = "GLOBAL_COMPOSITION_REPLAY_REJECTED"
    ADMISSION_REJECTED = "GLOBAL_COMPOSITION_ADMISSION_REJECTED"


class GlobalReviewCompositionError(RuntimeError):
    """Typed composition-layer refusal retaining the first lower reason."""

    def __init__(
        self,
        failure_family: GlobalCompositionFailureFamily,
        *,
        original_reason: str = "UNKNOWN",
        cleanup_outcome: Mapping[str, object] | None = None,
    ) -> None:
        self.failure_family = failure_family
        self.original_reason = original_reason
        self.__cleanup_bytes = (
            None
            if cleanup_outcome is None
            else canonical_json_bytes(dict(cleanup_outcome))
        )
        super().__init__(f"{failure_family.value}:{original_reason}")

    def cleanup_outcome_copy(self) -> dict[str, object] | None:
        return (
            None
            if self.__cleanup_bytes is None
            else json.loads(self.__cleanup_bytes)
        )


def _lower_reason(exc: BaseException) -> str:
    for name in ("failure_family", "family", "code"):
        value = getattr(exc, name, None)
        if value is None:
            continue
        raw = getattr(value, "value", value)
        if type(raw) is str and raw:
            return raw
    return "UNKNOWN"


def _owned_bytes(value: bytes) -> bytes:
    if type(value) is not bytes:
        raise GlobalReviewCompositionError(
            GlobalCompositionFailureFamily.INPUT_BINDING_REJECTED
        )
    return memoryview(value).tobytes()


def _json_bytes(value: Mapping[str, object]) -> bytes:
    return canonical_json_bytes(copy.deepcopy(dict(value)))


def _input_binding_material(inputs: DerivationInputSet) -> tuple[bytes, ...]:
    if type(inputs) is not DerivationInputSet:
        raise GlobalReviewCompositionError(
            GlobalCompositionFailureFamily.INPUT_BINDING_REJECTED
        )
    try:
        canonical = tuple(_owned_bytes(getattr(inputs, name)) for name in _INPUT_BYTE_FIELDS)
        blobs = inputs.verified_blob_bytes_by_object_identity
        if not isinstance(blobs, Mapping):
            raise ValueError
        copied_blobs = tuple(
            (key, _owned_bytes(value))
            for key, value in sorted(blobs.items())
            if type(key) is str and type(value) is bytes
        )
        if len(copied_blobs) != len(blobs):
            raise ValueError
        digest_values = {name: getattr(inputs, name) for name in _INPUT_DIGEST_FIELDS}
        if any(type(value) is not str or not value for value in digest_values.values()):
            raise ValueError
        documents = (
            inputs.source_snapshot_document_copy(),
            inputs.review_policy_document_copy(),
            inputs.derivation_profile_document_copy(),
        )
        if any(type(document) is not dict for document in documents):
            raise ValueError
    except GlobalReviewCompositionError:
        raise
    except Exception as exc:
        raise GlobalReviewCompositionError(
            GlobalCompositionFailureFamily.INPUT_BINDING_REJECTED,
            original_reason=_lower_reason(exc),
        ) from exc
    binding = {
        "attempt_binding_function": ATTEMPT_BINDING_FUNCTION,
        "canonical": [
            {"field": name, "raw_sha256": hashlib.sha256(raw).hexdigest(), "size_bytes": len(raw)}
            for name, raw in zip(_INPUT_BYTE_FIELDS, canonical)
        ],
        "verified_blobs": [
            {
                "object_identity": key,
                "raw_sha256": hashlib.sha256(raw).hexdigest(),
                "size_bytes": len(raw),
            }
            for key, raw in copied_blobs
        ],
        "digests": digest_values,
        "document_raw_sha256": [
            hashlib.sha256(canonical_json_bytes(document)).hexdigest()
            for document in documents
        ],
    }
    return (_json_bytes(binding), *canonical, *[raw for _, raw in copied_blobs])


def _include_advisory(inputs: DerivationInputSet) -> bool:
    rows = inputs.review_policy_document_copy().get("provider_requirements")
    if not isinstance(rows, list):
        raise GlobalReviewCompositionError(
            GlobalCompositionFailureFamily.INPUT_BINDING_REJECTED
        )
    return any(
        isinstance(row, Mapping)
        and row.get("capability_id") == "python-ast-advisory"
        for row in rows
    )


def _roster_document(
    inputs: DerivationInputSet, bindings: Sequence[ProviderBinding]
) -> dict[str, object]:
    if not isinstance(bindings, Sequence) or isinstance(bindings, (str, bytes)):
        raise GlobalReviewCompositionError(
            GlobalCompositionFailureFamily.PROVIDER_ROSTER_REJECTED
        )
    submitted = tuple(bindings)
    expected = closed_fact_bindings(include_advisory=_include_advisory(inputs))
    if (
        len(submitted) != len(expected)
        or any(type(item) is not ProviderBinding for item in submitted)
        or submitted != expected
    ):
        raise GlobalReviewCompositionError(
            GlobalCompositionFailureFamily.PROVIDER_ROSTER_REJECTED
        )
    return {
        "roster_identity": _ROSTER_IDENTITY,
        "providers": [
            {
                "descriptor": item.descriptor.document(),
                "launch_key": item.launch_key,
            }
            for item in submitted
        ],
    }


def _context_document(context: BudgetContext) -> dict[str, object]:
    if (
        type(context) is not BudgetContext
        or context.state is not BudgetState.RUNNING
        or context.stop_trigger is not None
        or not context.checkpoint()
    ):
        raise GlobalReviewCompositionError(
            GlobalCompositionFailureFamily.FOREIGN_CONTEXT_REJECTED
        )
    limits = context.limits
    return {
        "runtime_identity": id(context),
        "wall_clock_ms": limits.wall_clock_ms,
        "memory_bytes": limits.memory_bytes,
        "artifact_bytes": limits.artifact_bytes,
        "started_at_monotonic": context.started_at_monotonic,
        "execution_deadline_monotonic": context.execution_deadline_monotonic,
        "state": context.state.value,
        "stop_trigger": None,
    }


def _stage(ledger: Mapping[str, object], name: str) -> Mapping[str, object]:
    stages = ledger.get("stages")
    if not isinstance(stages, list):
        raise ValueError
    values = [item for item in stages if isinstance(item, Mapping) and item.get("stage") == name]
    if len(values) != 1:
        raise ValueError
    return values[0]


def _root(ledger: Mapping[str, object], name: str) -> Mapping[str, object]:
    roots = ledger.get("root_bindings")
    if not isinstance(roots, list):
        raise ValueError
    values = [item for item in roots if isinstance(item, Mapping) and item.get("stage") == name]
    if len(values) != 1:
        raise ValueError
    return values[0]


def _producer_world(
    branch: str,
    route: str,
    result_kind: str,
    result_document: Mapping[str, object],
) -> str:
    """Producer-side discriminant; independent admission does not call it."""

    if route == _NEGATIVE_ROUTE:
        if branch not in _NEGATIVE_WORLDS or result_kind != unified.NEGATIVE_RESULT_KIND:
            raise ValueError
        return branch
    if (
        branch != "NORMAL_FULFILLED"
        or route != _NORMAL_ROUTE
        or result_kind != unified.NORMAL_RESULT_KIND
    ):
        raise ValueError
    ledger = result_document.get("coverage_ledger")
    slice_set = result_document.get("review_slice_set")
    if not isinstance(ledger, Mapping):
        raise ValueError
    root = _root(ledger, "REVIEW_SLICE_SET")
    stage = _stage(ledger, "SLICE_DERIVATION")
    terminal = root.get("terminal_branch")
    overall = ledger.get("overall_coverage_status")
    status = stage.get("coverage_status")
    if (
        terminal == "PREDECESSOR_UNKNOWN"
        and root.get("binding_state") == "QUALIFIED_UNKNOWN"
        and slice_set is None
        and overall == "UNKNOWN"
        and status == "UNKNOWN"
    ):
        return "NORMAL_RELATION_CONFLICT"
    if not isinstance(slice_set, Mapping) or not isinstance(slice_set.get("slices"), list):
        raise ValueError
    count = len(slice_set["slices"])
    if terminal == "CLOSED_EMPTY" and count == 0 and overall == status == "COMPLETE":
        return "NORMAL_BRANCH_EMPTY"
    if (
        terminal == "NORMAL_PARTIAL"
        and count > 0
        and overall == status == "PARTIAL"
        and bool(stage.get("frontier"))
    ):
        return "NORMAL_SLICE_PARTIAL"
    if (
        terminal == "NORMAL_CLOSED"
        and count > 0
        and overall == status == "COMPLETE"
        and not stage.get("frontier")
    ):
        return "NORMAL_CONSISTENT"
    raise ValueError


def _independent_world(
    branch: object,
    route: object,
    result_kind: object,
    result_document: Mapping[str, object],
) -> str:
    """Independent world reconstruction from copy-owned exact material."""

    if route == _NEGATIVE_ROUTE:
        if branch not in {
            "ZERO_PARSE_DENOMINATOR",
            "ALL_PARSE_REJECTED",
            "PROJECTION_BLOCKED",
            "REQUIRED_PROVIDER_NON_SUCCESS",
        } or result_kind != "NEGATIVE_WORLD_COVERAGE":
            raise ValueError
        if result_document.get("artifact_kind") != "COVERAGE_LEDGER":
            raise ValueError
        roots = result_document.get("root_bindings")
        if not isinstance(roots, list) or any(
            not isinstance(item, Mapping)
            or item.get("binding_state") != "QUALIFIED_ABSENT"
            for item in roots
        ):
            raise ValueError
        return str(branch)
    if (
        branch != "NORMAL_FULFILLED"
        or route != "RELATION_HANDOFF"
        or result_kind != "NORMAL_REVIEW_SLICE_COVERAGE"
    ):
        raise ValueError
    ledger = result_document.get("coverage_ledger")
    if not isinstance(ledger, Mapping):
        raise ValueError
    roots = ledger.get("root_bindings")
    stages = ledger.get("stages")
    if not isinstance(roots, list) or not isinstance(stages, list):
        raise ValueError
    root_values = [
        item
        for item in roots
        if isinstance(item, Mapping) and item.get("stage") == "REVIEW_SLICE_SET"
    ]
    stage_values = [
        item
        for item in stages
        if isinstance(item, Mapping) and item.get("stage") == "SLICE_DERIVATION"
    ]
    if len(root_values) != 1 or len(stage_values) != 1:
        raise ValueError
    root = root_values[0]
    stage = stage_values[0]
    terminal = root.get("terminal_branch")
    root_state = root.get("binding_state")
    overall = ledger.get("overall_coverage_status")
    stage_status = stage.get("coverage_status")
    slice_set = result_document.get("review_slice_set")
    if (terminal, root_state, overall, stage_status, slice_set) == (
        "PREDECESSOR_UNKNOWN",
        "QUALIFIED_UNKNOWN",
        "UNKNOWN",
        "UNKNOWN",
        None,
    ):
        return "NORMAL_RELATION_CONFLICT"
    if not isinstance(slice_set, Mapping):
        raise ValueError
    members = slice_set.get("slices")
    if not isinstance(members, list):
        raise ValueError
    if (terminal, root_state, overall, stage_status, len(members)) == (
        "CLOSED_EMPTY",
        "ARTIFACT_PRESENT",
        "COMPLETE",
        "COMPLETE",
        0,
    ):
        return "NORMAL_BRANCH_EMPTY"
    if (
        terminal == "NORMAL_PARTIAL"
        and root_state == "ARTIFACT_PRESENT"
        and overall == stage_status == "PARTIAL"
        and len(members) > 0
        and isinstance(stage.get("frontier"), list)
        and len(stage["frontier"]) > 0
    ):
        return "NORMAL_SLICE_PARTIAL"
    if (
        terminal == "NORMAL_CLOSED"
        and root_state == "ARTIFACT_PRESENT"
        and overall == stage_status == "COMPLETE"
        and len(members) > 0
        and stage.get("frontier") == []
    ):
        return "NORMAL_CONSISTENT"
    raise ValueError


def _validate_ledger_digests(ledger: Mapping[str, object]) -> None:
    unsigned = copy.deepcopy(dict(ledger))
    actual = unsigned.pop("coverage_ledger_digest", None)
    if actual != semantic_digest(LEDGER_DIGEST_DOMAIN, unsigned):
        raise ValueError
    root_payload = {
        "root_binding_function": ledger.get("root_binding_function"),
        "root_chain_domain": ledger.get("root_chain_domain"),
        "root_bindings": copy.deepcopy(ledger.get("root_bindings")),
    }
    if (
        root_payload["root_chain_domain"] != ROOT_CHAIN_DOMAIN
        or ledger.get("root_chain_digest")
        != semantic_digest(ROOT_CHAIN_DOMAIN, root_payload)
    ):
        raise ValueError
    stages = ledger.get("stages")
    if not isinstance(stages, list):
        raise ValueError
    statuses = [item.get("coverage_status") for item in stages if isinstance(item, Mapping)]
    if len(statuses) != len(stages):
        raise ValueError
    overall = (
        "UNKNOWN"
        if "UNKNOWN" in statuses
        else "PARTIAL"
        if "PARTIAL" in statuses
        else "COMPLETE"
    )
    if ledger.get("overall_coverage_status") != overall:
        raise ValueError


class _GlobalCompositionCandidate:
    def __init__(
        self,
        *,
        owner: "BoundGlobalReviewCompositionAuthority",
        versions: Mapping[str, object],
        input_binding_bytes: bytes,
        input_raw: tuple[bytes, ...],
        roster_bytes: bytes,
        context_bytes: bytes,
        context: BudgetContext,
        branch: str,
        route: str,
        result_kind: str,
        declared_world: str,
        continuity_bytes: bytes,
        result_bytes: bytes,
        carrier_input: Mapping[str, object],
        carrier_validation: Mapping[str, object],
        carrier_candidate_digest: str,
        carrier_admission_digest: str,
        manifest_validation: Mapping[str, object],
        manifest_admission_digest: str,
        manifest_bytes: bytes,
        staging_receipt: Mapping[str, object],
        cleanup_outcome: Mapping[str, object],
        terminal_phase: OwnedPhaseResult,
        admitted_manifest: manifest02.AdmittedReviewDerivationManifest02,
        _token: object,
    ) -> None:
        if _token is not _CANDIDATE_TOKEN:
            raise GlobalReviewCompositionError(
                GlobalCompositionFailureFamily.ADMISSION_REJECTED
            )
        self.__lock = threading.Lock()
        self.__state = "PENDING"
        self.__owner = owner
        self.__bound_owner = owner
        self.__versions_bytes = _json_bytes(versions)
        self.__bound_versions_bytes = self.__versions_bytes
        self.__input_binding_bytes = _owned_bytes(input_binding_bytes)
        self.__bound_input_binding_bytes = self.__input_binding_bytes
        self.__input_raw = tuple(_owned_bytes(value) for value in input_raw)
        self.__bound_input_raw = self.__input_raw
        self.__roster_bytes = _owned_bytes(roster_bytes)
        self.__bound_roster_bytes = self.__roster_bytes
        self.__context_bytes = _owned_bytes(context_bytes)
        self.__bound_context_bytes = self.__context_bytes
        self.__context = context
        self.__bound_context = context
        self.__branch = branch
        self.__route = route
        self.__result_kind = result_kind
        self.__declared_world = declared_world
        self.__continuity_bytes = _owned_bytes(continuity_bytes)
        self.__bound_continuity_bytes = self.__continuity_bytes
        self.__result_bytes = _owned_bytes(result_bytes)
        self.__bound_result_bytes = self.__result_bytes
        self.__carrier_input = _copy_carrier_input(carrier_input)
        self.__bound_carrier_input = self.__carrier_input
        self.__carrier_validation_bytes = _json_bytes(carrier_validation)
        self.__carrier_candidate_digest = carrier_candidate_digest
        self.__carrier_admission_digest = carrier_admission_digest
        self.__manifest_validation_bytes = _json_bytes(manifest_validation)
        self.__manifest_admission_digest = manifest_admission_digest
        self.__manifest_bytes = _owned_bytes(manifest_bytes)
        self.__bound_manifest_bytes = self.__manifest_bytes
        self.__staging_receipt_bytes = _json_bytes(staging_receipt)
        self.__cleanup_bytes = _json_bytes(cleanup_outcome)
        self.__terminal_phase = terminal_phase
        self.__bound_terminal_phase = terminal_phase
        self.__admitted_manifest = admitted_manifest
        self.__bound_admitted_manifest = admitted_manifest
        self.__seal = self.__snapshot_seal()
        self.__bound_seal = self.__seal

    def __copy__(self):
        raise GlobalReviewCompositionError(
            GlobalCompositionFailureFamily.LATE_MUTATION_REJECTED
        )

    def __deepcopy__(self, _memo):
        return self.__copy__()

    def __reduce__(self):
        return self.__copy__()

    def __reduce_ex__(self, _protocol):
        return self.__reduce__()

    def __getstate__(self):
        return self.__copy__()

    def to_json(self):
        return self.__copy__()

    def __snapshot_seal(self) -> str:
        carrier_copy = self.__carrier_input
        file_rows = [
            {
                "role": role,
                "raw_sha256": hashlib.sha256(raw).hexdigest(),
                "size_bytes": len(raw),
            }
            for role, raw in sorted(carrier_copy["file_bytes_by_role"].items())
        ]
        return semantic_digest(
            _CANDIDATE_SEAL_DOMAIN,
            {
                "candidate_identity": _CANDIDATE_IDENTITY,
                "versions_raw_sha256": hashlib.sha256(self.__versions_bytes).hexdigest(),
                "input_binding_raw_sha256": hashlib.sha256(self.__input_binding_bytes).hexdigest(),
                "input_raw": [hashlib.sha256(value).hexdigest() for value in self.__input_raw],
                "roster_raw_sha256": hashlib.sha256(self.__roster_bytes).hexdigest(),
                "context_raw_sha256": hashlib.sha256(self.__context_bytes).hexdigest(),
                "branch": self.__branch,
                "route": self.__route,
                "result_kind": self.__result_kind,
                "declared_world": self.__declared_world,
                "continuity_raw_sha256": hashlib.sha256(self.__continuity_bytes).hexdigest(),
                "result_raw_sha256": hashlib.sha256(self.__result_bytes).hexdigest(),
                "carrier_records_raw_sha256": hashlib.sha256(
                    canonical_json_bytes(carrier_copy["files"])
                ).hexdigest(),
                "carrier_files": file_rows,
                "carrier_consumption_identity": carrier_copy["consumption_identity"],
                "carrier_input_admission_digest": carrier_copy["admission_digest"],
                "carrier_input_validation_raw_sha256": hashlib.sha256(
                    canonical_json_bytes(carrier_copy["validation"])
                ).hexdigest(),
                "carrier_authority_ceiling_raw_sha256": hashlib.sha256(
                    canonical_json_bytes(carrier_copy["authority_ceiling"])
                ).hexdigest(),
                "carrier_validation_raw_sha256": hashlib.sha256(
                    self.__carrier_validation_bytes
                ).hexdigest(),
                "carrier_candidate_digest": self.__carrier_candidate_digest,
                "carrier_admission_digest": self.__carrier_admission_digest,
                "manifest_validation_raw_sha256": hashlib.sha256(
                    self.__manifest_validation_bytes
                ).hexdigest(),
                "manifest_admission_digest": self.__manifest_admission_digest,
                "manifest_raw_sha256": hashlib.sha256(self.__manifest_bytes).hexdigest(),
                "staging_receipt_raw_sha256": hashlib.sha256(
                    self.__staging_receipt_bytes
                ).hexdigest(),
                "cleanup_raw_sha256": hashlib.sha256(self.__cleanup_bytes).hexdigest(),
                "terminal_phase_raw_sha256": hashlib.sha256(
                    self.__terminal_phase.canonical_bytes
                ).hexdigest(),
            },
        )

    def _begin_validation(self) -> dict[str, object]:
        with self.__lock:
            if self.__state != "PENDING":
                raise GlobalReviewCompositionError(
                    GlobalCompositionFailureFamily.REPLAY_REJECTED
                )
            try:
                mutated = (
                    self.__owner is not self.__bound_owner
                    or self.__input_binding_bytes
                    is not self.__bound_input_binding_bytes
                    or self.__input_raw is not self.__bound_input_raw
                    or self.__roster_bytes is not self.__bound_roster_bytes
                    or self.__context_bytes is not self.__bound_context_bytes
                    or self.__context is not self.__bound_context
                    or self.__continuity_bytes
                    is not self.__bound_continuity_bytes
                    or self.__result_bytes is not self.__bound_result_bytes
                    or self.__carrier_input is not self.__bound_carrier_input
                    or self.__manifest_bytes is not self.__bound_manifest_bytes
                    or self.__terminal_phase is not self.__bound_terminal_phase
                    or self.__admitted_manifest
                    is not self.__bound_admitted_manifest
                    or self.__seal is not self.__bound_seal
                    or self.__snapshot_seal() != self.__seal
                )
            except Exception as exc:
                self.__state = "REVOKED"
                raise GlobalReviewCompositionError(
                    GlobalCompositionFailureFamily.LATE_MUTATION_REJECTED
                ) from exc
            if mutated:
                self.__state = "REVOKED"
                raise GlobalReviewCompositionError(
                    GlobalCompositionFailureFamily.LATE_MUTATION_REJECTED
                )
            self.__state = "VALIDATING"
        try:
            return {
                "owner": self.__owner,
                "versions": json.loads(self.__versions_bytes),
                "input_binding": json.loads(self.__input_binding_bytes),
                "input_raw": tuple(
                    _owned_bytes(value) for value in self.__input_raw
                ),
                "roster": json.loads(self.__roster_bytes),
                "context_document": json.loads(self.__context_bytes),
                "context": self.__context,
                "branch": self.__branch,
                "route": self.__route,
                "result_kind": self.__result_kind,
                "declared_world": self.__declared_world,
                "continuity": json.loads(self.__continuity_bytes),
                "result_document": json.loads(self.__result_bytes),
                "carrier_input": _copy_carrier_input(self.__carrier_input),
                "carrier_validation": json.loads(
                    self.__carrier_validation_bytes
                ),
                "carrier_candidate_digest": self.__carrier_candidate_digest,
                "carrier_admission_digest": self.__carrier_admission_digest,
                "manifest_validation": json.loads(
                    self.__manifest_validation_bytes
                ),
                "manifest_admission_digest": self.__manifest_admission_digest,
                "manifest_bytes": _owned_bytes(self.__manifest_bytes),
                "staging_receipt": json.loads(self.__staging_receipt_bytes),
                "cleanup_outcome": json.loads(self.__cleanup_bytes),
                "terminal_phase": self.__terminal_phase,
                "candidate_seal": self.__seal,
            }
        except GlobalReviewCompositionError:
            self._validation_failed()
            raise
        except Exception as exc:
            self._validation_failed()
            raise GlobalReviewCompositionError(
                GlobalCompositionFailureFamily.LATE_MUTATION_REJECTED,
                original_reason=_lower_reason(exc),
            ) from exc

    def _validation_failed(self) -> None:
        with self.__lock:
            self.__state = "REVOKED"

    def _validation_succeeded(self) -> None:
        with self.__lock:
            if self.__state != "VALIDATING":
                raise GlobalReviewCompositionError(
                    GlobalCompositionFailureFamily.ADMISSION_REJECTED
                )
            self.__state = "ADMITTED"

    def _attempt_manifest_staging_replay(self) -> None:
        try:
            manifest02.stage_admitted_review_derivation_manifest_0_2(
                self.__admitted_manifest, {}
            )
        except manifest02.Manifest02Error as exc:
            raise GlobalReviewCompositionError(
                GlobalCompositionFailureFamily.REPLAY_REJECTED,
                original_reason=_lower_reason(exc),
            ) from exc
        raise GlobalReviewCompositionError(
            GlobalCompositionFailureFamily.ADMISSION_REJECTED,
            original_reason="MANIFEST_STAGING_REPLAY_UNEXPECTEDLY_SUCCEEDED",
        )


def _copy_carrier_input(value: Mapping[str, object]) -> dict[str, object]:
    records = value.get("files")
    byte_map = value.get("file_bytes_by_role")
    if not isinstance(records, list) or not isinstance(byte_map, Mapping):
        raise GlobalReviewCompositionError(
            GlobalCompositionFailureFamily.PARTIAL_RESULT_REJECTED
        )
    copied_bytes = {
        key: _owned_bytes(raw)
        for key, raw in byte_map.items()
        if type(key) is str and type(raw) is bytes
    }
    if len(copied_bytes) != len(byte_map):
        raise GlobalReviewCompositionError(
            GlobalCompositionFailureFamily.PARTIAL_RESULT_REJECTED
        )
    return {
        "consumption_identity": value.get("consumption_identity"),
        "admission_digest": value.get("admission_digest"),
        "files": copy.deepcopy(records),
        "file_bytes_by_role": copied_bytes,
        "validation": copy.deepcopy(value.get("validation")),
        "authority_ceiling": copy.deepcopy(value.get("authority_ceiling")),
    }


class GlobalReviewCompositionResult:
    """One-shot private admitted result; never a public Artifact or Verdict."""

    def __init__(self, document: Mapping[str, object], *, _token: object) -> None:
        if _token is not _RESULT_TOKEN:
            raise GlobalReviewCompositionError(
                GlobalCompositionFailureFamily.ADMISSION_REJECTED
            )
        self.__lock = threading.Lock()
        self.__consumed = False
        self.__document_bytes = _json_bytes(document)
        self.__bound_document_bytes = self.__document_bytes
        self.__document_seal = hashlib.sha256(self.__document_bytes).hexdigest()
        self.__bound_document_seal = self.__document_seal

    def __copy__(self):
        raise GlobalReviewCompositionError(
            GlobalCompositionFailureFamily.ADMISSION_REJECTED
        )

    def __deepcopy__(self, _memo):
        return self.__copy__()

    def __reduce__(self):
        return self.__copy__()

    def __reduce_ex__(self, _protocol):
        return self.__reduce__()

    def __getstate__(self):
        return self.__copy__()

    def to_json(self):
        return self.__copy__()

    @property
    def world(self) -> str:
        self.__validate()
        return json.loads(self.__document_bytes)["world"]

    def __validate(self) -> None:
        if (
            self.__document_bytes is not self.__bound_document_bytes
            or type(self.__document_bytes) is not bytes
            or self.__document_seal is not self.__bound_document_seal
            or hashlib.sha256(self.__document_bytes).hexdigest()
            != self.__document_seal
        ):
            raise GlobalReviewCompositionError(
                GlobalCompositionFailureFamily.LATE_MUTATION_REJECTED
            )
        try:
            document = json.loads(self.__document_bytes)
            unsigned = copy.deepcopy(document)
            admission_digest = unsigned.pop("global_admission_digest", None)
        except Exception as exc:
            raise GlobalReviewCompositionError(
                GlobalCompositionFailureFamily.ADMISSION_REJECTED,
                original_reason=_lower_reason(exc),
            ) from exc
        if (
            any(document.get(key) != value for key, value in _VERSION_DOCUMENT.items())
            or admission_digest != semantic_digest(ADMISSION_FUNCTION, unsigned)
        ):
            raise GlobalReviewCompositionError(
                GlobalCompositionFailureFamily.ADMISSION_REJECTED
            )

    def claim_private_result(self) -> dict[str, object]:
        with self.__lock:
            self.__validate()
            if self.__consumed:
                raise GlobalReviewCompositionError(
                    GlobalCompositionFailureFamily.REPLAY_REJECTED
                )
            self.__consumed = True
            return json.loads(self.__document_bytes)


class BoundGlobalReviewCompositionAuthority:
    def __init__(
        self,
        closure: OwnedParseFulfillmentClosure,
        *,
        exact_inputs: DerivationInputSet,
        context: BudgetContext,
        derivation_id: str,
        bindings: Sequence[ProviderBinding],
        cleanup_obligations: Sequence[Callable[[], object]] = (),
        transport_limits: ExecutionCellTransportSafetyLimits = DEFAULT_TRANSPORT_LIMITS,
        cancellation_requested: Callable[[], bool] | None = None,
        versions: Mapping[str, str] = _VERSION_DOCUMENT,
    ) -> None:
        self.__lock = threading.RLock()
        self.__state = GlobalCompositionState.BOUND
        self.__candidate: _GlobalCompositionCandidate | None = None
        self.__result: GlobalReviewCompositionResult | None = None
        if type(closure) is not OwnedParseFulfillmentClosure:
            raise GlobalReviewCompositionError(
                GlobalCompositionFailureFamily.INPUT_BINDING_REJECTED
            )
        if dict(versions) != _VERSION_DOCUMENT:
            raise GlobalReviewCompositionError(
                GlobalCompositionFailureFamily.VERSION_REJECTED
            )
        self.__versions = copy.deepcopy(_VERSION_DOCUMENT)
        self.__inputs = exact_inputs
        self.__input_material = _input_binding_material(exact_inputs)
        self.__context = context
        self.__context_bytes = _json_bytes(_context_document(context))
        self.__roster = tuple(bindings)
        self.__roster_bytes = _json_bytes(_roster_document(exact_inputs, bindings))
        self.__cleanup_obligations = tuple(cleanup_obligations)
        if any(not callable(item) for item in self.__cleanup_obligations):
            raise GlobalReviewCompositionError(
                GlobalCompositionFailureFamily.INPUT_BINDING_REJECTED
            )
        try:
            selector = dual.create_post_terminal_fact_dual_successor_consumer(
                closure,
                derivation_id=derivation_id,
                bindings=self.__roster,
                transport_limits=transport_limits,
                cancellation_requested=cancellation_requested,
            )
        except Exception as exc:
            raise GlobalReviewCompositionError(
                GlobalCompositionFailureFamily.INPUT_BINDING_REJECTED,
                original_reason=_lower_reason(exc),
            ) from exc
        actual_inputs = getattr(selector, "_OwnedPostTerminalFactDualSuccessor__inputs", None)
        actual_context = getattr(selector, "_OwnedPostTerminalFactDualSuccessor__context", None)
        actual_bindings = getattr(selector, "_OwnedPostTerminalFactDualSuccessor__bindings", None)
        if actual_inputs is not exact_inputs or actual_context is not context:
            raise GlobalReviewCompositionError(
                GlobalCompositionFailureFamily.FOREIGN_CONTEXT_REJECTED
            )
        try:
            actual_roster = _json_bytes(_roster_document(exact_inputs, actual_bindings))
        except Exception as exc:
            raise GlobalReviewCompositionError(
                GlobalCompositionFailureFamily.PROVIDER_ROSTER_REJECTED,
                original_reason=_lower_reason(exc),
            ) from exc
        if actual_roster != self.__roster_bytes:
            raise GlobalReviewCompositionError(
                GlobalCompositionFailureFamily.PROVIDER_ROSTER_REJECTED
            )
        self.__selector = selector
        self.__bound_selector = selector
        self.__staging: dict[str, bytes] | None = None

    @property
    def state(self) -> GlobalCompositionState:
        with self.__lock:
            return self.__state

    def __copy__(self):
        self.__revoke()
        raise GlobalReviewCompositionError(
            GlobalCompositionFailureFamily.REPLAY_REJECTED
        )

    def __deepcopy__(self, _memo):
        return self.__copy__()

    def __reduce__(self):
        return self.__copy__()

    def __reduce_ex__(self, _protocol):
        return self.__reduce__()

    def __revoke(self) -> None:
        with self.__lock:
            self.__state = GlobalCompositionState.REVOKED

    def _validate_candidate_owner(self, candidate: _GlobalCompositionCandidate) -> None:
        with self.__lock:
            if (
                self.__state is not GlobalCompositionState.CANDIDATE_READY
                or candidate is not self.__candidate
                or self.__selector is not self.__bound_selector
            ):
                raise GlobalReviewCompositionError(
                    GlobalCompositionFailureFamily.ADMISSION_REJECTED
                )
            if _input_binding_material(self.__inputs) != self.__input_material:
                raise GlobalReviewCompositionError(
                    GlobalCompositionFailureFamily.LATE_MUTATION_REJECTED
                )
            if _json_bytes(_context_document(self.__context)) != self.__context_bytes:
                raise GlobalReviewCompositionError(
                    GlobalCompositionFailureFamily.FOREIGN_CONTEXT_REJECTED
                )
            if _json_bytes(_roster_document(self.__inputs, self.__roster)) != self.__roster_bytes:
                raise GlobalReviewCompositionError(
                    GlobalCompositionFailureFamily.PROVIDER_ROSTER_REJECTED
                )

    def _admission_binding_material(self) -> dict[str, object]:
        with self.__lock:
            return {
                "input_binding": json.loads(self.__input_material[0]),
                "input_raw": tuple(
                    _owned_bytes(value) for value in self.__input_material[1:]
                ),
                "roster": json.loads(self.__roster_bytes),
                "context_document": json.loads(self.__context_bytes),
                "context": self.__context,
            }

    def _admission_succeeded(
        self,
        candidate: _GlobalCompositionCandidate,
        result: GlobalReviewCompositionResult,
    ) -> None:
        with self.__lock:
            self._validate_candidate_owner(candidate)
            self.__result = result
            self.__state = GlobalCompositionState.ADMITTED

    def __cleanup(self) -> dict[str, object]:
        records = []
        obligations = [
            ("owned-private-manifest-staging", self.__clear_staging),
            *[
                (f"caller-bound-{index:03d}", action)
                for index, action in enumerate(self.__cleanup_obligations)
            ],
        ]
        for name, action in reversed(obligations):
            try:
                value = action()
                closed = value is not False
                reason = None if closed else "CLEANUP_RETURNED_FALSE"
            except Exception as exc:
                closed = False
                reason = _lower_reason(exc)
            records.append(
                {"obligation": name, "closed": closed, "reason": reason}
            )
        records.reverse()
        outcome = {
            "cleanup_identity": _CLEANUP_IDENTITY,
            "context_runtime_identity": id(self.__context),
            "obligations": records,
            "all_closed": all(item["closed"] is True for item in records),
            "context_state": self.__context.state.value,
            "stop_trigger": (
                None
                if self.__context.stop_trigger is None
                else self.__context.stop_trigger.value
            ),
        }
        outcome["cleanup_digest"] = semantic_digest(_CLEANUP_IDENTITY, outcome)
        return outcome

    def __clear_staging(self) -> bool:
        if self.__staging is not None:
            self.__staging.clear()
        return True

    def _produce_candidate_for_admission(self) -> _GlobalCompositionCandidate:
        with self.__lock:
            if self.__state is not GlobalCompositionState.BOUND:
                raise GlobalReviewCompositionError(
                    GlobalCompositionFailureFamily.REPLAY_REJECTED
                )
            self.__state = GlobalCompositionState.RUNNING

        first_error: GlobalReviewCompositionError | None = None
        material: dict[str, object] | None = None
        try:
            if self.__selector is not self.__bound_selector:
                raise GlobalReviewCompositionError(
                    GlobalCompositionFailureFamily.LATE_MUTATION_REJECTED
                )
            observations = tuple(
                fact.execute_product_fact_claim(claim)
                for claim in self.__selector.claims()
            )
            self.__selector.reconcile(observations)
            branch = getattr(
                self.__selector,
                "_OwnedPostTerminalFactDualSuccessor__branch",
                None,
            )
            route = getattr(
                self.__selector,
                "_OwnedPostTerminalFactDualSuccessor__route",
                None,
            )
            if route == _NORMAL_ROUTE and branch == "NORMAL_FULFILLED":
                route_claim = self.__selector.claim_relation()
                output_owner = unified.bind_unified_review_coverage_output_admission(
                    route_claim
                )
                admitted_transition = transition.run_claimed_fact_handoff_relation_transition(
                    route_claim
                )
                bridge = positive.admit_relation_transition_for_slice_composition(
                    admitted_transition.claim_continuation()
                )
                route_result = positive.compose_review_slice_set_and_coverage(
                    bridge.claim_continuation()
                )
                admitted_output = output_owner.submit(route_result)
                result_document = route_result.document_copy()
            elif route == _NEGATIVE_ROUTE and branch in _NEGATIVE_WORLDS:
                route_claim = self.__selector.claim_exact_input()
                output_owner = unified.bind_unified_review_coverage_output_admission(
                    route_claim
                )
                attempt = negative.claim_negative_world_coverage_attempt(route_claim)
                coverage_candidate = negative.produce_negative_world_coverage_candidate(
                    attempt
                )
                coverage_validation = (
                    negative.independently_validate_negative_world_coverage_candidate(
                        attempt, coverage_candidate
                    )
                )
                route_result = negative.admit_negative_world_coverage_candidate(
                    attempt, coverage_candidate, coverage_validation
                )
                admitted_output = output_owner.submit(route_result)
                result_document = route_result.coverage_ledger_document_copy()
            else:
                raise GlobalReviewCompositionError(
                    GlobalCompositionFailureFamily.WORLD_SPLICE_REJECTED
                )

            continuity_value = admitted_output._same_attempt_derivation_evidence_continuity()
            continuity_document = continuity_value._document_copy()
            world = _producer_world(
                branch,
                route,
                admitted_output.result_kind,
                result_document,
            )
            carrier_claim = carrier.project_manifest_carrier_successor(
                continuity_value
            )
            carrier_candidate = carrier.build_manifest_carrier_successor_candidate(
                carrier_claim
            )
            carrier_validation = (
                carrier.independently_validate_manifest_carrier_successor_candidate(
                    carrier_candidate
                )
            )
            admitted_carrier = carrier.admit_manifest_carrier_successor_candidate(
                carrier_candidate, carrier_validation
            )
            carrier_input_object = admitted_carrier.claim_future_manifest_consumption()
            carrier_input = carrier_input_object.input_copy()
            manifest_candidate = manifest02.build_review_derivation_manifest_0_2_candidate(
                carrier_input_object
            )
            manifest_validation = (
                manifest02.independently_validate_review_derivation_manifest_0_2_candidate(
                    manifest_candidate
                )
            )
            admitted_manifest = manifest02.admit_review_derivation_manifest_0_2_candidate(
                manifest_candidate, manifest_validation
            )
            manifest_document = manifest02.consume_admitted_review_derivation_manifest_0_2(
                admitted_manifest
            )
            self.__staging = {}
            receipt = manifest02.stage_admitted_review_derivation_manifest_0_2(
                admitted_manifest, self.__staging
            ).receipt_copy()
            staged_raw = _owned_bytes(self.__staging["manifest.json"])
            if canonical_json_bytes(manifest_document) != staged_raw:
                raise GlobalReviewCompositionError(
                    GlobalCompositionFailureFamily.PARTIAL_RESULT_REJECTED
                )
            material = {
                "branch": branch,
                "route": route,
                "result_kind": admitted_output.result_kind,
                "world": world,
                "continuity": continuity_document,
                "result_document": result_document,
                "carrier_input": carrier_input,
                "carrier_validation": carrier_validation.report_copy(),
                "carrier_candidate_digest": carrier_validation._candidate_digest,
                "carrier_admission_digest": admitted_carrier.admission_digest,
                "manifest_validation": manifest_validation.report_copy(),
                "manifest_admission_digest": admitted_manifest.admission_digest,
                "manifest_bytes": staged_raw,
                "receipt": receipt,
                "admitted_manifest": admitted_manifest,
            }
        except GlobalReviewCompositionError as exc:
            first_error = exc
        except Exception as exc:
            first_error = GlobalReviewCompositionError(
                (
                    GlobalCompositionFailureFamily.FOREIGN_CONTEXT_REJECTED
                    if self.__context.state is not BudgetState.RUNNING
                    or self.__context.stop_trigger is not None
                    else GlobalCompositionFailureFamily.PARTIAL_RESULT_REJECTED
                ),
                original_reason=_lower_reason(exc),
            )

        cleanup = self.__cleanup()
        if first_error is not None:
            self.__revoke()
            raise GlobalReviewCompositionError(
                first_error.failure_family,
                original_reason=first_error.original_reason,
                cleanup_outcome=cleanup,
            ) from first_error
        if material is None:
            self.__revoke()
            raise GlobalReviewCompositionError(
                GlobalCompositionFailureFamily.PARTIAL_RESULT_REJECTED,
                cleanup_outcome=cleanup,
            )
        if cleanup["all_closed"] is not True:
            self.__revoke()
            raise GlobalReviewCompositionError(
                GlobalCompositionFailureFamily.RESOURCE_CLEANUP_FAILED,
                original_reason=next(
                    (
                        item["reason"]
                        for item in cleanup["obligations"]
                        if item["closed"] is not True
                    ),
                    "UNKNOWN",
                ),
                cleanup_outcome=cleanup,
            )
        phase_payload = {
            "candidate_identity": _CANDIDATE_IDENTITY,
            "world": material["world"],
            "continuity_digest": material["continuity"]["continuity_digest"],
            "manifest_raw_sha256": hashlib.sha256(material["manifest_bytes"]).hexdigest(),
            "cleanup_digest": cleanup["cleanup_digest"],
        }
        phase = self.__context.try_complete_phase(
            canonical_json_bytes(phase_payload), resources_closed=True
        )
        if phase is None:
            self.__revoke()
            raise GlobalReviewCompositionError(
                GlobalCompositionFailureFamily.FOREIGN_CONTEXT_REJECTED,
                original_reason=(
                    "UNKNOWN"
                    if self.__context.stop_trigger is None
                    else self.__context.stop_trigger.value
                ),
                cleanup_outcome=cleanup,
            )
        candidate = _GlobalCompositionCandidate(
            owner=self,
            versions=self.__versions,
            input_binding_bytes=self.__input_material[0],
            input_raw=self.__input_material[1:],
            roster_bytes=self.__roster_bytes,
            context_bytes=self.__context_bytes,
            context=self.__context,
            branch=material["branch"],
            route=material["route"],
            result_kind=material["result_kind"],
            declared_world=material["world"],
            continuity_bytes=canonical_json_bytes(material["continuity"]),
            result_bytes=canonical_json_bytes(material["result_document"]),
            carrier_input=material["carrier_input"],
            carrier_validation=material["carrier_validation"],
            carrier_candidate_digest=material["carrier_candidate_digest"],
            carrier_admission_digest=material["carrier_admission_digest"],
            manifest_validation=material["manifest_validation"],
            manifest_admission_digest=material["manifest_admission_digest"],
            manifest_bytes=material["manifest_bytes"],
            staging_receipt=material["receipt"],
            cleanup_outcome=cleanup,
            terminal_phase=phase,
            admitted_manifest=material["admitted_manifest"],
            _token=_CANDIDATE_TOKEN,
        )
        with self.__lock:
            if self.__state is not GlobalCompositionState.RUNNING:
                self.__state = GlobalCompositionState.REVOKED
                raise GlobalReviewCompositionError(
                    GlobalCompositionFailureFamily.REPLAY_REJECTED
                )
            self.__candidate = candidate
            self.__state = GlobalCompositionState.CANDIDATE_READY
        return candidate

    def run(self) -> GlobalReviewCompositionResult:
        candidate = self._produce_candidate_for_admission()
        return independently_admit_global_review_composition(candidate)


def independently_admit_global_review_composition(
    candidate: _GlobalCompositionCandidate,
) -> GlobalReviewCompositionResult:
    if type(candidate) is not _GlobalCompositionCandidate:
        raise GlobalReviewCompositionError(
            GlobalCompositionFailureFamily.ADMISSION_REJECTED
        )
    snapshot = candidate._begin_validation()
    try:
        if snapshot["versions"] != _VERSION_DOCUMENT:
            raise GlobalReviewCompositionError(
                GlobalCompositionFailureFamily.COMPONENT_VERSION_REJECTED
            )
        owner = snapshot["owner"]
        if type(owner) is not BoundGlobalReviewCompositionAuthority:
            raise GlobalReviewCompositionError(
                GlobalCompositionFailureFamily.ADMISSION_REJECTED
            )
        owner._validate_candidate_owner(candidate)
        bound = owner._admission_binding_material()
        if (
            snapshot["input_binding"] != bound["input_binding"]
            or snapshot["input_raw"] != bound["input_raw"]
        ):
            raise GlobalReviewCompositionError(
                GlobalCompositionFailureFamily.INPUT_BINDING_REJECTED
            )
        if snapshot["roster"] != bound["roster"]:
            raise GlobalReviewCompositionError(
                GlobalCompositionFailureFamily.PROVIDER_ROSTER_REJECTED
            )
        if (
            snapshot["context_document"] != bound["context_document"]
            or snapshot["context"] is not bound["context"]
        ):
            raise GlobalReviewCompositionError(
                GlobalCompositionFailureFamily.FOREIGN_CONTEXT_REJECTED
            )
        context = snapshot["context"]
        context_document = snapshot["context_document"]
        if (
            type(context) is not BudgetContext
            or context_document.get("runtime_identity") != id(context)
            or context.state is not BudgetState.RUNNING
            or context.stop_trigger is not None
            or not context.checkpoint()
        ):
            raise GlobalReviewCompositionError(
                GlobalCompositionFailureFamily.FOREIGN_CONTEXT_REJECTED
            )
        if snapshot["roster"].get("roster_identity") != _ROSTER_IDENTITY:
            raise GlobalReviewCompositionError(
                GlobalCompositionFailureFamily.PROVIDER_ROSTER_REJECTED
            )
        continuity_document = snapshot["continuity"]
        branch = snapshot["branch"]
        route = snapshot["route"]
        continuity_unsigned = copy.deepcopy(continuity_document)
        continuity_digest = continuity_unsigned.pop("continuity_digest", None)
        if (
            any(
                continuity_document.get(key) != value
                for key, value in _CONTINUITY_VERSIONS.items()
            )
            or continuity_document.get("authority_ceiling")
            != _CONTINUITY_AUTHORITY_CEILING
            or continuity_digest
            != semantic_digest(
                _CONTINUITY_VERSIONS["contract_function"],
                continuity_unsigned,
            )
            or continuity_document.get("terminal_branch") != branch
            or continuity_document.get("selector_route") != route
            or continuity_document.get("result_kind") != snapshot["result_kind"]
            or continuity_document.get("reconciliation", {}).get("status")
            != "RECONCILED"
        ):
            raise GlobalReviewCompositionError(
                GlobalCompositionFailureFamily.WORLD_SPLICE_REJECTED
            )
        actual_world = _independent_world(
            branch,
            route,
            snapshot["result_kind"],
            snapshot["result_document"],
        )
        if actual_world != snapshot["declared_world"]:
            raise GlobalReviewCompositionError(
                GlobalCompositionFailureFamily.WORLD_SPLICE_REJECTED
            )
        ledger = (
            snapshot["result_document"]["coverage_ledger"]
            if route == _NORMAL_ROUTE
            else snapshot["result_document"]
        )
        _validate_ledger_digests(ledger)
        if (
            continuity_document.get("coverage_ledger_digest")
            != ledger.get("coverage_ledger_digest")
            or continuity_document.get("root_chain_digest")
            != ledger.get("root_chain_digest")
        ):
            raise GlobalReviewCompositionError(
                GlobalCompositionFailureFamily.WORLD_SPLICE_REJECTED
            )

        carrier_input = snapshot["carrier_input"]
        records = carrier_input["files"]
        byte_map = carrier_input["file_bytes_by_role"]
        if (
            carrier_input.get("consumption_identity")
            != carrier.FUTURE_CONSUMPTION_IDENTITY
            or carrier_input.get("admission_digest")
            != snapshot["carrier_admission_digest"]
            or carrier_input.get("authority_ceiling")
            != carrier_conformance.authority_ceiling_copy()
        ):
            raise GlobalReviewCompositionError(
                GlobalCompositionFailureFamily.PARTIAL_RESULT_REJECTED
            )
        if not isinstance(records, list) or len(records) != len(byte_map):
            raise GlobalReviewCompositionError(
                GlobalCompositionFailureFamily.PARTIAL_RESULT_REJECTED
            )
        for record in records:
            role = record.get("role") if isinstance(record, Mapping) else None
            raw = byte_map.get(role)
            if (
                type(role) is not str
                or type(raw) is not bytes
                or record.get("raw_sha256") != hashlib.sha256(raw).hexdigest()
                or record.get("size_bytes") != len(raw)
            ):
                raise GlobalReviewCompositionError(
                    GlobalCompositionFailureFamily.PARTIAL_RESULT_REJECTED
                )
        carrier_report = snapshot["carrier_validation"]
        if not isinstance(carrier_report, dict):
            raise GlobalReviewCompositionError(
                GlobalCompositionFailureFamily.PARTIAL_RESULT_REJECTED
            )
        if carrier_input.get("validation") != carrier_report:
            raise GlobalReviewCompositionError(
                GlobalCompositionFailureFamily.PARTIAL_RESULT_REJECTED
            )
        unsigned_carrier_report = copy.deepcopy(carrier_report)
        carrier_validation_digest = unsigned_carrier_report.pop(
            "validation_digest", None
        )
        if (
            carrier_report.get("status") != "QUALIFIED"
            or carrier_report.get("coverage_ledger_digest")
            != ledger.get("coverage_ledger_digest")
            or carrier_report.get("root_chain_digest")
            != ledger.get("root_chain_digest")
            or carrier_report.get("file_binding_digest")
            != semantic_digest(carrier_conformance.FILE_BINDING_DOMAIN, records)
            or carrier_validation_digest
            != semantic_digest(
                carrier_conformance.VALIDATION_DOMAIN,
                unsigned_carrier_report,
            )
        ):
            raise GlobalReviewCompositionError(
                GlobalCompositionFailureFamily.PARTIAL_RESULT_REJECTED
            )
        expected_carrier_admission = semantic_digest(
            carrier.ADMISSION_IDENTITY_DOMAIN,
            {
                "candidate_digest": snapshot["carrier_candidate_digest"],
                "validation_digest": carrier_validation_digest,
                "file_binding_digest": carrier_report["file_binding_digest"],
                "topology_proof_digest": carrier_report[
                    "topology_proof_digest"
                ],
            },
        )
        if snapshot["carrier_admission_digest"] != expected_carrier_admission:
            raise GlobalReviewCompositionError(
                GlobalCompositionFailureFamily.PARTIAL_RESULT_REJECTED
            )
        manifest_raw = snapshot["manifest_bytes"]
        if (
            manifest02.dispatch_review_derivation_manifest_version(manifest_raw)
            is not manifest02.ManifestSchemaVersion.V0_2
        ):
            raise GlobalReviewCompositionError(
                GlobalCompositionFailureFamily.COMPONENT_VERSION_REJECTED
            )
        manifest_document = json.loads(manifest_raw)
        manifest_files = manifest_document.get("files")
        expected_files = [
            {
                "role": item["role"],
                "path": item["path"],
                "sha256": item["raw_sha256"],
                "size_bytes": item["size_bytes"],
                "semantic_digest": item["semantic_digest"],
            }
            for item in records
        ]
        if manifest_files != expected_files:
            raise GlobalReviewCompositionError(
                GlobalCompositionFailureFamily.PARTIAL_RESULT_REJECTED
            )
        manifest_report = snapshot["manifest_validation"]
        if not isinstance(manifest_report, dict):
            raise GlobalReviewCompositionError(
                GlobalCompositionFailureFamily.PARTIAL_RESULT_REJECTED
            )
        unsigned_manifest_report = copy.deepcopy(manifest_report)
        manifest_validation_digest = unsigned_manifest_report.pop(
            "validation_digest", None
        )
        if (
            manifest_report.get("status") != "QUALIFIED"
            or manifest_report.get("manifest_raw_sha256")
            != hashlib.sha256(manifest_raw).hexdigest()
            or manifest_report.get("carrier_admission_digest")
            != snapshot["carrier_admission_digest"]
            or manifest_report.get("carrier_validation_digest")
            != carrier_validation_digest
            or manifest_report.get("file_binding_digest")
            != carrier_report.get("file_binding_digest")
            or manifest_report.get("coverage_ledger_digest")
            != ledger.get("coverage_ledger_digest")
            or manifest_report.get("root_chain_digest")
            != ledger.get("root_chain_digest")
            or manifest_validation_digest
            != semantic_digest(
                manifest_conformance.VALIDATION_DOMAIN,
                unsigned_manifest_report,
            )
        ):
            raise GlobalReviewCompositionError(
                GlobalCompositionFailureFamily.PARTIAL_RESULT_REJECTED
            )
        try:
            recomputed_manifest_report = (
                manifest_conformance.validate_review_derivation_manifest_0_2_snapshot(
                    {
                    "producer_identity": manifest02.PROJECTION_IDENTITY,
                    "conformance_identity": manifest_conformance.CONFORMANCE_IDENTITY,
                    "shared_expected_projector_state": False,
                    "manifest_bytes": manifest_raw,
                    "carrier_admission_digest": snapshot[
                        "carrier_admission_digest"
                    ],
                    "carrier_records": tuple(copy.deepcopy(records)),
                    "carrier_bytes_by_role": {
                        role: _owned_bytes(raw) for role, raw in byte_map.items()
                    },
                    "carrier_validation": copy.deepcopy(carrier_report),
                    "input_snapshot_digest": semantic_digest(
                        manifest_conformance.INPUT_SNAPSHOT_DOMAIN,
                        {
                            "carrier_admission_digest": snapshot[
                                "carrier_admission_digest"
                            ],
                            "carrier_validation_digest": carrier_validation_digest,
                            "manifest_raw_sha256": hashlib.sha256(
                                manifest_raw
                            ).hexdigest(),
                            "records": copy.deepcopy(records),
                        },
                    ),
                    "authority_ceiling": manifest_conformance.authority_ceiling_copy(),
                    }
                )
            )
        except manifest_conformance.Manifest02ConformanceFailure as exc:
            raise GlobalReviewCompositionError(
                GlobalCompositionFailureFamily.PARTIAL_RESULT_REJECTED,
                original_reason=_lower_reason(exc),
            ) from exc
        if recomputed_manifest_report != manifest_report:
            raise GlobalReviewCompositionError(
                GlobalCompositionFailureFamily.PARTIAL_RESULT_REJECTED
            )
        expected_manifest_admission = semantic_digest(
            manifest02.ADMISSION_DOMAIN,
            {
                "manifest_raw_sha256": manifest_report[
                    "manifest_raw_sha256"
                ],
                "carrier_admission_digest": snapshot[
                    "carrier_admission_digest"
                ],
                "validation_digest": manifest_validation_digest,
            },
        )
        if snapshot["manifest_admission_digest"] != expected_manifest_admission:
            raise GlobalReviewCompositionError(
                GlobalCompositionFailureFamily.PARTIAL_RESULT_REJECTED
            )
        roles = [item["role"] for item in manifest_files]
        expected_roles = (
            [
                "SOURCE_SNAPSHOT",
                "REVIEW_POLICY",
                "DERIVATION_PROFILE",
                "DERIVATION_EVIDENCE",
                "FACT_SET",
                "RELATION_SET",
                "COVERAGE_LEDGER",
            ]
            if actual_world == "NORMAL_RELATION_CONFLICT"
            else [
                "SOURCE_SNAPSHOT",
                "REVIEW_POLICY",
                "DERIVATION_PROFILE",
                "DERIVATION_EVIDENCE",
                "FACT_SET",
                "RELATION_SET",
                "REVIEW_SLICE_SET",
                "COVERAGE_LEDGER",
            ]
            if actual_world.startswith("NORMAL_")
            else [
                "SOURCE_SNAPSHOT",
                "REVIEW_POLICY",
                "DERIVATION_PROFILE",
                "DERIVATION_EVIDENCE",
                "COVERAGE_LEDGER",
            ]
        )
        if roles != expected_roles:
            raise GlobalReviewCompositionError(
                GlobalCompositionFailureFamily.WORLD_SPLICE_REJECTED
            )
        receipt = snapshot["staging_receipt"]
        if (
            receipt.get("staging_identity")
            != manifest02.PRIVATE_STAGING_IDENTITY
            or receipt.get("path") != "manifest.json"
            or receipt.get("admission_digest")
            != snapshot["manifest_admission_digest"]
            or receipt.get("raw_sha256") != hashlib.sha256(manifest_raw).hexdigest()
            or receipt.get("size_bytes") != len(manifest_raw)
            or receipt.get("receipt_digest")
            != semantic_digest(
                manifest02.PUBLICATION_RECEIPT_DOMAIN,
                {
                    key: copy.deepcopy(value)
                    for key, value in receipt.items()
                    if key != "receipt_digest"
                },
            )
        ):
            raise GlobalReviewCompositionError(
                GlobalCompositionFailureFamily.PARTIAL_RESULT_REJECTED
            )
        cleanup = snapshot["cleanup_outcome"]
        unsigned_cleanup = copy.deepcopy(cleanup)
        cleanup_digest = unsigned_cleanup.pop("cleanup_digest", None)
        if (
            cleanup.get("cleanup_identity") != _CLEANUP_IDENTITY
            or cleanup_digest
            != semantic_digest(_CLEANUP_IDENTITY, unsigned_cleanup)
            or cleanup.get("all_closed") is not True
            or cleanup.get("context_runtime_identity") != id(context)
            or cleanup.get("context_state") != "RUNNING"
            or cleanup.get("stop_trigger") is not None
        ):
            raise GlobalReviewCompositionError(
                GlobalCompositionFailureFamily.RESOURCE_CLEANUP_FAILED
            )
        terminal_phase = snapshot["terminal_phase"]
        if type(terminal_phase) is not OwnedPhaseResult:
            raise GlobalReviewCompositionError(
                GlobalCompositionFailureFamily.PARTIAL_RESULT_REJECTED
            )
        expected_phase_payload = {
            "candidate_identity": _CANDIDATE_IDENTITY,
            "world": actual_world,
            "continuity_digest": continuity_document["continuity_digest"],
            "manifest_raw_sha256": hashlib.sha256(manifest_raw).hexdigest(),
            "cleanup_digest": cleanup["cleanup_digest"],
        }
        if (
            terminal_phase.phase_status != "COMPLETED_FOR_PHASE"
            or terminal_phase.canonical_bytes
            != canonical_json_bytes(expected_phase_payload)
            or not (
                context.started_at_monotonic
                <= terminal_phase.completed_at_monotonic
                <= context.execution_deadline_monotonic
            )
        ):
            raise GlobalReviewCompositionError(
                GlobalCompositionFailureFamily.PARTIAL_RESULT_REJECTED
            )
        summary = {
            **_VERSION_DOCUMENT,
            "candidate_identity": _CANDIDATE_IDENTITY,
            "candidate_seal": snapshot["candidate_seal"],
            "input_binding_digest": semantic_digest(
                ATTEMPT_BINDING_FUNCTION, snapshot["input_binding"]
            ),
            "provider_roster_digest": semantic_digest(
                _ROSTER_IDENTITY, snapshot["roster"]
            ),
            "context_runtime_identity": id(context),
            "fact_consumer_attempt_id": continuity_document[
                "fact_consumer_attempt_id"
            ],
            "world": actual_world,
            "terminal_branch": branch,
            "selector_route": route,
            "application_admission_digest": continuity_document[
                "application_admission_digest"
            ],
            "continuity_digest": continuity_document["continuity_digest"],
            "coverage_ledger_digest": ledger["coverage_ledger_digest"],
            "root_chain_digest": ledger["root_chain_digest"],
            "root_topology": [
                {
                    "stage": item["stage"],
                    "binding_state": item["binding_state"],
                    "terminal_branch": item["terminal_branch"],
                }
                for item in ledger["root_bindings"]
            ],
            "carrier_admission_digest": snapshot["carrier_admission_digest"],
            "carrier_validation_digest": carrier_validation_digest,
            "manifest_admission_digest": snapshot["manifest_admission_digest"],
            "manifest_validation_digest": manifest_validation_digest,
            "manifest_raw_sha256": hashlib.sha256(manifest_raw).hexdigest(),
            "manifest_file_semantic_digests": [
                {
                    "role": item["role"],
                    "semantic_digest": item["semantic_digest"],
                }
                for item in manifest_files
            ],
            "staging_receipt_digest": receipt["receipt_digest"],
            "cleanup_outcome": copy.deepcopy(cleanup),
            "terminal_phase_completed_at_monotonic": terminal_phase.completed_at_monotonic,
            "authority_ceiling": {
                "private_global_composition_result": True,
                "reality_observation": False,
                "provider_observation": False,
                "evidence_sufficiency": False,
                "persistence": False,
                "public_review": False,
                "core_verdict": False,
                "human_disposition": False,
                "r2_r6": False,
            },
        }
        summary["global_admission_digest"] = semantic_digest(
            ADMISSION_FUNCTION, summary
        )
        result = GlobalReviewCompositionResult(summary, _token=_RESULT_TOKEN)
        candidate._validation_succeeded()
        owner._admission_succeeded(candidate, result)
        return result
    except GlobalReviewCompositionError:
        candidate._validation_failed()
        raise
    except manifest02.Manifest02Error as exc:
        candidate._validation_failed()
        raise GlobalReviewCompositionError(
            GlobalCompositionFailureFamily.COMPONENT_VERSION_REJECTED,
            original_reason=_lower_reason(exc),
        ) from exc
    except Exception as exc:
        candidate._validation_failed()
        raise GlobalReviewCompositionError(
            GlobalCompositionFailureFamily.ADMISSION_REJECTED,
            original_reason=_lower_reason(exc),
        ) from exc


def bind_global_review_composition_authority(
    closure: OwnedParseFulfillmentClosure,
    *,
    exact_inputs: DerivationInputSet,
    context: BudgetContext,
    derivation_id: str,
    bindings: Sequence[ProviderBinding],
    cleanup_obligations: Sequence[Callable[[], object]] = (),
    transport_limits: ExecutionCellTransportSafetyLimits = DEFAULT_TRANSPORT_LIMITS,
    cancellation_requested: Callable[[], bool] | None = None,
    versions: Mapping[str, str] = _VERSION_DOCUMENT,
) -> BoundGlobalReviewCompositionAuthority:
    return BoundGlobalReviewCompositionAuthority(
        closure,
        exact_inputs=exact_inputs,
        context=context,
        derivation_id=derivation_id,
        bindings=bindings,
        cleanup_obligations=cleanup_obligations,
        transport_limits=transport_limits,
        cancellation_requested=cancellation_requested,
        versions=versions,
    )
