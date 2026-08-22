from __future__ import annotations

import argparse
import copy
import json
import os
import shutil
import socket
import subprocess
import sys
from pathlib import Path
from typing import Any, Callable
from urllib.parse import urlsplit


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))

from scripts.m11_gatea_acceptance import (
    bootstrap_artifact,
    port_is_free,
    read_json,
    scan_sensitive,
    verify_single_application_artifact,
    wait_for_port_free,
    write_json,
)
from veritrail.bootstrap_preview import build_bootstrap_preview, resolve_bootstrap
from veritrail.bootstrap_public_run import BootstrapPublicRunResult, run_bootstrap_bundle
from veritrail.catalog import build_catalog, validate_bundle
from veritrail.comparison import create_comparison_bundle
from veritrail.plan import seal_plan
from veritrail.project_profile import seal_project_profile
from veritrail.resources import host_memory_bytes


APPLICATION_PORT = 18776
CONTRACT_VERSION = "1.0"
EXPECTED_SUBJECT_REF = "076be2f92194b90e31535d4583ac4d5e72922794"
EXPECTED_M14_CONTRACT_COMMIT = "8147579825ebfe42a1f619a42bd7411c4931827d"
EXPECTED_PROFILE_SHA256 = "afed07195c7d6285977109819bdbdaa9af7e1f967344cfa6c725038c4e5c45b0"
EXPECTED_POSITIVE_PLAN_SHA256 = "11c27beb4a3fbbb6635232f0944d5ba235d276ff287174bf3a3d610ba21714f3"
EXPECTED_NEGATIVE_PLAN_SHA256 = "303fe6581c96c7094afaec32bd862ddb7371016371aeb69c165106654cddb475"
MEBIBYTE = 1024 * 1024

