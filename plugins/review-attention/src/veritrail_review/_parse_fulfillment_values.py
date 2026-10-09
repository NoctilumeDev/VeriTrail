from __future__ import annotations

import base64
import hashlib
import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from types import MappingProxyType
from typing import Mapping

from veritrail_review.canonical import canonical_json_bytes, semantic_digest


PARSE_FUNCTION_ID = "r1-python-parse/0.1"
PARSE_WORKER_PROTOCOL = "veritrail-r1-parse-worker/0.1"
_RUNTIME_TOKEN = object()
_OBSERVATION_TOKEN = object()
_PRODUCT_SET_TOKEN = object()
_HEX_64 = re.compile(r"^[0-9a-f]{64}$")


@dataclass(frozen=True)
class OwnedParseRuntimeCapability:
    """Private exact executable capability; never a public runtime identity."""

    executable: Path
    executable_sha256: str
    capability_digest: str
    _state_seal: str = field(repr=False, compare=False)
    _construction_token: object = field(repr=False, compare=False)

    @classmethod
    def _create(
        cls, *, executable: Path, executable_sha256: str
    ) -> "OwnedParseRuntimeCapability":
        path = Path(executable)
        payload = {
            "parse_function": PARSE_FUNCTION_ID,
            "reference_implementation": "CPYTHON",
            "reference_version": "3.10.6",
            "executable_path": str(path),
            "executable_sha256": executable_sha256,
        }
        digest = semantic_digest(
            "veritrail.review.private-parse-runtime-capability/0.1", payload
        )
        values = {
            "executable": path,
            "executable_sha256": executable_sha256,
            "capability_digest": digest,
        }
        value = cls(
            **values,
            _state_seal=_state_seal(values),
            _construction_token=_RUNTIME_TOKEN,
        )
        _validate_runtime_capability(value, check_executable=False)
        return value


@dataclass(frozen=True)
class OwnedParseObservation:
    """One attempt-bound candidate observation; never reconciliation authority."""

    subject_identity: str
    obligation_id: str
    parse_function: str
    lifecycle: str
    semantic_result_bytes: bytes | None = field(repr=False)
    product_semantic_digest: str | None
    _attempt: object = field(repr=False, compare=False)
    _claim: object = field(repr=False, compare=False)
    _state_seal: str = field(repr=False, compare=False)
    _construction_token: object = field(repr=False, compare=False)

    @classmethod
    def _create(
        cls,
        *,
        subject_identity: str,
        obligation_id: str,
        lifecycle: str,
        semantic_result: Mapping[str, object] | None,
        attempt: object,
        claim: object,
    ) -> "OwnedParseObservation":
        result_bytes = (
            None
            if semantic_result is None
            else canonical_json_bytes(dict(semantic_result))
        )
        product_digest: str | None = None
        if semantic_result is not None and semantic_result.get("disposition") == "ACCEPTED":
            product_digest = semantic_digest(
                "veritrail.review.private-parse-product/0.1",
                {
                    "subject_identity": subject_identity,
                    "obligation_id": obligation_id,
                    "parse_function": PARSE_FUNCTION_ID,
                    "product": semantic_result.get("product"),
                },
            )
        values = {
            "subject_identity": subject_identity,
            "obligation_id": obligation_id,
            "parse_function": PARSE_FUNCTION_ID,
            "lifecycle": lifecycle,
            "semantic_result_bytes": result_bytes,
            "product_semantic_digest": product_digest,
        }
        value = cls(
            **values,
            _attempt=attempt,
            _claim=claim,
            _state_seal=_state_seal(values),
            _construction_token=_OBSERVATION_TOKEN,
        )
        _validate_parse_observation(value)
        return value

    def semantic_result_copy(self) -> dict[str, object] | None:
        _validate_parse_observation(self)
        if self.semantic_result_bytes is None:
            return None
        return _object(self.semantic_result_bytes)


