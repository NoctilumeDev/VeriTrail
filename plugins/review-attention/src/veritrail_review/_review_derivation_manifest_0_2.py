"""Bounded private Review Derivation Manifest 0.2 implementation.

The implementation consumes one frozen carrier snapshot, produces one exact
private candidate, admits only independently validated canonical bytes, and can
copy those bytes into caller-owned staging.  It has no filesystem publisher,
public Bundle, Evidence, CLI, Workbench, persistence, Verdict, or disposition
authority.
"""

from __future__ import annotations

import copy
import hashlib
import json
import threading
import weakref
from enum import Enum
from typing import Mapping

from veritrail_review import (
    _derivation_evidence_manifest_carrier_successor as carrier,
)
from veritrail_review import (
    _review_derivation_manifest_0_2_conformance as conformance,
)
from veritrail_review.canonical import canonical_json_bytes, semantic_digest


PROJECTION_IDENTITY = "r1-review-derivation-manifest-0.2-projection/0.1"
ADMISSION_DOMAIN = "veritrail.review.derivation-manifest-0.2-admission/0.1"
PUBLICATION_RECEIPT_DOMAIN = (
    "veritrail.review.derivation-manifest-0.2-private-staging/0.1"
)
PRIVATE_STAGING_IDENTITY = (
    "r1-review-derivation-manifest-0.2-private-caller-staging/0.1"
)
CARRIER_CONSUMPTION_IDENTITY = (
    "r1-future-manifest-carrier-consumption-input/0.1"
)

_ROLE_ORDER = (
    "SOURCE_SNAPSHOT",
    "REVIEW_POLICY",
    "DERIVATION_PROFILE",
    "DERIVATION_EVIDENCE",
    "FACT_SET",
    "RELATION_SET",
    "REVIEW_SLICE_SET",
    "COVERAGE_LEDGER",
)
_CARRIER_AUTHORITY_CEILING = {
    "private_copy_owned_manifest_carrier_successor": True,
    "future_manifest_consumption_one_shot": True,
    "manifest_created": False,
    "persistence": False,
    "public_review": False,
    "truth": False,
    "sufficiency": False,
    "core_verdict": False,
    "global_composition_authority": False,
    "r2_r6": False,
}

_VALIDATION_TOKEN = object()
_ADMISSION_TOKEN = object()
_RECEIPT_TOKEN = object()
_CANDIDATE_TOKEN = object()
_OPPORTUNITY_LOCK = threading.Lock()
_CLAIMED_OPPORTUNITIES: weakref.WeakKeyDictionary[
    carrier.ClaimedFutureManifestCarrierSnapshot, bool
] = weakref.WeakKeyDictionary()


class ManifestSchemaVersion(str, Enum):
    V0_1 = "0.1"
    V0_2 = "0.2"


class Manifest02FailureFamily(str, Enum):
    UNKNOWN_SCHEMA_VERSION = "UNKNOWN_SCHEMA_VERSION"
    MANIFEST_0_2_CONSTRUCTION_OPPORTUNITY_CONSUMED = (
        "MANIFEST_0_2_CONSTRUCTION_OPPORTUNITY_CONSUMED"
    )
    MANIFEST_0_2_CARRIER_INPUT_REJECTED = (
        "MANIFEST_0_2_CARRIER_INPUT_REJECTED"
    )
    MANIFEST_0_2_SNAPSHOT_REJECTED = "MANIFEST_0_2_SNAPSHOT_REJECTED"
    MANIFEST_0_2_SHAPE_REJECTED = "MANIFEST_0_2_SHAPE_REJECTED"
    MANIFEST_0_2_VERSION_OR_SHAPE_REJECTED = (
        "MANIFEST_0_2_VERSION_OR_SHAPE_REJECTED"
    )
    MANIFEST_0_2_CARRIER_RECORD_REJECTED = (
        "MANIFEST_0_2_CARRIER_RECORD_REJECTED"
    )
    MANIFEST_0_2_CHILD_BINDING_REJECTED = (
        "MANIFEST_0_2_CHILD_BINDING_REJECTED"
    )
    MANIFEST_0_2_ROLE_PATH_REJECTED = "MANIFEST_0_2_ROLE_PATH_REJECTED"
    MANIFEST_0_2_TOPOLOGY_REJECTED = "MANIFEST_0_2_TOPOLOGY_REJECTED"
    MANIFEST_0_2_ROOT_TOPOLOGY_REJECTED = (
        "MANIFEST_0_2_ROOT_TOPOLOGY_REJECTED"
    )
    MANIFEST_0_2_LEDGER_CONFORMANCE_REJECTED = (
        "MANIFEST_0_2_LEDGER_CONFORMANCE_REJECTED"
    )
    MANIFEST_0_2_LEDGER_PRIOR_CONFORMANCE_REJECTED = (
        "MANIFEST_0_2_LEDGER_PRIOR_CONFORMANCE_REJECTED"
    )
    MANIFEST_0_2_COMMON_MODE_OR_AUTHORITY_REJECTED = (
        "MANIFEST_0_2_COMMON_MODE_OR_AUTHORITY_REJECTED"
    )
    MANIFEST_0_2_ALREADY_VALIDATED = "MANIFEST_0_2_ALREADY_VALIDATED"
    MANIFEST_0_2_ADMISSION_REJECTED = "MANIFEST_0_2_ADMISSION_REJECTED"
    MANIFEST_0_2_SNAPSHOT_MUTATION_REJECTED = (
        "MANIFEST_0_2_SNAPSHOT_MUTATION_REJECTED"
    )
    MANIFEST_0_2_PRIVATE_STAGING_REJECTED = (
        "MANIFEST_0_2_PRIVATE_STAGING_REJECTED"
    )
    MANIFEST_0_2_PRIVATE_STAGING_ALREADY_USED = (
        "MANIFEST_0_2_PRIVATE_STAGING_ALREADY_USED"
    )


