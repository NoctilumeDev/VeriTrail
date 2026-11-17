"""Bounded private DerivationEvidence 0.3 and exact snapshot carrier.

The implementation ends at a one-shot future-Manifest input.  It does not
construct a Manifest, persist artifacts, expose a public Review API, or produce
a Core Verdict.
"""

from __future__ import annotations

import copy
import hashlib
import json
import threading
from enum import Enum
from typing import Mapping

from veritrail_review import _same_attempt_derivation_evidence_continuity as continuity
from veritrail_review import _derivation_evidence_manifest_carrier_conformance as conformance
from veritrail_review.canonical import canonical_json_bytes, semantic_digest


PROJECTION_FUNCTION = (
    "r1-derivation-evidence-manifest-carrier-successor-projection/0.1"
)
EVIDENCE_IDENTITY_DOMAIN = "veritrail.review.derivation-evidence/0.3"
CANDIDATE_IDENTITY_DOMAIN = "veritrail.review.manifest-carrier-candidate/0.1"
ADMISSION_IDENTITY_DOMAIN = "veritrail.review.manifest-carrier-admission/0.1"
FUTURE_CONSUMPTION_IDENTITY = (
    "r1-future-manifest-carrier-consumption-input/0.1"
)
OWNED_SNAPSHOT_IDENTITY_DOMAIN = (
    "veritrail.review.derivation-manifest-owned-snapshot/0.1"
)

_ROLE_PATHS = (
    ("SOURCE_SNAPSHOT", "source-snapshot.json", "source_snapshot_digest"),
    ("REVIEW_POLICY", "review-policy.json", "policy_digest"),
    ("DERIVATION_PROFILE", "derivation-profile.json", "profile_digest"),
    (
        "DERIVATION_EVIDENCE",
        "derivation-evidence.json",
        "derivation_evidence_digest",
    ),
    ("FACT_SET", "fact-set.json", "fact_set_digest"),
    ("RELATION_SET", "relation-set.json", "relation_set_digest"),
    ("REVIEW_SLICE_SET", "review-slices.json", "slice_set_digest"),
    ("COVERAGE_LEDGER", "coverage-ledger.json", "coverage_ledger_digest"),
)
_CLAIM_TOKEN = object()
_CANDIDATE_TOKEN = object()
_VALIDATION_TOKEN = object()
_ADMISSION_TOKEN = object()
_CONSUMPTION_TOKEN = object()


class ManifestCarrierSuccessorFailureFamily(str, Enum):
    MANIFEST_CARRIER_SUCCESSOR_VERSION_REJECTED = (
        "MANIFEST_CARRIER_SUCCESSOR_VERSION_REJECTED"
    )
    MANIFEST_CARRIER_PROJECTION_CLAIM_REJECTED = (
        "MANIFEST_CARRIER_PROJECTION_CLAIM_REJECTED"
    )
    MANIFEST_CARRIER_EVIDENCE_BINDING_REJECTED = (
        "MANIFEST_CARRIER_EVIDENCE_BINDING_REJECTED"
    )
    MANIFEST_CARRIER_LEDGER_CONFORMANCE_REJECTED = (
        "MANIFEST_CARRIER_LEDGER_CONFORMANCE_REJECTED"
    )
    MANIFEST_CARRIER_TOPOLOGY_REJECTED = (
        "MANIFEST_CARRIER_TOPOLOGY_REJECTED"
    )
    MANIFEST_CARRIER_CHILD_BINDING_REJECTED = (
        "MANIFEST_CARRIER_CHILD_BINDING_REJECTED"
    )
    MANIFEST_CARRIER_SNAPSHOT_MUTATION_REJECTED = (
        "MANIFEST_CARRIER_SNAPSHOT_MUTATION_REJECTED"
    )
    MANIFEST_CARRIER_SAME_ATTEMPT_REJECTED = (
        "MANIFEST_CARRIER_SAME_ATTEMPT_REJECTED"
    )
    MANIFEST_CARRIER_CONTEXT_REVOKED = "MANIFEST_CARRIER_CONTEXT_REVOKED"
    MANIFEST_CARRIER_COMMON_MODE_ORACLE_REJECTED = (
        "MANIFEST_CARRIER_COMMON_MODE_ORACLE_REJECTED"
    )
    MANIFEST_CARRIER_LEGACY_ALIAS_REJECTED = (
        "MANIFEST_CARRIER_LEGACY_ALIAS_REJECTED"
    )
    MANIFEST_CARRIER_ALREADY_VALIDATED = "MANIFEST_CARRIER_ALREADY_VALIDATED"
    MANIFEST_CARRIER_ALREADY_CONSUMED = "MANIFEST_CARRIER_ALREADY_CONSUMED"
    MANIFEST_CARRIER_AUTHORITY_CEILING_REJECTED = (
        "MANIFEST_CARRIER_AUTHORITY_CEILING_REJECTED"
    )