@dataclass(frozen=True)
class OwnedParseProductSet:
    """Attempt-neutral private semantic product set with copy-owned products."""

    source_snapshot_digest: str
    policy_digest: str
    analysis_scope_digest: str
    derivation_profile_digest: str
    language_support_function: str
    classification_digest: str
    parse_function: str
    product_set_digest: str
    denominator_count: int
    accepted_count: int
    rejected_count: int
    product_set_document_bytes: bytes = field(repr=False)
    _product_bytes_by_subject: Mapping[str, bytes] = field(repr=False, compare=False)
    _state_seal: str = field(repr=False, compare=False)
    _construction_token: object = field(repr=False, compare=False)

    @classmethod
    def _create(
        cls,
        *,
        source_snapshot_digest: str,
        policy_digest: str,
        analysis_scope_digest: str,
        derivation_profile_digest: str,
        language_support_function: str,
        classification_digest: str,
        product_set_document: Mapping[str, object],
        product_bytes_by_subject: Mapping[str, bytes],
    ) -> "OwnedParseProductSet":
        document = dict(product_set_document)
        document_bytes = canonical_json_bytes(document)
        denominator = document.get("denominator")
        accepted = document.get("accepted")
        rejected = document.get("rejected")
        if (
            not isinstance(denominator, list)
            or not isinstance(accepted, list)
            or not isinstance(rejected, list)
        ):
            raise ValueError("invalid private Parse product set")
        owned_products = MappingProxyType(
            {
                str(key): memoryview(value).tobytes()
                for key, value in product_bytes_by_subject.items()
            }
        )
        values = {
            "source_snapshot_digest": source_snapshot_digest,
            "policy_digest": policy_digest,
            "analysis_scope_digest": analysis_scope_digest,
            "derivation_profile_digest": derivation_profile_digest,
            "language_support_function": language_support_function,
            "classification_digest": classification_digest,
            "parse_function": PARSE_FUNCTION_ID,
            "product_set_digest": document["product_set_digest"],
            "denominator_count": len(denominator),
            "accepted_count": len(accepted),
            "rejected_count": len(rejected),
            "product_set_document_bytes": document_bytes,
            "_product_bytes_by_subject": owned_products,
        }
        value = cls(
            **values,
            _state_seal=_state_seal(values),
            _construction_token=_PRODUCT_SET_TOKEN,
        )
        _validate_parse_product_set(value)
        return value

    def product_set_document_copy(self) -> dict[str, object]:
        _validate_parse_product_set(self)
        return _object(self.product_set_document_bytes)

    def products_copy(self) -> dict[str, object]:
        _validate_parse_product_set(self)
        return {
            subject: json.loads(raw)
            for subject, raw in self._product_bytes_by_subject.items()
        }


def _validate_runtime_capability(
    value: OwnedParseRuntimeCapability, *, check_executable: bool
) -> None:
    if (
        type(value) is not OwnedParseRuntimeCapability
        or value._construction_token is not _RUNTIME_TOKEN
        or not isinstance(value.executable, Path)
        or not value.executable.is_absolute()
        or not _digest(value.executable_sha256)
        or not _digest(value.capability_digest)
    ):
        raise ValueError("invalid private Parse runtime capability")
    payload = {
        "parse_function": PARSE_FUNCTION_ID,
        "reference_implementation": "CPYTHON",
        "reference_version": "3.10.6",
        "executable_path": str(value.executable),
        "executable_sha256": value.executable_sha256,
    }
    values = {
        "executable": value.executable,
        "executable_sha256": value.executable_sha256,
        "capability_digest": value.capability_digest,
    }
    if (
        value.capability_digest
        != semantic_digest(
            "veritrail.review.private-parse-runtime-capability/0.1", payload
        )
        or value._state_seal != _state_seal(values)
    ):
        raise ValueError("private Parse runtime capability changed")
    if check_executable:
        try:
            if not value.executable.is_file():
                raise ValueError
            digest = hashlib.sha256(value.executable.read_bytes()).hexdigest()
        except OSError as exc:
            raise ValueError("private Parse runtime is unavailable") from exc
        if digest != value.executable_sha256:
            raise ValueError("private Parse runtime bytes changed")


def _validate_parse_observation(value: OwnedParseObservation) -> None:
    if (
        type(value) is not OwnedParseObservation
        or value._construction_token is not _OBSERVATION_TOKEN
        or not _digest(value.subject_identity)
        or not _digest(value.obligation_id)
        or value.parse_function != PARSE_FUNCTION_ID
        or value.lifecycle
        not in {
            "COMPLETED",
            "INTERRUPTED",
            "REFERENCE_RUNTIME_UNAVAILABLE",
            "INFRASTRUCTURE_FAILED",
            "INTERNAL_PARSER_FAILURE",
            "RELEASE_FAILED",
        }
    ):
        raise ValueError("invalid private Parse observation")
    values = {
        "subject_identity": value.subject_identity,
        "obligation_id": value.obligation_id,
        "parse_function": value.parse_function,
        "lifecycle": value.lifecycle,
        "semantic_result_bytes": value.semantic_result_bytes,
        "product_semantic_digest": value.product_semantic_digest,
    }
    if value._state_seal != _state_seal(values):
        raise ValueError("private Parse observation changed")
    if value.lifecycle != "COMPLETED":
        if value.semantic_result_bytes is not None or value.product_semantic_digest is not None:
            raise ValueError("non-success Parse lifecycle carried semantic truth")
        return
    if type(value.semantic_result_bytes) is not bytes:
        raise ValueError("completed Parse observation has no semantic result")
    result = _object(value.semantic_result_bytes)
    _validate_semantic_result(result)
    product = result["product"]
    expected = (
        semantic_digest(
            "veritrail.review.private-parse-product/0.1",
            {
                "subject_identity": value.subject_identity,
                "obligation_id": value.obligation_id,
                "parse_function": value.parse_function,
                "product": product,
            },
        )
        if result["disposition"] == "ACCEPTED"
        else None
    )
    if value.product_semantic_digest != expected:
        raise ValueError("Parse product identity changed")