class Manifest02Error(ValueError):
    def __init__(self, family: Manifest02FailureFamily) -> None:
        self.failure_family = family
        super().__init__(family.value)


def _error(value: str | Manifest02FailureFamily):
    family = (
        value
        if isinstance(value, Manifest02FailureFamily)
        else Manifest02FailureFamily(value)
    )
    raise Manifest02Error(family)


def _owned(raw: bytes) -> bytes:
    return bytes(bytearray(raw))


def _document(raw: object) -> dict[str, object]:
    if type(raw) is not bytes:
        _error(Manifest02FailureFamily.MANIFEST_0_2_SHAPE_REJECTED)
    try:
        value = json.loads(raw)
    except (TypeError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise Manifest02Error(
            Manifest02FailureFamily.MANIFEST_0_2_SHAPE_REJECTED
        ) from exc
    if type(value) is not dict or raw not in {
        canonical_json_bytes(value),
        canonical_json_bytes(value) + b"\n",
    }:
        _error(Manifest02FailureFamily.MANIFEST_0_2_SHAPE_REJECTED)
    return value


def dispatch_review_derivation_manifest_version(
    raw: bytes,
) -> ManifestSchemaVersion:
    """Select only an exact known version; never choose a closest fallback."""

    value = _document(raw)
    version = value.get("schema_version")
    if version == ManifestSchemaVersion.V0_1.value:
        return ManifestSchemaVersion.V0_1
    if version == ManifestSchemaVersion.V0_2.value:
        return ManifestSchemaVersion.V0_2
    _error(Manifest02FailureFamily.UNKNOWN_SCHEMA_VERSION)


def _input_snapshot_digest(value: Mapping[str, object]) -> str:
    return semantic_digest(
        conformance.INPUT_SNAPSHOT_DOMAIN,
        {
            "carrier_admission_digest": value["admission_digest"],
            "carrier_validation_digest": value["validation"][
                "validation_digest"
            ],
            "manifest_raw_sha256": hashlib.sha256(
                value["manifest_bytes"]
            ).hexdigest(),
            "records": copy.deepcopy(list(value["records"])),
        },
    )


def _claim_carrier_input(
    value: carrier.ClaimedFutureManifestCarrierSnapshot,
) -> dict[str, object]:
    if type(value) is not carrier.ClaimedFutureManifestCarrierSnapshot:
        _error(Manifest02FailureFamily.MANIFEST_0_2_CARRIER_INPUT_REJECTED)
    with _OPPORTUNITY_LOCK:
        if value in _CLAIMED_OPPORTUNITIES:
            _error(
                Manifest02FailureFamily.
                MANIFEST_0_2_CONSTRUCTION_OPPORTUNITY_CONSUMED
            )
        _CLAIMED_OPPORTUNITIES[value] = True
    try:
        consumed = value.input_copy()
    except Exception as exc:
        raise Manifest02Error(
            Manifest02FailureFamily.MANIFEST_0_2_CARRIER_INPUT_REJECTED
        ) from exc
    if (
        type(consumed) is not dict
        or set(consumed)
        != {
            "consumption_identity",
            "admission_digest",
            "files",
            "file_bytes_by_role",
            "validation",
            "authority_ceiling",
        }
        or consumed.get("consumption_identity")
        != CARRIER_CONSUMPTION_IDENTITY
        or consumed.get("authority_ceiling") != _CARRIER_AUTHORITY_CEILING
        or type(consumed.get("files")) is not list
        or type(consumed.get("file_bytes_by_role")) is not dict
        or type(consumed.get("validation")) is not dict
    ):
        _error(Manifest02FailureFamily.MANIFEST_0_2_CARRIER_INPUT_REJECTED)
    return consumed


def _project_manifest(consumed: Mapping[str, object]) -> bytes:
    records = consumed["files"]
    roles = [item.get("role") for item in records]
    if (
        len(roles) != len(set(roles))
        or roles != [role for role in _ROLE_ORDER if role in roles]
        or tuple(roles[:4]) != _ROLE_ORDER[:4]
        or roles[-1:] != ["COVERAGE_LEDGER"]
    ):
        _error(Manifest02FailureFamily.MANIFEST_0_2_CARRIER_INPUT_REJECTED)
    manifest = {
        "bundle_kind": "R1_DERIVATION",
        "schema_version": "0.2",
        "canonicalization_profile": "veritrail-json-c14n/1",
        "outcome_kind": "COVERAGE",
        "files": [
            {
                "role": item["role"],
                "path": item["path"],
                "sha256": item["raw_sha256"],
                "size_bytes": item["size_bytes"],
                "semantic_digest": item["semantic_digest"],
            }
            for item in records
        ],
    }
    return canonical_json_bytes(manifest)


class CandidateState(str, Enum):
    PENDING = "PENDING"
    VALIDATING = "VALIDATING"
    VALIDATED = "VALIDATED"
    ADMITTED = "ADMITTED"
    REVOKED = "REVOKED"


class ReviewDerivationManifest02Candidate:
    def __init__(
        self,
        *,
        manifest_bytes: bytes,
        consumed: Mapping[str, object],
        _token: object,
    ) -> None:
        if _token is not _CANDIDATE_TOKEN:
            _error(
                Manifest02FailureFamily.MANIFEST_0_2_CARRIER_INPUT_REJECTED
            )
        self.__manifest_bytes = _owned(manifest_bytes)
        self.__bound_manifest_bytes = self.__manifest_bytes
        self.__carrier_admission_digest = consumed["admission_digest"]
        self.__records = tuple(copy.deepcopy(consumed["files"]))
        self.__bound_records = self.__records
        self.__bytes_by_role = {
            role: _owned(raw)
            for role, raw in consumed["file_bytes_by_role"].items()
        }
        self.__bound_bytes_by_role = self.__bytes_by_role
        self.__validation = copy.deepcopy(consumed["validation"])
        self.__bound_validation = self.__validation
        self.__input_snapshot_digest = _input_snapshot_digest(
            {
                "admission_digest": self.__carrier_admission_digest,
                "validation": self.__validation,
                "manifest_bytes": self.__manifest_bytes,
                "records": self.__records,
            }
        )
        self.__bound_input_snapshot_digest = self.__input_snapshot_digest
        self.__state = CandidateState.PENDING
        self.__validation_object = None
        self.__lock = threading.Lock()

    @property
    def state(self) -> CandidateState:
        with self.__lock:
            return self.__state

    def __copy__(self):
        with self.__lock:
            self.__state = CandidateState.REVOKED
        _error(
            Manifest02FailureFamily.MANIFEST_0_2_SNAPSHOT_MUTATION_REJECTED
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

    def _current_snapshot_digest(self) -> str:
        return _input_snapshot_digest(
            {
                "admission_digest": self.__carrier_admission_digest,
                "validation": self.__validation,
                "manifest_bytes": self.__manifest_bytes,
                "records": self.__records,
            }
        )

    def _begin_validation(self) -> dict[str, object]:
        with self.__lock:
            if self.__state is not CandidateState.PENDING:
                _error(Manifest02FailureFamily.MANIFEST_0_2_ALREADY_VALIDATED)
            self.__state = CandidateState.VALIDATING
            if (
                self.__manifest_bytes is not self.__bound_manifest_bytes
                or self.__records is not self.__bound_records
                or self.__bytes_by_role is not self.__bound_bytes_by_role
                or self.__validation is not self.__bound_validation
                or self.__input_snapshot_digest
                is not self.__bound_input_snapshot_digest
                or self._current_snapshot_digest()
                != self.__input_snapshot_digest
            ):
                self.__state = CandidateState.REVOKED
                _error(
                    Manifest02FailureFamily.
                    MANIFEST_0_2_SNAPSHOT_MUTATION_REJECTED
                )
        return {
            "producer_identity": PROJECTION_IDENTITY,
            "conformance_identity": conformance.CONFORMANCE_IDENTITY,
            "shared_expected_projector_state": False,
            "manifest_bytes": _owned(self.__manifest_bytes),
            "carrier_admission_digest": self.__carrier_admission_digest,
            "carrier_records": tuple(copy.deepcopy(self.__records)),
            "carrier_bytes_by_role": {
                role: _owned(raw)
                for role, raw in self.__bytes_by_role.items()
            },
            "carrier_validation": copy.deepcopy(self.__validation),
            "input_snapshot_digest": self.__input_snapshot_digest,
            "authority_ceiling": conformance.authority_ceiling_copy(),
        }

    def _validation_failed(self) -> None:
        with self.__lock:
            self.__state = CandidateState.REVOKED

    def _validation_succeeded(
        self, report: Mapping[str, object]
    ) -> "ReviewDerivationManifest02Validation":
        with self.__lock:
            if self.__state is not CandidateState.VALIDATING:
                _error(
                    Manifest02FailureFamily.MANIFEST_0_2_ALREADY_VALIDATED
                )
            value = ReviewDerivationManifest02Validation(
                candidate=self,
                report=report,
                _token=_VALIDATION_TOKEN,
            )
            self.__validation_object = value
            self.__state = CandidateState.VALIDATED
            return value

    def _admit(
        self, validation: "ReviewDerivationManifest02Validation"
    ) -> "AdmittedReviewDerivationManifest02":
        with self.__lock:
            if (
                self.__state is not CandidateState.VALIDATED
                or validation is not self.__validation_object
                or validation._candidate is not self
                or self._current_snapshot_digest()
                != self.__input_snapshot_digest
            ):
                _error(Manifest02FailureFamily.MANIFEST_0_2_ADMISSION_REJECTED)
            admitted = AdmittedReviewDerivationManifest02(
                candidate=self,
                validation=validation,
                manifest_bytes=self.__manifest_bytes,
                _token=_ADMISSION_TOKEN,
            )
            self.__state = CandidateState.ADMITTED
            return admitted


class ReviewDerivationManifest02Validation:
    def __init__(
        self,
        *,
        candidate: ReviewDerivationManifest02Candidate,
        report: Mapping[str, object],
        _token: object,
    ) -> None:
        if _token is not _VALIDATION_TOKEN:
            _error(Manifest02FailureFamily.MANIFEST_0_2_ADMISSION_REJECTED)
        self._candidate = candidate
        self.__report_bytes = canonical_json_bytes(dict(report))

    def report_copy(self) -> dict[str, object]:
        return json.loads(self.__report_bytes)

    def __copy__(self):
        _error(Manifest02FailureFamily.MANIFEST_0_2_ADMISSION_REJECTED)

    def __deepcopy__(self, _memo):
        return self.__copy__()


class AdmittedReviewDerivationManifest02:
    def __init__(
        self,
        *,
        candidate: ReviewDerivationManifest02Candidate,
        validation: ReviewDerivationManifest02Validation,
        manifest_bytes: bytes,
        _token: object,
    ) -> None:
        if _token is not _ADMISSION_TOKEN:
            _error(Manifest02FailureFamily.MANIFEST_0_2_ADMISSION_REJECTED)
        self.__candidate = candidate
        self.__bound_candidate = candidate
        self.__validation = validation
        self.__bound_validation = validation
        self.__manifest_bytes = _owned(manifest_bytes)
        self.__bound_manifest_bytes = self.__manifest_bytes
        report = validation.report_copy()
        self.__admission_digest = semantic_digest(
            ADMISSION_DOMAIN,
            {
                "manifest_raw_sha256": report["manifest_raw_sha256"],
                "carrier_admission_digest": report[
                    "carrier_admission_digest"
                ],
                "validation_digest": report["validation_digest"],
            },
        )
        self.__publication_used = False
        self.__lock = threading.Lock()

    def __copy__(self):
        _error(Manifest02FailureFamily.MANIFEST_0_2_ADMISSION_REJECTED)

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
            or self.__manifest_bytes is not self.__bound_manifest_bytes
            or hashlib.sha256(self.__manifest_bytes).hexdigest()
            != self.__validation.report_copy()["manifest_raw_sha256"]
        ):
            _error(
                Manifest02FailureFamily.
                MANIFEST_0_2_SNAPSHOT_MUTATION_REJECTED
            )
        return self.__admission_digest

    def _manifest_copy(self) -> bytes:
        self.admission_digest
        return _owned(self.__manifest_bytes)

    def _claim_private_publication(self) -> bytes:
        with self.__lock:
            if self.__publication_used:
                _error(
                    Manifest02FailureFamily.
                    MANIFEST_0_2_PRIVATE_STAGING_ALREADY_USED
                )
            self.__publication_used = True
        return self._manifest_copy()


class PrivateManifest02StagingReceipt:
    def __init__(
        self,
        *,
        admission_digest: str,
        raw: bytes,
        _token: object,
    ) -> None:
        if _token is not _RECEIPT_TOKEN:
            _error(
                Manifest02FailureFamily.MANIFEST_0_2_PRIVATE_STAGING_REJECTED
            )
        self.__document = {
            "staging_identity": PRIVATE_STAGING_IDENTITY,
            "path": "manifest.json",
            "admission_digest": admission_digest,
            "raw_sha256": hashlib.sha256(raw).hexdigest(),
            "size_bytes": len(raw),
        }
        self.__document["receipt_digest"] = semantic_digest(
            PUBLICATION_RECEIPT_DOMAIN, self.__document
        )

    def receipt_copy(self) -> dict[str, object]:
        return copy.deepcopy(self.__document)


def build_review_derivation_manifest_0_2_candidate(
    value: carrier.ClaimedFutureManifestCarrierSnapshot,
) -> ReviewDerivationManifest02Candidate:
    consumed = _claim_carrier_input(value)
    try:
        manifest_bytes = _project_manifest(consumed)
    except Manifest02Error:
        raise
    except Exception as exc:
        raise Manifest02Error(
            Manifest02FailureFamily.MANIFEST_0_2_CARRIER_INPUT_REJECTED
        ) from exc
    return ReviewDerivationManifest02Candidate(
        manifest_bytes=manifest_bytes,
        consumed=consumed,
        _token=_CANDIDATE_TOKEN,
    )


def independently_validate_review_derivation_manifest_0_2_candidate(
    candidate: ReviewDerivationManifest02Candidate,
) -> ReviewDerivationManifest02Validation:
    if type(candidate) is not ReviewDerivationManifest02Candidate:
        _error(Manifest02FailureFamily.MANIFEST_0_2_SNAPSHOT_REJECTED)
    snapshot = candidate._begin_validation()
    try:
        report = conformance.validate_review_derivation_manifest_0_2_snapshot(
            snapshot
        )
    except conformance.Manifest02ConformanceFailure as exc:
        candidate._validation_failed()
        raise Manifest02Error(Manifest02FailureFamily(exc.family)) from exc
    except Exception as exc:
        candidate._validation_failed()
        raise Manifest02Error(
            Manifest02FailureFamily.
            MANIFEST_0_2_COMMON_MODE_OR_AUTHORITY_REJECTED
        ) from exc
    return candidate._validation_succeeded(report)


def admit_review_derivation_manifest_0_2_candidate(
    candidate: ReviewDerivationManifest02Candidate,
    validation: ReviewDerivationManifest02Validation,
) -> AdmittedReviewDerivationManifest02:
    if (
        type(candidate) is not ReviewDerivationManifest02Candidate
        or type(validation) is not ReviewDerivationManifest02Validation
    ):
        _error(Manifest02FailureFamily.MANIFEST_0_2_ADMISSION_REJECTED)
    return candidate._admit(validation)


def consume_admitted_review_derivation_manifest_0_2(
    admitted: AdmittedReviewDerivationManifest02,
) -> dict[str, object]:
    if type(admitted) is not AdmittedReviewDerivationManifest02:
        _error(Manifest02FailureFamily.MANIFEST_0_2_ADMISSION_REJECTED)
    raw = admitted._manifest_copy()
    if dispatch_review_derivation_manifest_version(raw) is not (
        ManifestSchemaVersion.V0_2
    ):
        _error(Manifest02FailureFamily.MANIFEST_0_2_VERSION_OR_SHAPE_REJECTED)
    return json.loads(raw)


def stage_admitted_review_derivation_manifest_0_2(
    admitted: AdmittedReviewDerivationManifest02,
    staging: dict[str, bytes],
) -> PrivateManifest02StagingReceipt:
    if type(admitted) is not AdmittedReviewDerivationManifest02:
        _error(Manifest02FailureFamily.MANIFEST_0_2_ADMISSION_REJECTED)
    raw = admitted._claim_private_publication()
    if type(staging) is not dict or "manifest.json" in staging:
        _error(Manifest02FailureFamily.MANIFEST_0_2_PRIVATE_STAGING_REJECTED)
    staging["manifest.json"] = _owned(raw)
    return PrivateManifest02StagingReceipt(
        admission_digest=admitted.admission_digest,
        raw=raw,
        _token=_RECEIPT_TOKEN,
    )
