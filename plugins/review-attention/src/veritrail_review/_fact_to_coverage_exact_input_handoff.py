"""Private terminal-validated Fact input carrier for future Coverage work.

This module preserves the original Fact input world.  It grants no Coverage
obligation, disposition, status, ledger, manifest, or publication authority.
"""

from __future__ import annotations

import hashlib
import json
import threading
from typing import Mapping
from uuid import uuid4

from veritrail_review._fact_fulfillment import (
    OwnedProductFactClosure,
)
from veritrail_review._source_operation_gate import _input_state_seal
from veritrail_review.budget import BudgetContext, BudgetState
from veritrail_review.canonical import canonical_json_bytes, semantic_digest
from veritrail_review.derivation_input_contracts import DerivationInputSet


HANDOFF_FUNCTION = "r1-fact-to-coverage-exact-input-handoff-successor/0.2"
CLAIM_PURPOSE = "FACT_TO_COVERAGE_EXACT_INPUT_SUCCESSOR_0_2"
HANDOFF_CONSUMER = "r1-negative-world-coverage-exact-input-consumer/0.1"
CARRIER_IDENTITY = "r1-terminal-validated-original-derivation-input-carrier/0.1"

_CARRIER_TOKEN = object()
_NEGATIVE_WORLD_CONSUMER_TOKEN = object()
_CANONICAL_FIELDS = (
    "source_snapshot_canonical_bytes",
    "review_policy_canonical_bytes",
    "derivation_profile_canonical_bytes",
)


class _NegativeWorldConsumeState:
    """One copy-stable lock and consume bit for the private successor seam."""

    def __init__(self) -> None:
        self.lock = threading.Lock()
        self.consumed = False
_DIGEST_FIELDS = (
    "source_snapshot_digest",
    "policy_digest",
    "analysis_scope_digest",
    "slice_policy_digest",
    "derivation_profile_digest",
)


class FactToCoverageExactInputHandoffError(ValueError):
    """The private carrier lost original input or same-attempt authority."""


def _copy_blob_map(inputs: DerivationInputSet) -> dict[str, bytes]:
    blobs = inputs.verified_blob_bytes_by_object_identity
    if not isinstance(blobs, Mapping):
        raise FactToCoverageExactInputHandoffError("invalid verified blob map")
    try:
        owned = {
            key: memoryview(value).tobytes()
            for key, value in sorted(blobs.items())
            if type(key) is str and type(value) is bytes
        }
    except Exception as exc:
        raise FactToCoverageExactInputHandoffError(
            "invalid verified blob map"
        ) from exc
    if len(owned) != len(blobs):
        raise FactToCoverageExactInputHandoffError("invalid verified blob map")
    return owned


def _input_identity(
    inputs: DerivationInputSet, *, input_state_seal: str
) -> dict[str, object]:
    blobs = _copy_blob_map(inputs)
    return {
        "input_state_seal": input_state_seal,
        "canonical_sha256": {
            name: hashlib.sha256(getattr(inputs, name)).hexdigest()
            for name in _CANONICAL_FIELDS
        },
        "verified_blob_sha256_by_object_identity": {
            key: hashlib.sha256(value).hexdigest()
            for key, value in blobs.items()
        },
        **{name: getattr(inputs, name) for name in _DIGEST_FIELDS},
    }