class ManifestCarrierSuccessorError(ValueError):
    def __init__(self, family: ManifestCarrierSuccessorFailureFamily) -> None:
        self.failure_family = family
        super().__init__(family.value)


def _error(value: str | ManifestCarrierSuccessorFailureFamily):
    family = (
        value
        if isinstance(value, ManifestCarrierSuccessorFailureFamily)
        else ManifestCarrierSuccessorFailureFamily(value)
    )
    raise ManifestCarrierSuccessorError(family)


def _owned(raw: bytes) -> bytes:
    return bytes(bytearray(raw))


def _doc(raw: bytes) -> dict[str, object]:
    value = json.loads(raw)
    canonical = canonical_json_bytes(value)
    if type(value) is not dict or raw not in {canonical, canonical + b"\n"}:
        _error(
            ManifestCarrierSuccessorFailureFamily.MANIFEST_CARRIER_PROJECTION_CLAIM_REJECTED
        )
    return value


def _evidence_document(coordinates: Mapping[str, object]) -> dict[str, object]:
    continuity_document = _doc(coordinates["continuity_bytes"])
    application = _doc(coordinates["application_admission_bytes"])
    request_provenance = _doc(coordinates["request_provenance_bytes"])
    value = {
        "artifact_kind": "DERIVATION_EVIDENCE",
        "schema_version": "0.3",
        "canonicalization_profile": "veritrail-json-c14n/1",
        "derivation_id": continuity_document["derivation_id"],
        "request_provenance": request_provenance,
        **copy.deepcopy(continuity_document["input_digests"]),
        "terminal_branch": continuity_document["terminal_branch"],
        "selector_route": continuity_document["selector_route"],
        "continuity_variant": continuity_document["continuity_variant"],
        "continuity_digest": continuity_document["continuity_digest"],
        "application_admission_digest": application[
            "application_admission_digest"
        ],
        "coverage_ledger_digest": application["coverage_ledger_digest"],
        "root_chain_digest": application["root_chain_digest"],
    }
    value["derivation_evidence_digest"] = semantic_digest(
        EVIDENCE_IDENTITY_DOMAIN, value
    )
    return value


def _project_file_entries(
    coordinates: Mapping[str, object], evidence_bytes: bytes
) -> tuple[dict[str, object], ...]:
    result = _doc(coordinates["result_bytes"])
    transition = (
        None
        if coordinates["transition_bytes"] is None
        else _doc(coordinates["transition_bytes"])
    )
    if coordinates["result_kind"] == "NORMAL_REVIEW_SLICE_COVERAGE":
        if transition is None:
            _error(
                ManifestCarrierSuccessorFailureFamily.MANIFEST_CARRIER_PROJECTION_CLAIM_REJECTED
            )
        ledger = result["coverage_ledger"]
        children = {
            "FACT_SET": transition["fact_set"],
            "RELATION_SET": transition["relation_set"],
        }
        if result["review_slice_set"] is not None:
            children["REVIEW_SLICE_SET"] = result["review_slice_set"]
    elif coordinates["result_kind"] == "NEGATIVE_WORLD_COVERAGE":
        if transition is not None:
            _error(
                ManifestCarrierSuccessorFailureFamily.MANIFEST_CARRIER_PROJECTION_CLAIM_REJECTED
            )
        ledger = result
        children = {}
    else:
        _error(
            ManifestCarrierSuccessorFailureFamily.MANIFEST_CARRIER_PROJECTION_CLAIM_REJECTED
        )
    raw_by_role = {
        "SOURCE_SNAPSHOT": coordinates["source_snapshot_bytes"],
        "REVIEW_POLICY": coordinates["review_policy_bytes"],
        "DERIVATION_PROFILE": coordinates["derivation_profile_bytes"],
        "DERIVATION_EVIDENCE": evidence_bytes,
        **{
            role: canonical_json_bytes(document)
            for role, document in children.items()
        },
        "COVERAGE_LEDGER": canonical_json_bytes(ledger),
    }
    entries = []
    for role, path, digest_key in _ROLE_PATHS:
        raw = raw_by_role.get(role)
        if raw is None:
            continue
        document = _doc(raw)
        entries.append(
            {
                "role": role,
                "path": path,
                "bytes": _owned(raw),
                "semantic_digest": document[digest_key],
            }
        )
    return tuple(entries)