def _validate_semantic_result(result: Mapping[str, object]) -> None:
    if set(result) != {"disposition", "reason_codes", "product"}:
        raise ValueError("invalid Parse semantic result")
    disposition = result["disposition"]
    if disposition == "ACCEPTED":
        if result["reason_codes"] != []:
            raise ValueError("accepted Parse result carried reasons")
        _validate_tree_value(result["product"])
    elif disposition == "REJECTED":
        if result["reason_codes"] != ["PARSE_ERROR"] or result["product"] is not None:
            raise ValueError("invalid rejected Parse result")
    else:
        raise ValueError("invalid Parse disposition")


def _validate_tree_value(value: object) -> None:
    if not isinstance(value, dict) or not isinstance(value.get("value_kind"), str):
        raise ValueError("invalid private Parse tree value")
    kind = value["value_kind"]
    if kind == "AST":
        if set(value) != {"value_kind", "node_type", "fields", "attributes"}:
            raise ValueError
        if not isinstance(value["node_type"], str) or not value["node_type"]:
            raise ValueError
        for group_name in ("fields", "attributes"):
            group = value[group_name]
            if not isinstance(group, dict) or any(
                not isinstance(name, str) or not name for name in group
            ):
                raise ValueError
            for child in group.values():
                _validate_tree_value(child)
    elif kind == "LIST":
        if set(value) != {"value_kind", "items"} or not isinstance(value["items"], list):
            raise ValueError
        for child in value["items"]:
            _validate_tree_value(child)
    elif kind == "SCALAR":
        if set(value) != {"value_kind", "value"}:
            raise ValueError
        _validate_scalar(value["value"])
    else:
        raise ValueError("unknown private Parse tree kind")


def _validate_scalar(value: object) -> None:
    if value is None or isinstance(value, (bool, int, str)):
        return
    if not isinstance(value, dict) or not isinstance(value.get("scalar_kind"), str):
        raise ValueError("invalid private Parse scalar")
    kind = value["scalar_kind"]
    try:
        if kind == "FLOAT" and set(value) == {"scalar_kind", "hex"}:
            if float.fromhex(value["hex"]).hex() != value["hex"]:  # type: ignore[arg-type]
                raise ValueError
        elif kind == "COMPLEX" and set(value) == {"scalar_kind", "real_hex", "imag_hex"}:
            for key in ("real_hex", "imag_hex"):
                if float.fromhex(value[key]).hex() != value[key]:  # type: ignore[arg-type]
                    raise ValueError
        elif kind == "BYTES" and set(value) == {"scalar_kind", "base64"}:
            raw = base64.b64decode(value["base64"], validate=True)  # type: ignore[arg-type]
            if base64.b64encode(raw).decode("ascii") != value["base64"]:
                raise ValueError
        elif kind == "ELLIPSIS" and set(value) == {"scalar_kind"}:
            return
        else:
            raise ValueError
    except (TypeError, ValueError) as exc:
        raise ValueError("invalid private Parse scalar") from exc