class ClaimedFactToCoverageExactInputHandoff:
    """One-shot private view of terminal Fact source and its original inputs."""

    def __init__(
        self,
        source: Mapping[str, object],
        inputs: DerivationInputSet,
        context: BudgetContext,
        closure: OwnedProductFactClosure,
        claim_id: str,
        *,
        _token: object,
    ) -> None:
        if (
            _token is not _CARRIER_TOKEN
            or type(inputs) is not DerivationInputSet
            or type(context) is not BudgetContext
            or type(closure) is not OwnedProductFactClosure
            or type(claim_id) is not str
            or not claim_id
        ):
            raise FactToCoverageExactInputHandoffError(
                "exact-input carrier is not constructible"
            )
        self.__token = _token
        self.__closure = closure
        self.__bound_closure = closure
        self.__inputs = inputs
        self.__bound_inputs = inputs
        self.__context = context
        self.__bound_context = context
        self.__claim_id = claim_id
        self.__bound_claim_id = claim_id
        self.__source_bytes = canonical_json_bytes(dict(source))
        self.__bound_source_bytes = self.__source_bytes
        self.__input_state_seal = _input_state_seal(inputs)
        self.__canonical_bytes = tuple(
            getattr(inputs, name) for name in _CANONICAL_FIELDS
        )
        self.__blob_bytes = _copy_blob_map(inputs)
        self.__digests = tuple(getattr(inputs, name) for name in _DIGEST_FIELDS)
        self.__budget_identity = (
            context.limits,
            context.started_at_monotonic,
            context.execution_deadline_monotonic,
        )
        self.__document_bytes = canonical_json_bytes(self.__document())
        self.__bound_document_bytes = self.__document_bytes
        self.__failed = False
        self.__negative_world_consume_state = _NegativeWorldConsumeState()
        self.__validate()

    def __document(self) -> dict[str, object]:
        return {
            "handoff_function": HANDOFF_FUNCTION,
            "claim_purpose": CLAIM_PURPOSE,
            "consumer_identity": HANDOFF_CONSUMER,
            "carrier_identity": CARRIER_IDENTITY,
            "claim_id": self.__claim_id,
            "fact_terminal_source": json.loads(self.__source_bytes),
            "input_identity": _input_identity(
                self.__inputs, input_state_seal=self.__input_state_seal
            ),
            "same_object_graph_proof": {
                "terminal_source_revalidated": True,
                "original_derivation_input_set": True,
                "original_budget_context": True,
                "shared_one_shot_claim": True,
            },
        }

    def __fail(self, _exc: Exception) -> FactToCoverageExactInputHandoffError:
        self.__failed = True
        for closure in (self.__bound_closure, self.__closure):
            try:
                closure._revoke_handoff_source()
            except Exception:
                pass
        return FactToCoverageExactInputHandoffError(
            "exact-input carrier is no longer live"
        )

    def __validate(self) -> None:
        try:
            if (
                self.__failed
                or self.__token is not _CARRIER_TOKEN
                or self.__closure is not self.__bound_closure
                or self.__inputs is not self.__bound_inputs
                or self.__context is not self.__bound_context
                or self.__claim_id != self.__bound_claim_id
                or self.__source_bytes is not self.__bound_source_bytes
                or self.__document_bytes is not self.__bound_document_bytes
                or type(self.__source_bytes) is not bytes
                or type(self.__document_bytes) is not bytes
                or (
                    self.__context.limits,
                    self.__context.started_at_monotonic,
                    self.__context.execution_deadline_monotonic,
                )
                != self.__budget_identity
                or self.__context.state is not BudgetState.RUNNING
                or self.__context.stop_trigger is not None
                or not self.__context.checkpoint()
                or _input_state_seal(self.__inputs) != self.__input_state_seal
                or tuple(getattr(self.__inputs, name) for name in _CANONICAL_FIELDS)
                != self.__canonical_bytes
                or _copy_blob_map(self.__inputs) != self.__blob_bytes
                or tuple(getattr(self.__inputs, name) for name in _DIGEST_FIELDS)
                != self.__digests
            ):
                raise ValueError
            source, context, inputs = (
                self.__closure._validate_exact_input_successor_source()
            )
            if (
                context is not self.__context
                or inputs is not self.__inputs
                or canonical_json_bytes(source) != self.__source_bytes
                or canonical_json_bytes(self.__document()) != self.__document_bytes
            ):
                raise ValueError
        except Exception as exc:
            raise self.__fail(exc) from exc

    def fact_terminal_source_copy(self) -> dict[str, object]:
        self.__validate()
        return json.loads(self.__source_bytes)

    def source_snapshot_document_copy(self) -> dict[str, object]:
        self.__validate()
        return self.__inputs.source_snapshot_document_copy()

    def review_policy_document_copy(self) -> dict[str, object]:
        self.__validate()
        return self.__inputs.review_policy_document_copy()

    def derivation_profile_document_copy(self) -> dict[str, object]:
        self.__validate()
        return self.__inputs.derivation_profile_document_copy()

    def verified_blob_bytes_copy(self) -> dict[str, bytes]:
        self.__validate()
        return {
            key: memoryview(value).tobytes()
            for key, value in self.__blob_bytes.items()
        }

    def input_identity_copy(self) -> dict[str, object]:
        self.__validate()
        document = json.loads(self.__document_bytes)
        return {
            key: document[key]
            for key in (
                "handoff_function",
                "claim_purpose",
                "consumer_identity",
                "carrier_identity",
                "claim_id",
                "input_identity",
                "same_object_graph_proof",
            )
        }

    def _consume_negative_world_authority(self, *, _token: object):
        """Bind one private negative-world attempt to this exact carrier.

        The hook deliberately returns the original object graph only to the
        sibling private implementation that owns the opaque token.  It does
        not add a public method, alter the carrier identity, or construct any
        Coverage history.
        """

        if _token is not _NEGATIVE_WORLD_CONSUMER_TOKEN:
            raise FactToCoverageExactInputHandoffError(
                "negative-world carrier consumer is not supported"
            )
        state = self.__negative_world_consume_state
        with state.lock:
            self.__validate()
            if state.consumed:
                raise FactToCoverageExactInputHandoffError(
                    "negative-world carrier was already consumed"
                )
            source = json.loads(self.__source_bytes)
            if source.get("branch") not in {
                "ZERO_PARSE_DENOMINATOR",
                "ALL_PARSE_REJECTED",
                "PROJECTION_BLOCKED",
                "REQUIRED_PROVIDER_NON_SUCCESS",
            }:
                raise FactToCoverageExactInputHandoffError(
                    "terminal branch is not a negative-world branch"
                )
            state.consumed = True
            return (
                source,
                self.__inputs,
                self.__context,
                self.__closure,
                self.__claim_id,
            )


