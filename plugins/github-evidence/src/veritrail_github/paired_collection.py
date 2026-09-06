from __future__ import annotations

import re
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

from veritrail.evidence import ImportedEvidence

from veritrail_github.conformance import verify_github_evidence
from veritrail_github.contracts import validate_observation_request
from veritrail_github.errors import ContractError
from veritrail_github.public_render_conformance import (
    verify_public_render_evidence,
)
from veritrail_github.public_render_contracts import (
    validate_public_render_request,
)
from veritrail_github.publisher import publish_evidence


_SESSION_ID_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:/-]{0,127}$")
_COLLECTION_ORDER = ("github-api", "github-public-render")


@dataclass(frozen=True)
class PairedSideOutcome:
    """Safe execution provenance for one independent Evidence side."""

    collector_role: str
    requested_output_path: Path
    artifact_path: Path | None
    artifact_sha256: str | None
    coverage: str | None
    state: str
    error_code: str | None


@dataclass(frozen=True)
class PairedCollectionResult:
    """Correlation result; deliberately contains no joined facts or Verdict."""

    collection_session_id: str
    collection_order: tuple[str, str]
    api: PairedSideOutcome
    render: PairedSideOutcome


class PairedCollectionCoordinator:
    """Run independent P1 and P2 collectors in one bounded correlation window."""

    def __init__(
        self,
        *,
        api_collector_factory: Callable[[Callable[[], str]], Any],
        render_collector_factory: Callable[[Callable[[], str]], Any],
        session_id_factory: Callable[[], str] | None = None,
    ) -> None:
        if not callable(api_collector_factory) or not callable(
            render_collector_factory
        ):
            raise TypeError("paired collector factories must be callable")
        if session_id_factory is not None and not callable(session_id_factory):
            raise TypeError("paired collection session factory must be callable")
        self._api_collector_factory = api_collector_factory
        self._render_collector_factory = render_collector_factory
        self._session_id_factory = session_id_factory or (
            lambda: f"github-paired-{uuid.uuid4().hex}"
        )

    def collect_and_publish(
        self,
        plan: dict[str, Any],
        api_request: dict[str, Any],
        render_request: dict[str, Any],
        *,
        api_output_path: Path,
        render_output_path: Path,
    ) -> PairedCollectionResult:
        """Validate offline, then collect and publish P1 followed by P2."""

        verified_api, verified_render = _validate_request_pair(
            plan, api_request, render_request
        )
        _validate_output_pair(api_output_path, render_output_path)

        try:
            session_id = self._session_id_factory()
        except Exception:
            raise ContractError(["paired collection session creation failed"]) from None
        if not isinstance(session_id, str) or not _SESSION_ID_PATTERN.fullmatch(
            session_id
        ):
            raise ContractError(
                ["paired collection session factory returned an invalid reference"]
            )
        shared_session_factory = lambda: session_id

        api_outcome = self._run_side(
            role="github-api",
            plan=plan,
            request=verified_api,
            output_path=api_output_path,
            collector_factory=self._api_collector_factory,
            session_factory=shared_session_factory,
            verifier=verify_github_evidence,
        )
        render_outcome = self._run_side(
            role="github-public-render",
            plan=plan,
            request=verified_render,
            output_path=render_output_path,
            collector_factory=self._render_collector_factory,
            session_factory=shared_session_factory,
            verifier=verify_public_render_evidence,
        )
        return PairedCollectionResult(
            collection_session_id=session_id,
            collection_order=_COLLECTION_ORDER,
            api=api_outcome,
            render=render_outcome,
        )

    @staticmethod
    def _run_side(
        *,
        role: str,
        plan: dict[str, Any],
        request: dict[str, Any],
        output_path: Path,
        collector_factory: Callable[[Callable[[], str]], Any],
        session_factory: Callable[[], str],
        verifier: Callable[[dict[str, Any], dict[str, Any], ImportedEvidence], None],
    ) -> PairedSideOutcome:
        try:
            collector = collector_factory(session_factory)
        except Exception:
            return _missing_outcome(role, output_path, "COLLECTOR_FACTORY_ERROR")

        try:
            result = collector.collect(plan, request)
        except Exception:
            return _missing_outcome(role, output_path, "COLLECTION_ERROR")

        artifact = getattr(result, "artifact", None)
        try:
            verifier(plan, request, artifact)
            observation = artifact.document["metadata"]["veritrail_observation"]
            coverage = observation["coverage"]
        except Exception:
            return _missing_outcome(role, output_path, "ARTIFACT_CONFORMANCE_ERROR")

        if observation.get("collection_session_id") != session_factory():
            return _missing_outcome(role, output_path, "SESSION_MISMATCH")

        try:
            publish_evidence(output_path, artifact)
        except Exception:
            return PairedSideOutcome(
                collector_role=role,
                requested_output_path=output_path,
                artifact_path=None,
                artifact_sha256=artifact.sha256,
                coverage=coverage,
                state="COLLECTED_NOT_PUBLISHED",
                error_code="PUBLISH_ERROR",
            )
        return PairedSideOutcome(
            collector_role=role,
            requested_output_path=output_path,
            artifact_path=output_path,
            artifact_sha256=artifact.sha256,
            coverage=coverage,
            state="PUBLISHED",
            error_code=None,
        )


def _validate_request_pair(
    plan: dict[str, Any],
    api_request: dict[str, Any],
    render_request: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    errors: list[str] = []
    verified_api: dict[str, Any] | None = None
    verified_render: dict[str, Any] | None = None
    try:
        verified_api = validate_observation_request(plan, api_request)
    except ContractError as exc:
        errors.extend(f"github-api: {item}" for item in exc.errors)
    try:
        verified_render = validate_public_render_request(plan, render_request)
    except ContractError as exc:
        errors.extend(f"github-public-render: {item}" for item in exc.errors)
    if errors:
        raise ContractError(errors)
    if verified_api is None or verified_render is None:
        raise ContractError(["paired request validation did not produce both requests"])
    return verified_api, verified_render


def _validate_output_pair(api_path: Path, render_path: Path) -> None:
    errors: list[str] = []
    for role, path in (("github-api", api_path), ("github-public-render", render_path)):
        if not isinstance(path, Path):
            errors.append(f"{role} output path must be a pathlib.Path")
        elif not path.name:
            errors.append(f"{role} output path must name an Evidence file")
        elif path.exists():
            errors.append(f"{role} output path already exists")
    if isinstance(api_path, Path) and isinstance(render_path, Path):
        if api_path.resolve(strict=False) == render_path.resolve(strict=False):
            errors.append("P1 and P2 output paths must be distinct")
    if errors:
        raise ContractError(errors)


def _missing_outcome(
    role: str, output_path: Path, error_code: str
) -> PairedSideOutcome:
    return PairedSideOutcome(
        collector_role=role,
        requested_output_path=output_path,
        artifact_path=None,
        artifact_sha256=None,
        coverage=None,
        state="MISSING",
        error_code=error_code,
    )