def _validate_parse_product_set(value: OwnedParseProductSet) -> None:
    if (
        type(value) is not OwnedParseProductSet
        or value._construction_token is not _PRODUCT_SET_TOKEN
        or value.parse_function != PARSE_FUNCTION_ID
        or not _digest(value.product_set_digest)
        or any(
            not _digest(item)
            for item in (
                value.source_snapshot_digest,
                value.policy_digest,
                value.analysis_scope_digest,
                value.derivation_profile_digest,
                value.classification_digest,
            )
        )
        or not isinstance(value._product_bytes_by_subject, Mapping)
    ):
        raise ValueError("invalid private Parse product set")
    document = _object(value.product_set_document_bytes)
    if set(document) != {
        "source_snapshot_digest",
        "policy_digest",
        "analysis_scope_digest",
        "derivation_profile_digest",
        "language_support_function",
        "classification_digest",
        "parse_function",
        "denominator",
        "accepted",
        "rejected",
        "product_set_digest",
    }:
        raise ValueError
    denominator = document["denominator"]
    accepted = document["accepted"]
    rejected = document["rejected"]
    if (
        not _digest_list(denominator)
        or not isinstance(accepted, list)
        or not isinstance(rejected, list)
        or len(denominator) != len(set(denominator))
    ):
        raise ValueError
    accepted_ids: list[str] = []
    for entry in accepted:
        if (
            not isinstance(entry, dict)
            or set(entry)
            != {
                "subject_identity",
                "obligation_id",
                "product_semantic_digest",
            }
            or not _digest(entry["subject_identity"])
            or not _digest(entry["obligation_id"])
            or not _digest(entry["product_semantic_digest"])
        ):
            raise ValueError
        accepted_ids.append(entry["subject_identity"])
    rejected_ids: list[str] = []
    for entry in rejected:
        if (
            not isinstance(entry, dict)
            or set(entry) != {"subject_identity", "obligation_id"}
            or not _digest(entry["subject_identity"])
            or not _digest(entry["obligation_id"])
        ):
            raise ValueError
        rejected_ids.append(entry["subject_identity"])
    if (
        len(accepted_ids) != len(set(accepted_ids))
        or len(rejected_ids) != len(set(rejected_ids))
        or set(accepted_ids).intersection(rejected_ids)
        or set(accepted_ids).union(rejected_ids) != set(denominator)
        or [item for item in denominator if item in set(accepted_ids)] != accepted_ids
        or [item for item in denominator if item in set(rejected_ids)] != rejected_ids
        or set(value._product_bytes_by_subject) != set(accepted_ids)
    ):
        raise ValueError
    for entry in accepted:
        subject = entry["subject_identity"]
        product = json.loads(value._product_bytes_by_subject[subject])
        _validate_tree_value(product)
        if entry["product_semantic_digest"] != semantic_digest(
            "veritrail.review.private-parse-product/0.1",
            {
                "subject_identity": subject,
                "obligation_id": entry["obligation_id"],
                "parse_function": PARSE_FUNCTION_ID,
                "product": product,
            },
        ):
            raise ValueError
    unsigned = {key: item for key, item in document.items() if key != "product_set_digest"}
    if document["product_set_digest"] != semantic_digest(
        "veritrail.review.private-parse-product-set/0.1", unsigned
    ):
        raise ValueError
    values = {
        "source_snapshot_digest": value.source_snapshot_digest,
        "policy_digest": value.policy_digest,
        "analysis_scope_digest": value.analysis_scope_digest,
        "derivation_profile_digest": value.derivation_profile_digest,
        "language_support_function": value.language_support_function,
        "classification_digest": value.classification_digest,
        "parse_function": value.parse_function,
        "product_set_digest": value.product_set_digest,
        "denominator_count": value.denominator_count,
        "accepted_count": value.accepted_count,
        "rejected_count": value.rejected_count,
        "product_set_document_bytes": value.product_set_document_bytes,
        "_product_bytes_by_subject": value._product_bytes_by_subject,
    }
    if (
        canonical_json_bytes(document) != value.product_set_document_bytes
        or value._state_seal != _state_seal(values)
        or (
            value.source_snapshot_digest,
            value.policy_digest,
            value.analysis_scope_digest,
            value.derivation_profile_digest,
            value.language_support_function,
            value.classification_digest,
            value.product_set_digest,
            value.denominator_count,
            value.accepted_count,
            value.rejected_count,
        )
        != (
            document["source_snapshot_digest"],
            document["policy_digest"],
            document["analysis_scope_digest"],
            document["derivation_profile_digest"],
            document["language_support_function"],
            document["classification_digest"],
            document["product_set_digest"],
            len(denominator),
            len(accepted),
            len(rejected),
        )
    ):
        raise ValueError("private Parse product set changed")


def _state_seal(values: Mapping[str, object]) -> str:
    payload: dict[str, object] = {}
    for key, value in values.items():
        if isinstance(value, Path):
            payload[key] = str(value)
        elif isinstance(value, bytes):
            payload[f"{key}_sha256"] = hashlib.sha256(value).hexdigest()
        elif isinstance(value, Mapping):
            payload[f"{key}_sha256_by_key"] = {
                str(item_key): hashlib.sha256(item_value).hexdigest()
                for item_key, item_value in sorted(value.items())
                if isinstance(item_value, bytes)
            }
            if len(payload[f"{key}_sha256_by_key"]) != len(value):  # type: ignore[arg-type]
                raise ValueError
        else:
            payload[key] = value
    return semantic_digest("veritrail.review.private-parse-owned-state/0.1", payload)


def _object(raw: bytes) -> dict[str, object]:
    value = json.loads(raw)
    if not isinstance(value, dict) or canonical_json_bytes(value) != raw:
        raise ValueError("private Parse bytes are not one canonical object")
    return value


def _digest(value: object) -> bool:
    return isinstance(value, str) and _HEX_64.fullmatch(value) is not None


def _digest_list(value: object) -> bool:
    return isinstance(value, list) and all(_digest(item) for item in value)