def _coordinate_seal(coordinates: Mapping[str, object]) -> dict[str, object]:
    byte_keys = (
        "continuity_bytes",
        "source_snapshot_bytes",
        "review_policy_bytes",
        "derivation_profile_bytes",
        "request_provenance_bytes",
        "terminal_source_bytes",
        "transition_bytes",
        "result_bytes",
        "application_admission_bytes",
        "attempt_binding_bytes",
    )
    return {
        "result_kind": coordinates["result_kind"],
        "byte_sha256": {
            key: (
                None
                if coordinates[key] is None
                else hashlib.sha256(coordinates[key]).hexdigest()
            )
            for key in byte_keys
        },
    }


def _file_snapshot_seal(
    file_entries: tuple[dict[str, object], ...],
    file_records: tuple[dict[str, object], ...],
) -> str:
    return semantic_digest(
        OWNED_SNAPSHOT_IDENTITY_DOMAIN,
        {
            "entries": [
                {
                    "role": item["role"],
                    "path": item["path"],
                    "raw_sha256": hashlib.sha256(item["bytes"]).hexdigest(),
                    "size_bytes": len(item["bytes"]),
                    "semantic_digest": item["semantic_digest"],
                }
                for item in file_entries
            ],
            "records": copy.deepcopy(list(file_records)),
        },
    )


def _claim_snapshot_seal(
    *,
    evidence_bytes: bytes,
    coordinate_seal: Mapping[str, object],
    file_entries: tuple[dict[str, object], ...],
) -> str:
    return semantic_digest(
        OWNED_SNAPSHOT_IDENTITY_DOMAIN,
        {
            "evidence_raw_sha256": hashlib.sha256(evidence_bytes).hexdigest(),
            "coordinate_seal": copy.deepcopy(dict(coordinate_seal)),
            "entries": [
                {
                    "role": item["role"],
                    "path": item["path"],
                    "raw_sha256": hashlib.sha256(item["bytes"]).hexdigest(),
                    "size_bytes": len(item["bytes"]),
                    "semantic_digest": item["semantic_digest"],
                }
                for item in file_entries
            ],
        },
    )


def _candidate_snapshot_seal(
    *,
    continuity_bytes: bytes,
    application_admission_bytes: bytes,
    attempt_binding_bytes: bytes,
    coordinate_seal: Mapping[str, object],
    file_entries: tuple[dict[str, object], ...],
    file_records: tuple[dict[str, object], ...],
) -> str:
    return semantic_digest(
        OWNED_SNAPSHOT_IDENTITY_DOMAIN,
        {
            "continuity_raw_sha256": hashlib.sha256(continuity_bytes).hexdigest(),
            "application_admission_raw_sha256": hashlib.sha256(
                application_admission_bytes
            ).hexdigest(),
            "attempt_binding_raw_sha256": hashlib.sha256(
                attempt_binding_bytes
            ).hexdigest(),
            "coordinate_seal": copy.deepcopy(dict(coordinate_seal)),
            "file_snapshot_seal": _file_snapshot_seal(
                file_entries, file_records
            ),
        },
    )


