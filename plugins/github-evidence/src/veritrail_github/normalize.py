from __future__ import annotations

from collections import Counter
import re
from typing import Any

from veritrail_github.errors import ContractError


def _object(value: Any, path: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ContractError([f"{path} must be an object"])
    return value


def _array(value: Any, path: str) -> list[Any]:
    if not isinstance(value, list):
        raise ContractError([f"{path} must be an array"])
    return value


def _string(value: Any, path: str, *, nullable: bool = False) -> str | None:
    if nullable and value is None:
        return None
    if not isinstance(value, str):
        raise ContractError([f"{path} must be a string"])
    return value


def _integer(value: Any, path: str, *, nullable: bool = False) -> int | None:
    if nullable and value is None:
        return None
    if not isinstance(value, int) or isinstance(value, bool):
        raise ContractError([f"{path} must be an integer"])
    return value


def _boolean(value: Any, path: str, *, nullable: bool = False) -> bool | None:
    if nullable and value is None:
        return None
    if not isinstance(value, bool):
        raise ContractError([f"{path} must be a boolean"])
    return value


def _sha(value: Any, path: str, *, nullable: bool = False) -> str | None:
    normalized = _string(value, path, nullable=nullable)
    if normalized is None:
        return None
    if not re.fullmatch(r"[0-9a-f]{40}", normalized):
        raise ContractError([f"{path} must be a 40-character lowercase SHA"])
    return normalized


def normalize_repository(
    payload: Any,
    *,
    owner: str,
    repository: str,
    projections: set[str],
    conflicts: list[dict[str, Any]],
) -> tuple[dict[str, Any] | None, str, str]:
    value = _object(payload, "repository response")
    owner_value = _object(value.get("owner"), "repository.owner")
    observed_owner = _string(owner_value.get("login"), "repository.owner.login")
    observed_name = _string(value.get("name"), "repository.name")
    full_name = _string(value.get("full_name"), "repository.full_name")
    repository_id = _integer(value.get("id"), "repository.id")
    private = _boolean(value.get("private"), "repository.private")
    default_branch = _string(value.get("default_branch"), "repository.default_branch")
    visibility_value = value.get("visibility")
    visibility = (
        _string(visibility_value, "repository.visibility")
        if visibility_value is not None
        else ("private" if private else "public")
    )
    if (
        observed_owner.casefold() != owner.casefold()
        or observed_name.casefold() != repository.casefold()
    ):
        conflicts.append(
            {
                "code": "REPOSITORY_IDENTITY_MISMATCH",
                "expected_owner": owner,
                "expected_repository": repository,
                "observed_full_name": full_name,
            }
        )
    normalized: dict[str, Any] = {}
    if "repository.identity" in projections:
        normalized.update(
            {
                "id": repository_id,
                "owner": observed_owner,
                "name": observed_name,
                "full_name": full_name,
                "private": private,
                "visibility": visibility,
            }
        )
    if "repository.default_branch" in projections:
        normalized["default_branch"] = default_branch
    public_visibility = "PRIVATE_OR_RESTRICTED" if private else "PUBLIC"
    return (normalized or None), default_branch, public_visibility


def normalize_commit(
    payload: Any,
    *,
    target_commit_sha: str,
    projected: bool,
    conflicts: list[dict[str, Any]],
) -> dict[str, Any] | None:
    value = _object(payload, "commit response")
    observed_sha = _sha(value.get("sha"), "commit.sha")
    if observed_sha != target_commit_sha:
        conflicts.append(
            {
                "code": "COMMIT_IDENTITY_MISMATCH",
                "expected_sha": target_commit_sha,
                "observed_sha": observed_sha,
            }
        )
    if not projected:
        return None
    return {
        "sha": observed_sha,
        "node_id": _string(value.get("node_id"), "commit.node_id", nullable=True),
    }


def normalize_pull_request(payload: Any) -> dict[str, Any]:
    value = _object(payload, "pull request response")
    head = _object(value.get("head"), "pull_request.head")
    base = _object(value.get("base"), "pull_request.base")
    return {
        "number": _integer(value.get("number"), "pull_request.number"),
        "state": _string(value.get("state"), "pull_request.state"),
        "merged": _boolean(value.get("merged"), "pull_request.merged"),
        "head_sha": _sha(head.get("sha"), "pull_request.head.sha"),
        "base_sha": _sha(base.get("sha"), "pull_request.base.sha"),
        "merge_commit_sha": _sha(
            value.get("merge_commit_sha"),
            "pull_request.merge_commit_sha",
            nullable=True,
        ),
    }


def normalize_active_rules(payload: Any) -> list[dict[str, Any]]:
    rules = _array(payload, "active rules response")
    normalized: list[dict[str, Any]] = []
    for index, item in enumerate(rules):
        rule = _object(item, f"active_rules[{index}]")
        if rule.get("type") != "required_status_checks":
            continue
        parameters = _object(
            rule.get("parameters"), f"active_rules[{index}].parameters"
        )
        checks = _array(
            parameters.get("required_status_checks"),
            f"active_rules[{index}].parameters.required_status_checks",
        )
        ruleset_id = rule.get("ruleset_id")
        ruleset_source_type = rule.get("ruleset_source_type")
        ruleset_source = rule.get("ruleset_source")
        source = {
            "source_kind": "RULESET",
            "ruleset_id": (
                _integer(ruleset_id, f"active_rules[{index}].ruleset_id")
                if ruleset_id is not None
                else None
            ),
            "ruleset_source_type": (
                _string(
                    ruleset_source_type,
                    f"active_rules[{index}].ruleset_source_type",
                )
                if ruleset_source_type is not None
                else None
            ),
            "ruleset_source": (
                _string(ruleset_source, f"active_rules[{index}].ruleset_source")
                if ruleset_source is not None
                else None
            ),
        }
        for check_index, check_value in enumerate(checks):
            check = _object(check_value, f"active_rules[{index}].checks[{check_index}]")
            integration_id = check.get("integration_id")
            normalized.append(
                {
                    "context": _string(check.get("context"), "required_check.context"),
                    "integration_id": (
                        _integer(integration_id, "required_check.integration_id")
                        if integration_id is not None
                        else None
                    ),
                    "source": dict(source),
                }
            )
    return normalized


def normalize_branch_protection(payload: Any) -> list[dict[str, Any]]:
    value = _object(payload, "required status protection response")
    normalized: list[dict[str, Any]] = []
    checks = value.get("checks")
    if checks is not None:
        for index, check_value in enumerate(
            _array(checks, "required_status_checks.checks")
        ):
            check = _object(check_value, f"required_status_checks.checks[{index}]")
            app_id = check.get("app_id")
            normalized.append(
                {
                    "context": _string(check.get("context"), "required_check.context"),
                    "integration_id": (
                        _integer(app_id, "required_check.app_id")
                        if app_id is not None
                        else None
                    ),
                    "source": {"source_kind": "BRANCH_PROTECTION"},
                }
            )
    else:
        for context in _array(value.get("contexts"), "required_status_checks.contexts"):
            normalized.append(
                {
                    "context": _string(context, "required_check.context"),
                    "integration_id": None,
                    "source": {"source_kind": "BRANCH_PROTECTION"},
                }
            )
    return normalized


def merge_required_checks(
    checks: list[dict[str, Any]], conflicts: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    grouped: dict[tuple[str, int | None], dict[str, Any]] = {}
    source_counts: Counter[tuple[Any, ...]] = Counter()
    for check in checks:
        identity = (check["context"], check.get("integration_id"))
        source = check["source"]
        source_identity = (
            source["source_kind"],
            source.get("ruleset_id"),
            source.get("ruleset_source_type"),
            source.get("ruleset_source"),
        )
        source_counts[identity + source_identity] += 1
        item = grouped.setdefault(
            identity,
            {
                "context": check["context"],
                "integration_id": check.get("integration_id"),
                "sources": [],
            },
        )
        if source not in item["sources"]:
            item["sources"].append(dict(source))

    for identity, count in sorted(source_counts.items(), key=lambda item: str(item[0])):
        if count > 1:
            context, integration_id, source_kind, ruleset_id, _, _ = identity
            conflict = {
                "code": "REQUIRED_CHECK_SOURCE_IDENTITY_DUPLICATED",
                "context": context,
                "source_kind": source_kind,
                "integration_id": integration_id,
                "candidate_count": count,
            }
            if ruleset_id is not None:
                conflict["ruleset_id"] = ruleset_id
            conflicts.append(conflict)

    merged = list(grouped.values())
    for item in merged:
        item["sources"].sort(key=_required_check_source_sort_key)

    context_counts = Counter(item["context"] for item in merged)
    incomplete = {
        item["context"] for item in merged if item.get("integration_id") is None
    }
    for context in sorted(incomplete):
        if context_counts[context] > 1:
            conflicts.append(
                {
                    "code": "REQUIRED_CHECK_IDENTITY_AMBIGUOUS",
                    "context": context,
                    "candidate_count": context_counts[context],
                }
            )
    return sorted(
        merged,
        key=lambda item: (
            item["context"],
            -1 if item["integration_id"] is None else item["integration_id"],
        ),
    )


def _required_check_source_sort_key(source: dict[str, Any]) -> tuple[Any, ...]:
    return (
        source["source_kind"],
        -1 if source.get("ruleset_id") is None else source["ruleset_id"],
        source.get("ruleset_source_type") or "",
        source.get("ruleset_source") or "",
    )


def normalize_observed_checks(
    check_runs_payload: Any,
    statuses_payload: Any,
    *,
    target_commit_sha: str,
    conflicts: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    runs_root = _object(check_runs_payload, "check runs response")
    runs = _array(runs_root.get("check_runs"), "check_runs")
    normalized: list[dict[str, Any]] = []
    for index, run_value in enumerate(runs):
        run = _object(run_value, f"check_runs[{index}]")
        app_value = run.get("app")
        app = (
            _object(app_value, f"check_runs[{index}].app")
            if app_value is not None
            else None
        )
        suite_value = run.get("check_suite")
        suite = (
            _object(suite_value, f"check_runs[{index}].check_suite")
            if suite_value is not None
            else None
        )
        head_sha = _sha(run.get("head_sha"), f"check_runs[{index}].head_sha")
        if head_sha != target_commit_sha:
            conflicts.append(
                {
                    "code": "OBSERVED_CHECK_SHA_MISMATCH",
                    "source_kind": "CHECK_RUN",
                    "run_id": _integer(run.get("id"), f"check_runs[{index}].id"),
                    "observed_sha": head_sha,
                }
            )
        normalized.append(
            {
                "source_kind": "CHECK_RUN",
                "name": _string(run.get("name"), f"check_runs[{index}].name"),
                "app_id": (
                    _integer(app.get("id"), f"check_runs[{index}].app.id")
                    if app
                    else None
                ),
                "app_slug": (
                    _string(
                        app.get("slug"), f"check_runs[{index}].app.slug", nullable=True
                    )
                    if app
                    else None
                ),
                "suite_id": (
                    _integer(suite.get("id"), f"check_runs[{index}].check_suite.id")
                    if suite
                    else None
                ),
                "run_id": _integer(run.get("id"), f"check_runs[{index}].id"),
                "status": _string(run.get("status"), f"check_runs[{index}].status"),
                "conclusion": _string(
                    run.get("conclusion"),
                    f"check_runs[{index}].conclusion",
                    nullable=True,
                ),
                "head_sha": head_sha,
            }
        )

    statuses_root = _object(statuses_payload, "combined status response")
    root_sha_value = statuses_root.get("sha")
    if root_sha_value is not None:
        root_sha = _sha(root_sha_value, "combined_status.sha")
        if root_sha != target_commit_sha:
            conflicts.append(
                {
                    "code": "COMBINED_STATUS_SHA_MISMATCH",
                    "observed_sha": root_sha,
                }
            )
    statuses = _array(statuses_root.get("statuses"), "combined_status.statuses")
    for index, status_value in enumerate(statuses):
        status = _object(status_value, f"statuses[{index}]")
        creator_value = status.get("creator")
        creator = (
            _object(creator_value, f"statuses[{index}].creator")
            if creator_value is not None
            else None
        )
        observed_sha = _sha(
            status.get("sha", target_commit_sha), f"statuses[{index}].sha"
        )
        if observed_sha != target_commit_sha:
            conflicts.append(
                {
                    "code": "OBSERVED_CHECK_SHA_MISMATCH",
                    "source_kind": "COMMIT_STATUS",
                    "status_id": _integer(status.get("id"), f"statuses[{index}].id"),
                    "observed_sha": observed_sha,
                }
            )
        normalized.append(
            {
                "source_kind": "COMMIT_STATUS",
                "name": _string(status.get("context"), f"statuses[{index}].context"),
                "creator_id": (
                    _integer(creator.get("id"), f"statuses[{index}].creator.id")
                    if creator
                    else None
                ),
                "creator_login": (
                    _string(
                        creator.get("login"),
                        f"statuses[{index}].creator.login",
                        nullable=True,
                    )
                    if creator
                    else None
                ),
                "status_id": _integer(status.get("id"), f"statuses[{index}].id"),
                "state": _string(status.get("state"), f"statuses[{index}].state"),
                "head_sha": observed_sha,
            }
        )

    for item in normalized:
        if item["source_kind"] == "CHECK_RUN" and item.get("app_id") is None:
            conflicts.append(
                {
                    "code": "OBSERVED_CHECK_IDENTITY_INCOMPLETE",
                    "source_kind": "CHECK_RUN",
                    "run_id": item["run_id"],
                    "name": item["name"],
                }
            )
    source_identities = Counter(
        (
            item["source_kind"],
            item.get("run_id")
            if item["source_kind"] == "CHECK_RUN"
            else item.get("status_id"),
        )
        for item in normalized
    )
    for (source_kind, source_id), count in sorted(source_identities.items()):
        if count > 1:
            conflicts.append(
                {
                    "code": "OBSERVED_CHECK_SOURCE_IDENTITY_DUPLICATED",
                    "source_kind": source_kind,
                    "source_id": source_id,
                    "candidate_count": count,
                }
            )
    return sorted(
        normalized,
        key=lambda item: (
            item["name"],
            item["source_kind"],
            item.get("app_id") or -1,
            item.get("creator_id") or -1,
            item.get("run_id") or item.get("status_id") or -1,
        ),
    )


def normalize_release(
    payload: Any,
    *,
    include_identity: bool,
    include_assets: bool,
    conflicts: list[dict[str, Any]],
) -> dict[str, Any]:
    value = _object(payload, "release response")
    normalized: dict[str, Any] = {}
    if include_identity:
        normalized.update(
            {
                "id": _integer(value.get("id"), "release.id"),
                "tag_name": _string(value.get("tag_name"), "release.tag_name"),
                "target_commitish": _string(
                    value.get("target_commitish"), "release.target_commitish"
                ),
                "draft": _boolean(value.get("draft"), "release.draft"),
                "prerelease": _boolean(value.get("prerelease"), "release.prerelease"),
                "immutable": _boolean(
                    value.get("immutable"), "release.immutable", nullable=True
                ),
                "published_at": _string(
                    value.get("published_at"), "release.published_at", nullable=True
                ),
            }
        )
    if include_assets:
        assets: list[dict[str, Any]] = []
        for index, asset_value in enumerate(
            _array(value.get("assets"), "release.assets")
        ):
            asset = _object(asset_value, f"release.assets[{index}]")
            assets.append(
                {
                    "id": _integer(asset.get("id"), f"release.assets[{index}].id"),
                    "name": _string(asset.get("name"), f"release.assets[{index}].name"),
                    "size_bytes": _integer(
                        asset.get("size"), f"release.assets[{index}].size"
                    ),
                    "state": _string(
                        asset.get("state"), f"release.assets[{index}].state"
                    ),
                    "digest": _string(
                        asset.get("digest"),
                        f"release.assets[{index}].digest",
                        nullable=True,
                    ),
                }
            )
        normalized["assets"] = sorted(
            assets, key=lambda item: (item["name"], item["id"])
        )
        identities = Counter((item["id"], item["name"]) for item in assets)
        for (asset_id, name), count in sorted(identities.items()):
            if count > 1:
                conflicts.append(
                    {
                        "code": "RELEASE_ASSET_IDENTITY_DUPLICATED",
                        "asset_id": asset_id,
                        "name": name,
                        "candidate_count": count,
                    }
                )
    return normalized


def normalize_pages(payload: Any) -> dict[str, Any]:
    value = _object(payload, "pages response")
    source_value = value.get("source")
    source = _object(source_value, "pages.source") if source_value is not None else None
    return {
        "status": _string(value.get("status"), "pages.status", nullable=True),
        "cname": _string(value.get("cname"), "pages.cname", nullable=True),
        "custom_404": _boolean(
            value.get("custom_404"), "pages.custom_404", nullable=True
        ),
        "html_url": _string(value.get("html_url"), "pages.html_url", nullable=True),
        "build_type": _string(
            value.get("build_type"), "pages.build_type", nullable=True
        ),
        "source": (
            {
                "branch": _string(source.get("branch"), "pages.source.branch"),
                "path": _string(source.get("path"), "pages.source.path"),
            }
            if source
            else None
        ),
        "https_enforced": _boolean(
            value.get("https_enforced"), "pages.https_enforced", nullable=True
        ),
        "public": _boolean(value.get("public"), "pages.public", nullable=True),
        "protected_domain_state": _string(
            value.get("protected_domain_state"),
            "pages.protected_domain_state",
            nullable=True,
        ),
        "pending_domain_unverified_at": _string(
            value.get("pending_domain_unverified_at"),
            "pages.pending_domain_unverified_at",
            nullable=True,
        ),
    }


def ref_target(payload: Any) -> tuple[str, str, str]:
    value = _object(payload, "tag ref response")
    ref_name = _string(value.get("ref"), "tag_ref.ref")
    target = _object(value.get("object"), "tag_ref.object")
    return (
        ref_name,
        _string(target.get("type"), "tag_ref.object.type"),
        _sha(target.get("sha"), "tag_ref.object.sha"),
    )


def annotated_tag_target(payload: Any) -> tuple[str, str, str]:
    value = _object(payload, "annotated tag response")
    tag_sha = _sha(value.get("sha"), "annotated_tag.sha")
    target = _object(value.get("object"), "annotated_tag.object")
    return (
        tag_sha,
        _string(target.get("type"), "annotated_tag.object.type"),
        _sha(target.get("sha"), "annotated_tag.object.sha"),
    )