PUBLIC_PAGES = (
    ("/index.html", "墨叙"),
    ("/works/sushi/", "苏轼生平全记录"),
    ("/works/darkroom/", "暗室 · 藏书"),
    ("/works/liuyong/", "乐章集"),
    ("/works/wangwei/", "空山见王维"),
    ("/works/night-voyage/", "夜航船"),
)
GALLERY_WORK_IDS = ("darkroom", "liuyong", "sushi", "wangwei", "night-voyage")
POSITIVE_DOCUMENTS_PER_VIEWPORT = 10
SCREENSHOT_NAMES = ("gallery", "sushi", "darkroom", "night-voyage")
RUNS = (
    ("m14-ink-positive-01", "positive", "NONE", "COMPLETED", "PASS"),
    (
        "m14-ink-browser-negative-01",
        "browser-negative",
        "BROWSER_HARD_FAILURE",
        "COMPLETED",
        "FAIL",
    ),
    ("m14-ink-port-conflict-01", "positive", None, "ABORTED", "PENDING"),
    (
        "m14-ink-recovery-positive-02",
        "positive",
        "NONE",
        "COMPLETED",
        "PASS",
    ),
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run the preregistered M14 InkNarratives public-surface matrix."
    )
    parser.add_argument("--subject-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args()


def raw_profile() -> dict[str, Any]:
    return {
        "schema_version": "0.2",
        "topology": "SINGLE_APPLICATION",
        "profile_id": "m14-inknarratives-single-app",
        "version": 1,
        "platform": "WINDOWS_11",
        "cold_state": "C1_PROCESS_COLD",
        "nodes": [
            {
                "node_id": "application",
                "role": "APPLICATION",
                "adapter": "TRUSTED_PROCESS_SERVICE",
                "depends_on": [],
                "tool_binding": "python-application",
                "arguments": [
                    {"literal": "-m"},
                    {"literal": "http.server"},
                    {"node_port": "application"},
                    {"literal": "--bind"},
                    {"literal": "127.0.0.1"},
                ],
                "working_directory": ".",
                "environment": {
                    "inherit": ["SYSTEMROOT", "WINDIR"],
                    "set": {"PYTHONDONTWRITEBYTECODE": "1"},
                },
                "port": APPLICATION_PORT,
                "readiness": {
                    "adapter": "HTTP_GET_LOOPBACK_OWNED_PID",
                    "path": "/index.html",
                    "expected_status": 200,
                    "attempt_timeout_ms": 500,
                    "total_timeout_ms": 10000,
                    "interval_ms": 100,
                    "consecutive_successes": 2,
                    "max_response_bytes": 65536,
                },
                "limits": {
                    "max_stdout_bytes": 262144,
                    "max_stderr_bytes": 262144,
                    "max_processes": 8,
                    "max_job_memory_mb": 512,
                },
                "shutdown": {
                    "adapter": "JOB_TERMINATE_AFTER_CAPTURE",
                    "process_release_timeout_ms": 5000,
                    "port_release_timeout_ms": 5000,
                    "reader_shutdown_timeout_ms": 5000,
                },
            }
        ],
        "start_order": ["application"],
        "teardown_order": ["application"],
        "application_node_id": "application",
        "subject_watch_roots": ["."],
        "max_watch_files": 2000,
        "max_watch_total_bytes": 67108864,
        "lifecycle_timeout_ms": 120000,
    }


def _browser_steps(origin: str) -> list[dict[str, Any]]:
    gallery = origin + "/index.html"
    return [
        {"id": "gallery-main-visible", "action": "expect_visible", "selector": "main"},
        {
            "id": "gallery-title",
            "action": "expect_text",
            "selector": "h1",
            "value": "墨叙",
        },
        {
            "id": "gallery-works-visible",
            "action": "expect_visible",
            "selector": "#works",
        },
        {
            "id": "gallery-works-title",
            "action": "expect_text",
            "selector": "#works-title",
            "value": "在线展卷",
        },
        *[
            {
                "id": f"gallery-work-{work_id}",
                "action": "expect_visible",
                "selector": f'[data-work="{work_id}"]',
            }
            for work_id in GALLERY_WORK_IDS
        ],
        *[
            {
                "id": f"gallery-link-{work_id}",
                "action": "expect_visible",
                "selector": f'[data-work-link="{work_id}"]',
            }
            for work_id in GALLERY_WORK_IDS
        ],
        {"id": "gallery-shot", "action": "screenshot", "name": "gallery"},
        {"id": "sushi-goto", "action": "goto", "url": origin + "/works/sushi/"},
        {
            "id": "sushi-title",
            "action": "expect_text",
            "selector": "h1",
            "value": "苏轼生平全记录",
        },
        {
            "id": "sushi-chapter-click",
            "action": "click",
            "selector": 'a[href="#chapter11"]',
        },
        {
            "id": "sushi-chapter-visible",
            "action": "expect_visible",
            "selector": "#chapter11",
        },
        {"id": "sushi-reading-toggle", "action": "click", "selector": ".reading-toggle"},
        {"id": "sushi-shot", "action": "screenshot", "name": "sushi"},
        {"id": "sushi-return-gallery", "action": "goto", "url": gallery},
        {
            "id": "sushi-return-title",
            "action": "expect_text",
            "selector": "h1",
            "value": "墨叙",
        },
        {
            "id": "darkroom-goto",
            "action": "goto",
            "url": origin + "/works/darkroom/",
        },
        {
            "id": "darkroom-title",
            "action": "expect_text",
            "selector": "h1",
            "value": "暗室 · 藏书",
        },
        {
            "id": "darkroom-library-visible",
            "action": "expect_visible",
            "selector": "#library",
        },
        {
            "id": "darkroom-book-click",
            "action": "click",
            "selector": '.book[data-title="封装之书"]',
        },
        {
            "id": "darkroom-reader-title",
            "action": "expect_text",
            "selector": "#readerTitle",
            "value": "封装之书",
        },
        {"id": "darkroom-shot", "action": "screenshot", "name": "darkroom"},
        {"id": "darkroom-return-gallery", "action": "goto", "url": gallery},
        {
            "id": "darkroom-return-title",
            "action": "expect_text",
            "selector": "h1",
            "value": "墨叙",
        },
        {"id": "liuyong-goto", "action": "goto", "url": origin + "/works/liuyong/"},
        {
            "id": "liuyong-title",
            "action": "expect_text",
            "selector": "h1",
            "value": "乐章集",
        },
        {
            "id": "liuyong-juan-click",
            "action": "click",
            "selector": 'a[href="#juan8"]',
        },
        {
            "id": "liuyong-juan-visible",
            "action": "expect_visible",
            "selector": "#juan8",
        },
        {
            "id": "liuyong-atmosphere-toggle",
            "action": "click",
            "selector": ".atmosphere-toggle",
        },
        {"id": "liuyong-return-gallery", "action": "goto", "url": gallery},
        {
            "id": "liuyong-return-title",
            "action": "expect_text",
            "selector": "h1",
            "value": "墨叙",
        },
        {"id": "wangwei-goto", "action": "goto", "url": origin + "/works/wangwei/"},
        {
            "id": "wangwei-title",
            "action": "expect_text",
            "selector": "h1",
            "value": "空山见王维",
        },
        {
            "id": "wangwei-chapter-click",
            "action": "click",
            "selector": 'a[href="#c6"]',
        },
        {
            "id": "wangwei-chapter-visible",
            "action": "expect_visible",
            "selector": "#c6",
        },
        {"id": "wangwei-return-gallery", "action": "goto", "url": gallery},
        {
            "id": "wangwei-return-title",
            "action": "expect_text",
            "selector": "h1",
            "value": "墨叙",
        },
        {
            "id": "night-voyage-goto",
            "action": "goto",
            "url": origin + "/works/night-voyage/",
        },
        {
            "id": "night-voyage-title",
            "action": "expect_text",
            "selector": "h1",
            "value": "夜航船",
        },
        {
            "id": "night-voyage-cabin-visible",
            "action": "expect_visible",
            "selector": "#cabin",
        },
        {
            "id": "night-voyage-book-click",
            "action": "click",
            "selector": '.book[data-book="mountain"]',
        },
        {
            "id": "night-voyage-reader-title",
            "action": "expect_text",
            "selector": "#reader-title",
            "value": "空山之后",
        },
        {
            "id": "night-voyage-shot",
            "action": "screenshot",
            "name": "night-voyage",
        },
    ]


def raw_positive_plan(profile_sha256: str) -> dict[str, Any]:
    plan = read_json(REPOSITORY_ROOT / "examples" / "bootstrap" / "plan-positive.json")
    origin = f"http://127.0.0.1:{APPLICATION_PORT}"
    plan["plan_id"] = "m14-inknarratives-public-positive"
    plan["version"] = 3
    plan["subject"] = {
        "id": "inknarratives",
        "version": "public-surface-2026-08-21",
        "source_ref": EXPECTED_SUBJECT_REF,
    }
    plan["question"] = (
        "Can the frozen VeriTrail single-application capability prove the exact "
        "InkNarratives public gallery, all five works, representative interactions, "
        "return-to-gallery routes, two viewports and complete cleanup?"
    )
    plan["baseline"] = {
        "id": "m14-self-single-application-capability",
        "status": "VALID",
        "fingerprint": "c8cae904d6091cf8d2b7e55c63b50308d80d63e340e1cd2afdd2a80c903e0ed6",
        "tolerances": {
            "viewport_count": 2,
            "unexpected_browser_errors": 0,
            "cleanup_failures": 0,
        },
    }
    plan["variables"] = [
        {
            "name": "project_bootstrap_topology",
            "role": "PRIMARY",
            "value": "veritrail_managed_windows_c1_single_application",
            "source": "sealed-plan",
        },
        {
            "name": "subject_ref",
            "role": "CONTROLLED",
            "value": EXPECTED_SUBJECT_REF,
            "source": "sealed-plan",
        },
        {
            "name": "browser_engine",
            "role": "CONTROLLED",
            "value": "chromium",
            "source": "browser-adapter",
        },
        {
            "name": "browser_headless",
            "role": "CONTROLLED",
            "value": True,
            "source": "sealed-plan",
        },
        {
            "name": "viewport_profile_count",
            "role": "CONTROLLED",
            "value": 2,
            "unit": "profiles",
            "source": "sealed-plan",
        },
        {
            "name": "public_page_count",
            "role": "CONTROLLED",
            "value": len(PUBLIC_PAGES),
            "unit": "pages",
            "source": "sealed-plan",
        },
    ]
    for assertion in plan["assertions"]:
        assertion["id"] = assertion["id"].replace("m11-", "m14-ink-", 1)
        if assertion["id"] == "m14-ink-browser-screenshot-coverage":
            assertion["expected"] = len(SCREENSHOT_NAMES) * 2
    plan["preflight"]["ports"] = [{"port": APPLICATION_PORT, "expected": "FREE"}]
    plan["browser"] = {
        "engine": "chromium",
        "headless": True,
        "start_url": origin + PUBLIC_PAGES[0][0],
        "allowed_origins": [origin],
        "timeout_ms": 10000,
        "viewports": [
            {"name": "desktop", "width": 1440, "height": 960, "is_mobile": False},
            {"name": "mobile", "width": 390, "height": 844, "is_mobile": True},
        ],
        "steps": _browser_steps(origin),
        "screenshot_safety": "UNREDACTED_OPERATOR_ACKNOWLEDGED",
        "max_job_memory_mb": 1536,
    }
    plan["bootstrap_profile"] = {
        "profile_id": "m14-inknarratives-single-app",
        "profile_version": 1,
        "profile_sha256": profile_sha256,
    }
    plan["change_scope"] = {
        "level": "L3_SYSTEM",
        "owner": "VeriTrail M14 / InkNarratives public validation",
        "expected_blast_radius": (
            "M14 external-target consumption, public browser flow, immutable Bundle "
            "validation, Catalog, Comparison and release acceptance"
        ),
        "consumers": [
            "project-profile-validator",
            "plan-validator",
            "bootstrap-preview",
            "bootstrap-lifecycle",
            "resource-monitor",
            "browser-adapter",
            "artifact-store",
            "verdict-engine",
            "catalog",
            "comparison",
            "workbench",
        ],
    }
    plan["reproduction_steps"] = [
        "Confirm public InkNarratives origin/main equals the preregistered commit.",
        "Run the target-native repository verifier before the first Run.",
        "Seal ProjectProfile 0.2 and Plan 0.7 before browser execution.",
        "Validate four immutable Bundles and compare only the two positive Runs.",
    ]
    plan["cleanup_steps"] = [
        "Close Playwright contexts and Chromium.",
        "Terminate the owned application Job and release stream readers.",
        f"Verify port {APPLICATION_PORT}, run-work and staging are released.",
        "Run the target-native verifier again and confirm the Subject is unchanged.",
    ]
    return plan


def raw_browser_negative_plan(profile_sha256: str) -> dict[str, Any]:
    plan = raw_positive_plan(profile_sha256)
    plan["plan_id"] = "m14-inknarratives-public-browser-negative"
    missing = next(
        step for step in plan["browser"]["steps"] if step["id"] == "gallery-works-visible"
    )
    missing["selector"] = "#veritrail-m14-missing-gallery"
    return plan


def _git(subject_root: Path, *arguments: str) -> str:
    completed = subprocess.run(
        ["git", "-C", str(subject_root), *arguments],
        check=True,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace",
        creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
    )
    return completed.stdout.strip()


def run_native_verifier(subject_root: Path) -> dict[str, Any]:
    completed = subprocess.run(
        ["node", "scripts/verify-repository.mjs"],
        cwd=subject_root,
        check=True,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace",
        creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
    )
    message = completed.stdout.strip()
    expected = "Repository verification passed: gallery + 5 standalone HTML demos."
    if message != expected or completed.stderr.strip():
        raise AssertionError("InkNarratives native verifier output differs from the contract")
    return {"status": "PASS", "message": message}


def verify_subject(subject_root: Path, *, remote_readback: bool) -> dict[str, Any]:
    if not subject_root.is_dir():
        raise AssertionError("the preregistered Subject root is unavailable")
    head = _git(subject_root, "rev-parse", "HEAD")
    if head != EXPECTED_SUBJECT_REF:
        raise AssertionError("InkNarratives HEAD differs from the preregistered ref")
    if _git(subject_root, "status", "--porcelain=v1"):
        raise AssertionError("InkNarratives worktree is not clean")
    if Path(_git(subject_root, "rev-parse", "--show-toplevel")).resolve() != subject_root:
        raise AssertionError("the selected Subject root is not the Git worktree root")
    environment_files = sorted(
        path.name
        for path in subject_root.rglob("*")
        if path.is_file() and (path.name == ".env" or path.name.startswith(".env."))
    )
    if environment_files:
        raise AssertionError("InkNarratives contains an environment file")
    root_html = {path.name for path in subject_root.glob("*.html")}
    expected_root = {
        "404.html",
        "index.html",
        "苏轼.html",
        "暗室.html",
        "柳永.html",
        "王维.html",
        "长卷.html",
    }
    if root_html != expected_root:
        raise AssertionError("InkNarratives root HTML set differs from the contract")
    public_work_pages = {
        path.parent.name
        for path in (subject_root / "works").glob("*/index.html")
        if path.is_file()
    }
    if public_work_pages != set(GALLERY_WORK_IDS):
        raise AssertionError("InkNarratives public works set differs from the contract")
    remote_commit = None
    if remote_readback:
        if _git(subject_root, "remote", "get-url", "origin") != (
            "https://github.com/NoctilumeDev/InkNarratives.git"
        ):
            raise AssertionError("InkNarratives origin is not the preregistered public remote")
        values = _git(subject_root, "ls-remote", "origin", "refs/heads/main").split()
        if len(values) != 2 or values[0] != EXPECTED_SUBJECT_REF:
            raise AssertionError("public origin/main differs from the preregistered ref")
        remote_commit = values[0]
    return {
        "head": head,
        "worktree_clean": True,
        "remote_readback_commit": remote_commit,
        "environment_file_count": len(environment_files),
        "root_html_count": len(root_html),
        "public_work_count": len(public_work_pages),
    }


def prepare_authorities(
    output: Path, subject_root: Path, bindings: Path
) -> dict[str, dict[str, Any]]:
    profile = seal_project_profile(raw_profile())
    if profile["seal"]["digest"] != EXPECTED_PROFILE_SHA256:
        raise AssertionError("M14 Profile digest drifted")
    drafts = {
        "positive": raw_positive_plan(profile["seal"]["digest"]),
        "browser-negative": raw_browser_negative_plan(profile["seal"]["digest"]),
    }
    expected = {
        "positive": EXPECTED_POSITIVE_PLAN_SHA256,
        "browser-negative": EXPECTED_NEGATIVE_PLAN_SHA256,
    }
    authorities: dict[str, dict[str, Any]] = {}
    for name, draft in drafts.items():
        plan = seal_plan(draft, profile)
        if plan["seal"]["digest"] != expected[name]:
            raise AssertionError(f"M14 {name} Plan digest drifted")
        preview = build_bootstrap_preview(
            plan,
            profile,
            subject_root=subject_root,
            tool_bindings_path=bindings,
        )
        authority_root = output / "authorities" / name
        profile_path = authority_root / "sealed-profile.json"
        plan_path = authority_root / "sealed-plan.json"
        preview_path = authority_root / "bootstrap-preview.json"
        write_json(profile_path, profile)
        write_json(plan_path, plan)
        write_json(preview_path, preview)
        authorities[name] = {
            "profile": profile,
            "plan": plan,
            "preview": preview,
            "frozen_bytes": {
                "profile": profile_path.read_bytes(),
                "plan": plan_path.read_bytes(),
                "preview": preview_path.read_bytes(),
            },
            "paths": {
                "profile": profile_path,
                "plan": plan_path,
                "preview": preview_path,
            },
        }
    return authorities


def verify_authorities_unchanged(authorities: dict[str, dict[str, Any]]) -> None:
    for name, authority in authorities.items():
        for item in ("profile", "plan", "preview"):
            if authority["paths"][item].read_bytes() != authority["frozen_bytes"][item]:
                raise AssertionError(f"M14 {name} {item} authority changed after sealing")


def run_scenario(
    *,
    run_id: str,
    authority_name: str,
    authorities: dict[str, dict[str, Any]],
    subject_root: Path,
    bindings: Path,
    runs_root: Path,
) -> tuple[BootstrapPublicRunResult, dict[str, Any]]:
    authority = authorities[authority_name]
    resolver: Callable[..., Any] = resolve_bootstrap
    external_socket: socket.socket | None = None
    recovery = {"external_owner_preserved": None, "actual_resource_recovery": None}

    if run_id == "m14-ink-port-conflict-01":

        def resolve_then_contest(*args: Any, **kwargs: Any) -> Any:
            nonlocal external_socket
            resolved = resolve_bootstrap(*args, **kwargs)
            external_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            exclusive = getattr(socket, "SO_EXCLUSIVEADDRUSE", None)
            if exclusive is not None:
                external_socket.setsockopt(socket.SOL_SOCKET, exclusive, 1)
            external_socket.bind(("127.0.0.1", APPLICATION_PORT))
            external_socket.listen(socket.SOMAXCONN)
            return resolved

        resolver = resolve_then_contest

    try:
        result = run_bootstrap_bundle(
            authority["plan"],
            authority["profile"],
            subject_root=subject_root,
            tool_bindings_path=bindings,
            approved_preview_sha256=authority["preview"]["preview_sha256"],
            output=runs_root / run_id,
            run_id=run_id,
            resolver=resolver,
        )
        if external_socket is not None:
            recovery["external_owner_preserved"] = (
                external_socket.getsockopt(socket.SOL_SOCKET, socket.SO_ACCEPTCONN) == 1
            )
        return result, recovery
    finally:
        if external_socket is not None:
            external_socket.close()
            recovery["actual_resource_recovery"] = wait_for_port_free(APPLICATION_PORT)


def evidence_artifact(bundle: Path, evidence_type: str) -> dict[str, Any] | None:
    manifest = read_json(bundle / "evidence-manifest.json")
    entries = [
        item for item in manifest["artifacts"] if item["evidence_type"] == evidence_type
    ]
    if not entries:
        return None
    if len(entries) != 1:
        raise AssertionError(f"{bundle.name} has multiple {evidence_type} artifacts")
    return read_json(bundle / Path(*entries[0]["path"].split("/")))


def verify_browser_artifact(
    run_id: str, document: dict[str, Any], *, positive: bool
) -> None:
    facts = document["facts"]
    zero_fields = (
        "unexpected_console_error_count",
        "page_error_count",
        "failed_request_count",
        "unexpected_http_error_count",
        "duplicate_write_request_group_count",
        "horizontal_overflow_viewport_count",
    )
    if any(facts[field] != 0 for field in zero_fields):
        raise AssertionError(f"{run_id} Browser evidence contains an unexpected error")
    if facts["viewport_count"] != 2 or facts["cleanup_complete"] is not True:
        raise AssertionError(f"{run_id} Browser coverage or cleanup is incomplete")

    documents = [
        item
        for item in facts["network"]
        if item["method"] == "GET" and item["resource_type"] == "document"
    ]
    expected_paths = {path for path, _ in PUBLIC_PAGES} if positive else {"/index.html"}
    expected_count = POSITIVE_DOCUMENTS_PER_VIEWPORT if positive else 1
    for viewport in ("desktop", "mobile"):
        viewport_documents = [item for item in documents if item["viewport"] == viewport]
        observed = {
            urlsplit(item["url"]).path
            for item in viewport_documents
            if item["status"] == 200
            and item["finished"] is True
            and item["failure"] is None
        }
        if observed != expected_paths or len(viewport_documents) != expected_count:
            raise AssertionError(f"{run_id} did not prove the public route set for {viewport}")
    if len(documents) != expected_count * 2:
        raise AssertionError(f"{run_id} contains an unexpected document navigation")

    if positive:
        if (
            facts["capture_complete"] is not True
            or facts["all_steps_passed"] is not True
            or facts["screenshot_count"] != len(SCREENSHOT_NAMES) * 2
        ):
            raise AssertionError(f"{run_id} positive Browser evidence is incomplete")
        expected_shots = {
            (viewport, name)
            for viewport in ("desktop", "mobile")
            for name in SCREENSHOT_NAMES
        }
        observed_shots = {
            (item["viewport"], item["name"]) for item in facts["screenshots"]
        }
        if observed_shots != expected_shots:
            raise AssertionError(f"{run_id} screenshot coverage differs from the contract")
    else:
        failures = [
            item
            for item in facts["steps"]
            if item["step_id"] == "gallery-works-visible" and item["status"] == "FAILED"
        ]
        if (
            facts["capture_complete"] is not False
            or facts["all_steps_passed"] is not False
            or facts["screenshot_count"] != 0
            or len(failures) != 2
        ):
            raise AssertionError(f"{run_id} did not fail at the preregistered selector")


def verify_bootstrap(run_id: str, document: dict[str, Any]) -> int:
    facts = document["facts"]
    node = facts["nodes"][0]
    successful_readiness = [
        item for item in node["readiness"]["attempts"] if item["result"] == "SUCCESS"
    ]
    response_sizes = {item["response_byte_count"] for item in successful_readiness}
    cleanup = facts["cleanup"]
    if (
        facts["services_ready"] is not True
        or node["readiness"]["ready"] is not True
        or len(successful_readiness) < 2
        or len(response_sizes) != 1
        or not 0 < next(iter(response_sizes)) <= 65536
    ):
        raise AssertionError(f"{run_id} did not remeasure the readiness contract")
    if any(
        item["http_status"] != 200 or item["listener_owner_in_job"] is not True
        for item in successful_readiness
    ):
        raise AssertionError(f"{run_id} readiness did not belong to the owned Job")
    if (
        node["job"]["job_memory_limit_mb"] != 512
        or node["job"]["job_memory_limit_enforced"] is not True
        or node["job"]["active_process_limit"] != 8
        or node["job"]["active_process_limit_enforced"] is not True
        or facts["browser_exercise"]["job_memory_limit_mb"] != 1536
        or facts["browser_exercise"]["job_memory_limit_enforced"] is not True
        or facts["browser_exercise"]["process_cleanup_complete"] is not True
        or facts["resource_observation"]["sampling_complete"] is not True
        or facts["subject_observation"]["scan_complete"] is not True
        or facts["cleanup_complete"] is not True
        or not all(cleanup.values())
    ):
        raise AssertionError(f"{run_id} resource or cleanup facts are incomplete")
    return next(iter(response_sizes))


def main() -> int:
    args = parse_args()
    if os.name != "nt":
        raise AssertionError("M14 InkNarratives acceptance is Windows-only")
    if sys.version_info[:3] != (3, 10, 6):
        raise AssertionError("M14 InkNarratives acceptance requires Python 3.10.6")
    _git(
        REPOSITORY_ROOT,
        "merge-base",
        "--is-ancestor",
        EXPECTED_M14_CONTRACT_COMMIT,
        "HEAD",
    )
    if _git(
        REPOSITORY_ROOT,
        "diff",
        "--name-only",
        EXPECTED_M14_CONTRACT_COMMIT,
        "--",
        "src",
        "schemas",
    ):
        raise AssertionError("M14 changed the candidate Core or public schemas")
    if _git(REPOSITORY_ROOT, "status", "--porcelain=v1"):
        raise AssertionError("VeriTrail worktree must be clean before M14 acceptance")
    harness_commit = _git(REPOSITORY_ROOT, "rev-parse", "HEAD")

    subject_root = args.subject_root.resolve(strict=True)
    output = args.output.absolute()
    if output.exists():
        raise AssertionError("acceptance output already exists")
    if not port_is_free(APPLICATION_PORT):
        raise AssertionError(f"preregistered application port {APPLICATION_PORT} is occupied")
    total_memory, available_memory = host_memory_bytes()
    start_available_mb = available_memory // MEBIBYTE
    if start_available_mb < 4096:
        raise AssertionError("available memory is below the preregistered soft line")
    output.parent.mkdir(parents=True, exist_ok=True)
    if shutil.disk_usage(output.parent).free // MEBIBYTE < 1024:
        raise AssertionError("output volume is below the preregistered hard line")

    initial_subject = verify_subject(subject_root, remote_readback=True)
    initial_native_verification = run_native_verifier(subject_root)
    bindings = output / "inputs" / "tool-bindings.json"
    write_json(
        bindings,
        {
            "schema_version": "0.1",
            "bindings": {
                "python-application": {"executable": str(Path(sys.executable).resolve())}
            },
        },
    )
    authorities = prepare_authorities(output, subject_root, bindings)
    verify_authorities_unchanged(authorities)
    runs_root = output / "runs"
    runs_root.mkdir(parents=True)

    ledger: list[dict[str, Any]] = []
    resources: list[dict[str, Any]] = []
    for ordinal, (run_id, authority_name, expected_stop, status, verdict) in enumerate(
        RUNS, start=1
    ):
        result, recovery = run_scenario(
            run_id=run_id,
            authority_name=authority_name,
            authorities=authorities,
            subject_root=subject_root,
            bindings=bindings,
            runs_root=runs_root,
        )
        if result.report["execution_status"] != status or result.report["verdict"] != verdict:
            raise AssertionError(f"{run_id} status/verdict differs from the contract")
        validated = validate_bundle(runs_root / run_id, runs_root)
        artifact = bootstrap_artifact(runs_root / run_id)
        if artifact is None:
            if run_id != "m14-ink-port-conflict-01":
                raise AssertionError(f"{run_id} did not publish bootstrap Evidence")
            actual_stop = None
        else:
            bootstrap, manifest_entry = artifact
            verify_single_application_artifact(run_id, bootstrap, manifest_entry)
            facts = bootstrap["facts"]
            actual_stop = facts["stop"]["reason"]
            if facts["subject_observation"]["changed"] is not False:
                raise AssertionError(f"{run_id} observed Subject drift")
            readiness_response_bytes = verify_bootstrap(run_id, bootstrap)
            resources.append(
                {
                    "run_id": run_id,
                    "readiness_response_bytes": readiness_response_bytes,
                    "host_available_memory_min_mb": facts["resource_observation"][
                        "host_available_memory_min_mb"
                    ],
                    "core_peak_rss_mb": facts["resource_observation"]["core_peak_rss_mb"],
                    "application_peak_rss_mb": facts["resource_observation"][
                        "application_peak_rss_mb"
                    ],
                    "browser_peak_rss_mb": facts["resource_observation"][
                        "browser_peak_rss_mb"
                    ],
                }
            )
        if actual_stop != expected_stop:
            raise AssertionError(f"{run_id} stop reason differs from the contract")
        browser = evidence_artifact(runs_root / run_id, "browser.session")
        if run_id == "m14-ink-port-conflict-01":
            if browser is not None:
                raise AssertionError("port conflict Run fabricated Browser evidence")
            if (
                recovery["external_owner_preserved"] is not True
                or recovery["actual_resource_recovery"] is not True
            ):
                raise AssertionError("port conflict owner was not preserved and recovered")
        else:
            if browser is None:
                raise AssertionError(f"{run_id} did not publish Browser evidence")
            verify_browser_artifact(
                run_id,
                browser,
                positive=run_id != "m14-ink-browser-negative-01",
            )
        if not port_is_free(APPLICATION_PORT):
            raise AssertionError(f"{run_id} left port {APPLICATION_PORT} occupied")
        if list(output.rglob(".veritrail-*")):
            raise AssertionError(f"{run_id} left owned staging residue")
        subject_state = verify_subject(subject_root, remote_readback=False)
        verify_authorities_unchanged(authorities)
        ledger.append(
            {
                "ordinal": ordinal,
                "run_id": run_id,
                "authority": authority_name,
                "stop_reason": actual_stop,
                "execution_status": validated.execution_status,
                "verdict": validated.verdict,
                "bundle_sha256": validated.bundle_sha256,
                "subject_head": subject_state["head"],
                "subject_clean": subject_state["worktree_clean"],
                "recovery": recovery,
            }
        )

    comparison = create_comparison_bundle(
        baseline=runs_root / "m14-ink-positive-01",
        repeat=runs_root / "m14-ink-recovery-positive-02",
        output=output / "comparison",
    )
    comparison_document = read_json(output / "comparison" / "comparison.json")
    if (
        not comparison.comparable
        or comparison.comparison_status != "MATCH"
        or comparison_document["differences"] != []
    ):
        raise AssertionError("the two positive M14 Runs did not compare as MATCH")

    corrupted = runs_root / "m14-ink-corrupted-copy"
    shutil.copytree(runs_root / "m14-ink-positive-01", corrupted)
    with (corrupted / "report.json").open("ab") as stream:
        stream.write(b"\n")
    catalog = build_catalog(runs_root, output / "catalog")
    if (
        catalog.status != "COMPLETED_WITH_ISSUES"
        or catalog.run_count != 4
        or catalog.issue_count != 1
    ):
        raise AssertionError("Catalog did not accept four Runs and isolate one corrupt copy")

    sensitive_files = scan_sensitive(
        runs_root,
        [
            str(output),
            str(subject_root),
            str(Path.home()),
            "authorization:",
            "set-cookie:",
            "private key",
            ".env",
        ],
    )
    final_native_verification = run_native_verifier(subject_root)
    final_subject = verify_subject(subject_root, remote_readback=True)
    verify_authorities_unchanged(authorities)
    final_port_free = port_is_free(APPLICATION_PORT)
    final_residue = list(output.rglob(".veritrail-*"))
    if not final_port_free or final_residue:
        raise AssertionError("M14 final residual gate failed")

    summary = {
        "schema_version": "0.1",
        "contract_version": CONTRACT_VERSION,
        "platform": "WINDOWS_11",
        "cold_state": "C1_PROCESS_COLD",
        "python": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
        "m14_contract_commit": EXPECTED_M14_CONTRACT_COMMIT,
        "m14_harness_commit": harness_commit,
        "subject": {
            "id": "inknarratives",
            "ref": EXPECTED_SUBJECT_REF,
            "initial": initial_subject,
            "final": final_subject,
            "native_verifier_initial": initial_native_verification,
            "native_verifier_final": final_native_verification,
        },
        "start_resource": {
            "total_memory_mb": total_memory // MEBIBYTE,
            "available_memory_mb": start_available_mb,
        },
        "authorities": {
            name: {
                "profile_sha256": value["profile"]["seal"]["digest"],
                "plan_sha256": value["plan"]["seal"]["digest"],
                "preview_sha256": value["preview"]["preview_sha256"],
            }
            for name, value in authorities.items()
        },
        "runs": ledger,
        "resources": resources,
        "comparison": {
            "status": comparison.comparison_status,
            "difference_count": len(comparison_document["differences"]),
        },
        "catalog": {
            "status": catalog.status,
            "run_count": catalog.run_count,
            "issue_count": catalog.issue_count,
            "corrupted_copy_isolated": True,
        },
        "not_applicable": [
            "pairing",
            "batch",
            "database",
            "middleware",
            "business_writes",
            "multiple_roles",
            "multiple_instances",
            "eventual_consistency",
        ],
        "sensitive_scan": {"checked_text_files": sensitive_files, "matches": 0},
        "residual": {
            "application_port_free": final_port_free,
            "owned_staging_count": len(final_residue),
        },
    }
    write_json(output / "acceptance.json", summary)
    print(json.dumps(summary, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