def claim_fact_to_coverage_exact_input_handoff(
    closure: OwnedProductFactClosure,
    *,
    handoff_function: str = HANDOFF_FUNCTION,
    claim_purpose: str = CLAIM_PURPOSE,
    consumer_identity: str = HANDOFF_CONSUMER,
    carrier_identity: str = CARRIER_IDENTITY,
) -> ClaimedFactToCoverageExactInputHandoff:
    """Consume one terminal Fact closure under the exact 0.2 identities."""

    if (
        type(closure) is not OwnedProductFactClosure
        or any(
            type(value) is not str
            for value in (
                handoff_function,
                claim_purpose,
                consumer_identity,
                carrier_identity,
            )
        )
        or handoff_function != HANDOFF_FUNCTION
        or claim_purpose != CLAIM_PURPOSE
        or consumer_identity != HANDOFF_CONSUMER
        or carrier_identity != CARRIER_IDENTITY
    ):
        raise FactToCoverageExactInputHandoffError(
            "exact-input handoff identity is not supported"
        )
    source_acquired = False
    try:
        source, context, inputs = closure._claim_exact_input_successor_source()
        source_acquired = True
        claim_id = semantic_digest(
            "veritrail.review.private-fact-coverage-exact-input-claim/0.2",
            {"nonce": uuid4().hex},
        )
        return ClaimedFactToCoverageExactInputHandoff(
            source,
            inputs,
            context,
            closure,
            claim_id,
            _token=_CARRIER_TOKEN,
        )
    except Exception as exc:
        if source_acquired:
            try:
                closure._revoke_handoff_source()
            except Exception:
                pass
        raise FactToCoverageExactInputHandoffError(
            "exact-input handoff claim failed closed"
        ) from exc
