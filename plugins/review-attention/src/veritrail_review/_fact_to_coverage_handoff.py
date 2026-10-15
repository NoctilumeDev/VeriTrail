"""Private, same-attempt Fact-stage history handoff.

This module stops before Coverage vocabulary, status, join, or publication.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from uuid import uuid4

from veritrail_review._fact_fulfillment import (
    OwnedProductFactClosure,
    ProductFactConsumerError,
)
from veritrail_review.budget import BudgetContext, BudgetState
from veritrail_review.canonical import canonical_json_bytes, semantic_digest


HANDOFF_FUNCTION = "r1-fact-to-coverage-handoff/0.1"
HANDOFF_CONSUMER = "veritrail-review-private-coverage-composition/0.1"
_HANDOFF_TOKEN = object()


class FactToCoverageHandoffError(ValueError):
    """The private handoff lost its original source or consumer authority."""


@dataclass(frozen=True)
class ClaimedFactToCoverageHandoff:
    """Copy-owned Fact-stage input for the one fixed downstream consumer."""

    _bytes: bytes = field(repr=False)
    _context: BudgetContext = field(repr=False, compare=False)
    _bound_context: BudgetContext = field(repr=False, compare=False)
    _token: object = field(repr=False, compare=False)
    _bound_bytes: bytes = field(init=False, repr=False, compare=False)

    def __post_init__(self) -> None:
        if self._token is not _HANDOFF_TOKEN:
            raise FactToCoverageHandoffError("handoff is not constructible")
        object.__setattr__(self, "_bound_bytes", self._bytes)
        self._validate()

    def _validate(self) -> None:
        if (
            self._token is not _HANDOFF_TOKEN
            or self._bytes is not self._bound_bytes
            or self._context is not self._bound_context
            or type(self._bytes) is not bytes
            or self._context.state is not BudgetState.RUNNING
            or self._context.stop_trigger is not None
            or not self._context.checkpoint()
        ):
            raise FactToCoverageHandoffError("handoff is no longer live")
        document = json.loads(self._bytes)
        if (
            canonical_json_bytes(document) != self._bytes
            or document.get("handoff_function") != HANDOFF_FUNCTION
            or document.get("consumer_identity") != HANDOFF_CONSUMER
            or set(document)
            != {
                "claim_id",
                "consumer_identity",
                "handoff_function",
                "source",
            }
        ):
            raise FactToCoverageHandoffError("handoff bytes changed")

    def document_copy(self) -> dict[str, object]:
        self._validate()
        return json.loads(self._bytes)

    def _context_ref(self) -> BudgetContext:
        self._validate()
        return self._context


def claim_fact_to_coverage_handoff(
    closure: OwnedProductFactClosure,
) -> ClaimedFactToCoverageHandoff:
    """Consume one owned Fact closure for the fixed private consumer."""

    if type(closure) is not OwnedProductFactClosure:
        raise FactToCoverageHandoffError("handoff requires an owned Fact closure")
    source_acquired = False
    try:
        source, context = closure._claim_handoff_source()
        source_acquired = True
        claim_id = semantic_digest(
            "veritrail.review.private-fact-coverage-handoff-claim/0.1",
            {"nonce": uuid4().hex},
        )
        value = {
            "handoff_function": HANDOFF_FUNCTION,
            "consumer_identity": HANDOFF_CONSUMER,
            "claim_id": claim_id,
            "source": source,
        }
        return ClaimedFactToCoverageHandoff(
            canonical_json_bytes(value), context, context, _HANDOFF_TOKEN
        )
    except Exception as exc:
        if source_acquired:
            try:
                closure._revoke_handoff_source()
            except Exception:
                pass
        raise FactToCoverageHandoffError("handoff claim failed closed") from exc
