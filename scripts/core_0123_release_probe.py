from __future__ import annotations

import argparse
import copy
import json
from importlib.metadata import version
from pathlib import Path
from typing import Any

import veritrail
from veritrail.browser import _classify_host_socket_request_failure
from veritrail.canonical import canonical_json_bytes, sha256_bytes
from veritrail.evidence import ImportedEvidence
from veritrail.verdict import _is_exact_host_socket_collection_failure


EXPECTED_VERSION = "0.12.3"
EXACT_RAW_FAILURE = "net::ERR_NO_BUFFER_SPACE"
NEAR_MISSES = (
    "net::err_no_buffer_space",
    "net::ERR_NO_BUFFER_SPACE_EXTRA",
    "prefix net::ERR_NO_BUFFER_SPACE",
    "net::ERR_CONNECTION_RESET",
    "net::ERR_INSUFFICIENT_RESOURCES",
    "request failed",
    "",
)


class ReleaseProbeFailure(RuntimeError):
    pass


def require(condition: object, message: str) -> None:
    if not condition:
        raise ReleaseProbeFailure(message)


def _browser_artifact(document: dict[str, Any], input_name: str) -> ImportedEvidence:
    encoded = canonical_json_bytes(document)
    return ImportedEvidence(
        document=copy.deepcopy(document),
        sha256=sha256_bytes(encoded),
        size=len(encoded),
        redacted_fields=0,
        input_name=input_name,
    )


def _exact_document() -> dict[str, Any]:
    raw = f"  {EXACT_RAW_FAILURE}\r\n"
    return {
        "schema_version": "0.1",
        "evidence_type": "browser.session",
        "source": "core-0.12.3-release-probe",
        "captured_at": "2026-10-09T00:00:00Z",
        "facts": {
            "network": [{"viewport": "desktop", "failure": raw}],
            "collection_errors": [
                {
                    "collector": "network:desktop",
                    "error_type": "HostSocketNoBufferSpace",
                }
            ],
        },
        "observed_variables": {},
    }


def run(output: Path, expected_source_root: Path | None) -> dict[str, Any]:
    package_path = Path(veritrail.__file__).resolve()
    require(veritrail.__version__ == EXPECTED_VERSION, "Core runtime version drifted")
    require(version("veritrail") == EXPECTED_VERSION, "Core distribution version drifted")
    if expected_source_root is not None:
        source_root = (expected_source_root.resolve() / "src").resolve()
        require(
            not package_path.is_relative_to(source_root),
            "release probe imported Core from the source checkout",
        )

    require(not output.exists(), "release probe output already exists")
    output.parent.mkdir(parents=True, exist_ok=True)

    padded_raw = f"  {EXACT_RAW_FAILURE}\r\n"
    for viewport in ("desktop", "mobile"):
        require(
            _classify_host_socket_request_failure(viewport, padded_raw)
            == (f"network:{viewport}", "HostSocketNoBufferSpace"),
            f"exact {viewport} classification drifted",
        )
    require(padded_raw == f"  {EXACT_RAW_FAILURE}\r\n", "raw failure text mutated")
    for near_miss in NEAR_MISSES:
        require(
            _classify_host_socket_request_failure("desktop", near_miss) is None,
            f"near-miss was over-classified: {near_miss!r}",
        )

    exact_document = _exact_document()
    require(
        _is_exact_host_socket_collection_failure(
            _browser_artifact(exact_document, "exact.json")
        ),
        "exact raw/collector binding was rejected",
    )

    raw_mismatch = copy.deepcopy(exact_document)
    raw_mismatch["facts"]["network"][0]["failure"] = "net::ERR_CONNECTION_RESET"
    require(
        not _is_exact_host_socket_collection_failure(
            _browser_artifact(raw_mismatch, "raw-mismatch.json")
        ),
        "collector projection was accepted without the exact raw Network fact",
    )

    mixed_errors = copy.deepcopy(exact_document)
    mixed_errors["facts"]["collection_errors"].append(
        {"collector": "page:desktop", "error_type": "SyntheticOtherError"}
    )
    require(
        not _is_exact_host_socket_collection_failure(
            _browser_artifact(mixed_errors, "mixed-errors.json")
        ),
        "mixed collector errors were accepted as an exact host-socket world",
    )

    summary = {
        "schema_version": "core-v0.12.3-host-socket-probe/1",
        "status": "PASS",
        "boundary": "CORE_0.12.3_HOST_SOCKET_INSTALLED_DISTRIBUTION",
        "package_version": version("veritrail"),
        "source_checkout_imported": False if expected_source_root is not None else None,
        "exact_failure": EXACT_RAW_FAILURE,
        "exact_viewports": ["desktop", "mobile"],
        "near_miss_count": len(NEAR_MISSES),
        "raw_network_fact_preserved": True,
        "collector_projection_requires_exact_raw_fact": True,
        "mixed_collector_errors_rejected": True,
    }
    output.write_bytes(canonical_json_bytes(summary) + b"\n")
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Verify the installed Core 0.12.3 exact host-socket classification boundary."
        )
    )
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--expected-source-root", type=Path)
    args = parser.parse_args()
    print(
        json.dumps(
            run(args.output.absolute(), args.expected_source_root),
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