class ManifestCarrierProjectionClaim:
    def __init__(
        self,
        *,
        exact_continuity: continuity.CommittedSameAttemptDerivationEvidenceContinuity,
        coordinates: Mapping[str, object],
        evidence_bytes: bytes,
        file_entries: tuple[dict[str, object], ...],
        _token: object,
    ) -> None:
        if (
            _token is not _CLAIM_TOKEN
            or type(exact_continuity)
            is not continuity.CommittedSameAttemptDerivationEvidenceContinuity
        ):
            _error(
                ManifestCarrierSuccessorFailureFamily.MANIFEST_CARRIER_PROJECTION_CLAIM_REJECTED
            )
        self.__continuity = exact_continuity
        self.__bound_continuity = exact_continuity
        self.__coordinates = dict(coordinates)
        self.__bound_coordinates = self.__coordinates
        self.__evidence_bytes = evidence_bytes
        self.__bound_evidence_bytes = evidence_bytes
        self.__file_entries = file_entries
        self.__bound_file_entries = file_entries
        self.__coordinate_seal = _coordinate_seal(coordinates)
        self.__owned_snapshot_seal = _claim_snapshot_seal(
            evidence_bytes=self.__evidence_bytes,
            coordinate_seal=self.__coordinate_seal,
            file_entries=self.__file_entries,
        )
        self.__bound_owned_snapshot_seal = self.__owned_snapshot_seal
        self.__claimed = False
        self.__lock = threading.Lock()

    def __copy__(self):
        _error(
            ManifestCarrierSuccessorFailureFamily.MANIFEST_CARRIER_PROJECTION_CLAIM_REJECTED
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

    def _claim_candidate_material(self) -> dict[str, object]:
        with self.__lock:
            if self.__claimed:
                _error(
                    ManifestCarrierSuccessorFailureFamily.MANIFEST_CARRIER_PROJECTION_CLAIM_REJECTED
                )
            self.__claimed = True
        if (
            self.__continuity is not self.__bound_continuity
            or self.__coordinates is not self.__bound_coordinates
            or self.__evidence_bytes is not self.__bound_evidence_bytes
            or self.__file_entries is not self.__bound_file_entries
            or self.__owned_snapshot_seal is not self.__bound_owned_snapshot_seal
            or _claim_snapshot_seal(
                evidence_bytes=self.__evidence_bytes,
                coordinate_seal=self.__coordinate_seal,
                file_entries=self.__file_entries,
            )
            != self.__owned_snapshot_seal
        ):
            _error(
                ManifestCarrierSuccessorFailureFamily.MANIFEST_CARRIER_SNAPSHOT_MUTATION_REJECTED
            )
        try:
            current = self.__continuity._manifest_carrier_successor_coordinates()
        except continuity.SameAttemptDerivationEvidenceContinuityError as exc:
            family = (
                ManifestCarrierSuccessorFailureFamily.MANIFEST_CARRIER_CONTEXT_REVOKED
                if exc.failure_family
                is continuity.EvidenceContinuityFailureFamily.EVIDENCE_CONTINUITY_CONTEXT_REVOKED
                else ManifestCarrierSuccessorFailureFamily.MANIFEST_CARRIER_SAME_ATTEMPT_REJECTED
            )
            raise ManifestCarrierSuccessorError(family) from exc
        if (
            _coordinate_seal(current) != self.__coordinate_seal
            or current["coverage_ledger_conformance_source"]
            is not self.__coordinates["coverage_ledger_conformance_source"]
        ):
            _error(
                ManifestCarrierSuccessorFailureFamily.MANIFEST_CARRIER_SAME_ATTEMPT_REJECTED
            )
        return {
            "exact_continuity": self.__continuity,
            "coordinates": self.__coordinates,
            "evidence_bytes": self.__evidence_bytes,
            "file_entries": self.__file_entries,
            "coordinate_seal": self.__coordinate_seal,
        }


class CandidateState(str, Enum):
    PENDING = "PENDING"
    VALIDATING = "VALIDATING"
    VALIDATED = "VALIDATED"
    ADMITTED = "ADMITTED"
    REVOKED = "REVOKED"


class ManifestCarrierSuccessorCandidate:
    def __init__(self, material: Mapping[str, object], *, _token: object) -> None:
        if _token is not _CANDIDATE_TOKEN:
            _error(
                ManifestCarrierSuccessorFailureFamily.MANIFEST_CARRIER_PROJECTION_CLAIM_REJECTED
            )
        self.__continuity = material["exact_continuity"]
        self.__bound_continuity = self.__continuity
        coordinates = material["coordinates"]
        self.__continuity_bytes = _owned(coordinates["continuity_bytes"])
        self.__application_admission_bytes = _owned(
            coordinates["application_admission_bytes"]
        )
        self.__attempt_binding_bytes = _owned(coordinates["attempt_binding_bytes"])
        self.__conformance_source = coordinates[
            "coverage_ledger_conformance_source"
        ]
        self.__bound_conformance_source = self.__conformance_source
        self.__file_entries = tuple(
            {
                "role": item["role"],
                "path": item["path"],
                "bytes": _owned(item["bytes"]),
                "semantic_digest": item["semantic_digest"],
            }
            for item in material["file_entries"]
        )
        self.__bound_file_entries = self.__file_entries
        self.__file_records = tuple(
            {
                "role": item["role"],
                "path": item["path"],
                "raw_sha256": hashlib.sha256(item["bytes"]).hexdigest(),
                "size_bytes": len(item["bytes"]),
                "semantic_digest": item["semantic_digest"],
            }
            for item in self.__file_entries
        )
        self.__bound_file_records = self.__file_records
        self.__bound_continuity_bytes = self.__continuity_bytes
        self.__bound_application_admission_bytes = (
            self.__application_admission_bytes
        )
        self.__bound_attempt_binding_bytes = self.__attempt_binding_bytes
        self.__coordinate_seal = copy.deepcopy(material["coordinate_seal"])
        self.__bound_coordinate_seal = self.__coordinate_seal
        self.__owned_snapshot_seal = _candidate_snapshot_seal(
            continuity_bytes=self.__continuity_bytes,
            application_admission_bytes=self.__application_admission_bytes,
            attempt_binding_bytes=self.__attempt_binding_bytes,
            coordinate_seal=self.__coordinate_seal,
            file_entries=self.__file_entries,
            file_records=self.__file_records,
        )
        self.__bound_owned_snapshot_seal = self.__owned_snapshot_seal
        identity_projection = {
            "coordinate_seal": self.__coordinate_seal,
            "files": list(self.__file_records),
        }
        self.__candidate_digest = semantic_digest(
            CANDIDATE_IDENTITY_DOMAIN, identity_projection
        )
        self.__state = CandidateState.PENDING
        self.__lock = threading.Lock()
        self.__validation = None

    @property
    def state(self) -> CandidateState:
        with self.__lock:
            return self.__state

    def __copy__(self):
        with self.__lock:
            self.__state = CandidateState.REVOKED
        _error(
            ManifestCarrierSuccessorFailureFamily.MANIFEST_CARRIER_SNAPSHOT_MUTATION_REJECTED
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

    def _begin_validation(self) -> dict[str, object]:
        with self.__lock:
            if self.__state is not CandidateState.PENDING:
                _error(
                    ManifestCarrierSuccessorFailureFamily.MANIFEST_CARRIER_ALREADY_VALIDATED
                )
            self.__state = CandidateState.VALIDATING
            if (
                self.__continuity is not self.__bound_continuity
                or self.__continuity_bytes is not self.__bound_continuity_bytes
                or self.__application_admission_bytes
                is not self.__bound_application_admission_bytes
                or self.__attempt_binding_bytes
                is not self.__bound_attempt_binding_bytes
                or self.__conformance_source is not self.__bound_conformance_source
                or self.__file_entries is not self.__bound_file_entries
                or self.__file_records is not self.__bound_file_records
                or self.__coordinate_seal is not self.__bound_coordinate_seal
                or self.__owned_snapshot_seal
                is not self.__bound_owned_snapshot_seal
                or _candidate_snapshot_seal(
                    continuity_bytes=self.__continuity_bytes,
                    application_admission_bytes=(
                        self.__application_admission_bytes
                    ),
                    attempt_binding_bytes=self.__attempt_binding_bytes,
                    coordinate_seal=self.__coordinate_seal,
                    file_entries=self.__file_entries,
                    file_records=self.__file_records,
                )
                != self.__owned_snapshot_seal
            ):
                self.__state = CandidateState.REVOKED
                _error(
                    ManifestCarrierSuccessorFailureFamily.MANIFEST_CARRIER_SNAPSHOT_MUTATION_REJECTED
                )
        try:
            current = self.__continuity._manifest_carrier_successor_coordinates()
        except continuity.SameAttemptDerivationEvidenceContinuityError as exc:
            with self.__lock:
                self.__state = CandidateState.REVOKED
            family = (
                ManifestCarrierSuccessorFailureFamily.MANIFEST_CARRIER_CONTEXT_REVOKED
                if exc.failure_family
                is continuity.EvidenceContinuityFailureFamily.EVIDENCE_CONTINUITY_CONTEXT_REVOKED
                else ManifestCarrierSuccessorFailureFamily.MANIFEST_CARRIER_SAME_ATTEMPT_REJECTED
            )
            raise ManifestCarrierSuccessorError(family) from exc
        if (
            _coordinate_seal(current) != self.__coordinate_seal
            or current["coverage_ledger_conformance_source"]
            is not self.__conformance_source
        ):
            with self.__lock:
                self.__state = CandidateState.REVOKED
            _error(
                ManifestCarrierSuccessorFailureFamily.MANIFEST_CARRIER_SAME_ATTEMPT_REJECTED
            )
        return {
            "producer_projection_function": PROJECTION_FUNCTION,
            "independent_conformance_function": (
                conformance.INDEPENDENT_CONFORMANCE_FUNCTION
            ),
            "shared_expected_projector_state": False,
            "continuity_bytes": _owned(self.__continuity_bytes),
            "application_admission_bytes": _owned(
                self.__application_admission_bytes
            ),
            "attempt_binding_bytes": _owned(self.__attempt_binding_bytes),
            "coverage_ledger_conformance_source": self.__conformance_source,
            "file_entries": tuple(
                {
                    "role": item["role"],
                    "path": item["path"],
                    "bytes": _owned(item["bytes"]),
                    "semantic_digest": item["semantic_digest"],
                }
                for item in self.__file_entries
            ),
            "file_records": tuple(copy.deepcopy(self.__file_records)),
            "authority_ceiling": conformance.authority_ceiling_copy(),
        }

    def _validation_failed(self) -> None:
        with self.__lock:
            self.__state = CandidateState.REVOKED

    def _validation_succeeded(
        self, report: Mapping[str, object]
    ) -> "ManifestCarrierSuccessorValidation":
        with self.__lock:
            if self.__state is not CandidateState.VALIDATING:
                _error(
                    ManifestCarrierSuccessorFailureFamily.MANIFEST_CARRIER_ALREADY_VALIDATED
                )
            value = ManifestCarrierSuccessorValidation(
                candidate=self,
                candidate_digest=self.__candidate_digest,
                report=report,
                _token=_VALIDATION_TOKEN,
            )
            self.__validation = value
            self.__state = CandidateState.VALIDATED
            return value

    def _admit(
        self, validation: "ManifestCarrierSuccessorValidation"
    ) -> "AdmittedManifestCarrierSuccessor":
        with self.__lock:
            if _candidate_snapshot_seal(
                continuity_bytes=self.__continuity_bytes,
                application_admission_bytes=self.__application_admission_bytes,
                attempt_binding_bytes=self.__attempt_binding_bytes,
                coordinate_seal=self.__coordinate_seal,
                file_entries=self.__file_entries,
                file_records=self.__file_records,
            ) != self.__owned_snapshot_seal:
                self.__state = CandidateState.REVOKED
                _error(
                    ManifestCarrierSuccessorFailureFamily.MANIFEST_CARRIER_SNAPSHOT_MUTATION_REJECTED
                )
            if (
                self.__state is not CandidateState.VALIDATED
                or validation is not self.__validation
                or validation._candidate is not self
                or validation._candidate_digest != self.__candidate_digest
            ):
                _error(
                    ManifestCarrierSuccessorFailureFamily.MANIFEST_CARRIER_SAME_ATTEMPT_REJECTED
                )
            admitted = AdmittedManifestCarrierSuccessor(
                candidate=self,
                validation=validation,
                file_entries=self.__file_entries,
                file_records=self.__file_records,
                _token=_ADMISSION_TOKEN,
            )
            self.__state = CandidateState.ADMITTED
            return admitted


class ManifestCarrierSuccessorValidation:
    def __init__(
        self,
        *,
        candidate: ManifestCarrierSuccessorCandidate,
        candidate_digest: str,
        report: Mapping[str, object],
        _token: object,
    ) -> None:
        if _token is not _VALIDATION_TOKEN:
            _error(
                ManifestCarrierSuccessorFailureFamily.MANIFEST_CARRIER_COMMON_MODE_ORACLE_REJECTED
            )
        self._candidate = candidate
        self._candidate_digest = candidate_digest
        self.__report_bytes = canonical_json_bytes(dict(report))

    def report_copy(self) -> dict[str, object]:
        return json.loads(self.__report_bytes)

    def __copy__(self):
        _error(
            ManifestCarrierSuccessorFailureFamily.MANIFEST_CARRIER_COMMON_MODE_ORACLE_REJECTED
        )

    def __deepcopy__(self, _memo):
        return self.__copy__()


class AdmittedManifestCarrierSuccessor:
    def __init__(
        self,
        *,
        candidate: ManifestCarrierSuccessorCandidate,
        validation: ManifestCarrierSuccessorValidation,
        file_entries: tuple[dict[str, object], ...],
        file_records: tuple[dict[str, object], ...],
        _token: object,
    ) -> None:
        if _token is not _ADMISSION_TOKEN:
            _error(
                ManifestCarrierSuccessorFailureFamily.MANIFEST_CARRIER_SAME_ATTEMPT_REJECTED
            )
        self.__candidate = candidate
        self.__bound_candidate = candidate
        self.__validation = validation
        self.__bound_validation = validation
        self.__file_entries = tuple(
            {
                "role": item["role"],
                "path": item["path"],
                "bytes": _owned(item["bytes"]),
                "semantic_digest": item["semantic_digest"],
            }
            for item in file_entries
        )
        self.__bound_file_entries = self.__file_entries
        self.__file_records = tuple(copy.deepcopy(file_records))
        self.__bound_file_records = self.__file_records
        self.__owned_snapshot_seal = _file_snapshot_seal(
            self.__file_entries, self.__file_records
        )
        self.__bound_owned_snapshot_seal = self.__owned_snapshot_seal
        self.__consumed = False
        self.__lock = threading.Lock()
        report = validation.report_copy()
        self.__admission_digest = semantic_digest(
            ADMISSION_IDENTITY_DOMAIN,
            {
                "candidate_digest": validation._candidate_digest,
                "validation_digest": report["validation_digest"],
                "file_binding_digest": report["file_binding_digest"],
                "topology_proof_digest": report["topology_proof_digest"],
            },
        )

    def __copy__(self):
        _error(
            ManifestCarrierSuccessorFailureFamily.MANIFEST_CARRIER_SAME_ATTEMPT_REJECTED
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
    def admission_digest(self) -> str:
        if (
            self.__candidate is not self.__bound_candidate
            or self.__validation is not self.__bound_validation
            or self.__file_entries is not self.__bound_file_entries
            or self.__file_records is not self.__bound_file_records
            or self.__owned_snapshot_seal is not self.__bound_owned_snapshot_seal
            or _file_snapshot_seal(self.__file_entries, self.__file_records)
            != self.__owned_snapshot_seal
        ):
            _error(
                ManifestCarrierSuccessorFailureFamily.MANIFEST_CARRIER_SNAPSHOT_MUTATION_REJECTED
            )
        return self.__admission_digest

    def authority_ceiling_copy(self) -> dict[str, object]:
        self.admission_digest
        return conformance.authority_ceiling_copy()

    def claim_future_manifest_consumption(
        self,
    ) -> "ClaimedFutureManifestCarrierSnapshot":
        with self.__lock:
            if self.__consumed:
                _error(
                    ManifestCarrierSuccessorFailureFamily.MANIFEST_CARRIER_ALREADY_CONSUMED
                )
            self.__consumed = True
        self.admission_digest
        return ClaimedFutureManifestCarrierSnapshot(
            admission_digest=self.__admission_digest,
            file_entries=self.__file_entries,
            file_records=self.__file_records,
            validation_report=self.__validation.report_copy(),
            _token=_CONSUMPTION_TOKEN,
        )


class ClaimedFutureManifestCarrierSnapshot:
    def __init__(
        self,
        *,
        admission_digest: str,
        file_entries: tuple[dict[str, object], ...],
        file_records: tuple[dict[str, object], ...],
        validation_report: Mapping[str, object],
        _token: object,
    ) -> None:
        if _token is not _CONSUMPTION_TOKEN:
            _error(
                ManifestCarrierSuccessorFailureFamily.MANIFEST_CARRIER_ALREADY_CONSUMED
            )
        self.__admission_digest = admission_digest
        self.__entries = tuple(
            {
                "role": item["role"],
                "path": item["path"],
                "bytes": _owned(item["bytes"]),
                "semantic_digest": item["semantic_digest"],
            }
            for item in file_entries
        )
        self.__records = tuple(copy.deepcopy(file_records))
        self.__validation_bytes = canonical_json_bytes(dict(validation_report))
        self.__owned_snapshot_seal = semantic_digest(
            OWNED_SNAPSHOT_IDENTITY_DOMAIN,
            {
                "admission_digest": self.__admission_digest,
                "file_snapshot_seal": _file_snapshot_seal(
                    self.__entries, self.__records
                ),
                "validation_raw_sha256": hashlib.sha256(
                    self.__validation_bytes
                ).hexdigest(),
            },
        )

    def input_copy(self) -> dict[str, object]:
        if semantic_digest(
            OWNED_SNAPSHOT_IDENTITY_DOMAIN,
            {
                "admission_digest": self.__admission_digest,
                "file_snapshot_seal": _file_snapshot_seal(
                    self.__entries, self.__records
                ),
                "validation_raw_sha256": hashlib.sha256(
                    self.__validation_bytes
                ).hexdigest(),
            },
        ) != self.__owned_snapshot_seal:
            _error(
                ManifestCarrierSuccessorFailureFamily.MANIFEST_CARRIER_SNAPSHOT_MUTATION_REJECTED
            )
        file_bytes = {}
        for item in self.__entries:
            file_bytes[item["role"]] = _owned(item["bytes"])
        return {
            "consumption_identity": FUTURE_CONSUMPTION_IDENTITY,
            "admission_digest": self.__admission_digest,
            "files": copy.deepcopy(list(self.__records)),
            "file_bytes_by_role": file_bytes,
            "validation": json.loads(self.__validation_bytes),
            "authority_ceiling": conformance.authority_ceiling_copy(),
        }

    def __copy__(self):
        _error(
            ManifestCarrierSuccessorFailureFamily.MANIFEST_CARRIER_ALREADY_CONSUMED
        )

    def __deepcopy__(self, _memo):
        return self.__copy__()


def project_manifest_carrier_successor(
    value: continuity.CommittedSameAttemptDerivationEvidenceContinuity,
) -> ManifestCarrierProjectionClaim:
    if type(value) is not continuity.CommittedSameAttemptDerivationEvidenceContinuity:
        family = (
            ManifestCarrierSuccessorFailureFamily.MANIFEST_CARRIER_LEGACY_ALIAS_REJECTED
            if isinstance(value, Mapping)
            else ManifestCarrierSuccessorFailureFamily.MANIFEST_CARRIER_PROJECTION_CLAIM_REJECTED
        )
        raise ManifestCarrierSuccessorError(family)
    try:
        coordinates = value._manifest_carrier_successor_coordinates()
        evidence = _evidence_document(coordinates)
        evidence_bytes = canonical_json_bytes(evidence)
        entries = _project_file_entries(coordinates, evidence_bytes)
    except ManifestCarrierSuccessorError:
        raise
    except continuity.SameAttemptDerivationEvidenceContinuityError as exc:
        family = (
            ManifestCarrierSuccessorFailureFamily.MANIFEST_CARRIER_CONTEXT_REVOKED
            if exc.failure_family
            is continuity.EvidenceContinuityFailureFamily.EVIDENCE_CONTINUITY_CONTEXT_REVOKED
            else ManifestCarrierSuccessorFailureFamily.MANIFEST_CARRIER_SAME_ATTEMPT_REJECTED
        )
        raise ManifestCarrierSuccessorError(family) from exc
    except Exception as exc:
        raise ManifestCarrierSuccessorError(
            ManifestCarrierSuccessorFailureFamily.MANIFEST_CARRIER_PROJECTION_CLAIM_REJECTED
        ) from exc
    return ManifestCarrierProjectionClaim(
        exact_continuity=value,
        coordinates=coordinates,
        evidence_bytes=evidence_bytes,
        file_entries=entries,
        _token=_CLAIM_TOKEN,
    )


def build_manifest_carrier_successor_candidate(
    claim: ManifestCarrierProjectionClaim,
) -> ManifestCarrierSuccessorCandidate:
    if type(claim) is not ManifestCarrierProjectionClaim:
        _error(
            ManifestCarrierSuccessorFailureFamily.MANIFEST_CARRIER_PROJECTION_CLAIM_REJECTED
        )
    return ManifestCarrierSuccessorCandidate(
        claim._claim_candidate_material(), _token=_CANDIDATE_TOKEN
    )


def independently_validate_manifest_carrier_successor_candidate(
    candidate: ManifestCarrierSuccessorCandidate,
) -> ManifestCarrierSuccessorValidation:
    if type(candidate) is not ManifestCarrierSuccessorCandidate:
        _error(
            ManifestCarrierSuccessorFailureFamily.MANIFEST_CARRIER_PROJECTION_CLAIM_REJECTED
        )
    snapshot = candidate._begin_validation()
    try:
        report = conformance.validate_manifest_carrier_successor_snapshot(snapshot)
    except conformance.IndependentCarrierConformanceFailure as exc:
        candidate._validation_failed()
        raise ManifestCarrierSuccessorError(
            ManifestCarrierSuccessorFailureFamily(exc.family)
        ) from exc
    except Exception as exc:
        candidate._validation_failed()
        raise ManifestCarrierSuccessorError(
            ManifestCarrierSuccessorFailureFamily.MANIFEST_CARRIER_COMMON_MODE_ORACLE_REJECTED
        ) from exc
    return candidate._validation_succeeded(report)


def admit_manifest_carrier_successor_candidate(
    candidate: ManifestCarrierSuccessorCandidate,
    validation: ManifestCarrierSuccessorValidation,
) -> AdmittedManifestCarrierSuccessor:
    if (
        type(candidate) is not ManifestCarrierSuccessorCandidate
        or type(validation) is not ManifestCarrierSuccessorValidation
    ):
        _error(
            ManifestCarrierSuccessorFailureFamily.MANIFEST_CARRIER_SAME_ATTEMPT_REJECTED
        )
    return candidate._admit(validation)
