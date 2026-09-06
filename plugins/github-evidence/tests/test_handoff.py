from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from veritrail.canonical import canonical_json_bytes
from veritrail.evidence import import_evidence_document, verify_imported_evidence

from veritrail_github.errors import ContractError, HandoffError
from veritrail_github.handoff import (
    build_handoff_manifest,
    import_verified_handoff_evidence,
    publish_handoff_manifest,
)
from veritrail_github.paired_collection import (
    PairedCollectionResult,
    PairedSideOutcome,
)
from veritrail_github.publisher import publish_evidence


def _artifact(role: str, value: str, *, coverage: str = "COMPLETE"):
    return import_evidence_document(
        {
            "schema_version": "0.1",
            "evidence_type": "platform.fixture",
            "source": "p3-handoff-fixture/0.1",
            "captured_at": "2026-09-06T00:00:00Z",
            "facts": {"value": value},
            "metadata": {
                "veritrail_observation": {
                    "collector_role": role,
                    "coverage": coverage,
                    "collection_session_id": "must-not-enter-manifest",
                }
            },
        },
        f"{role}.json",
    )


def _published_outcome(role: str, path: Path, digest: str) -> PairedSideOutcome:
    return PairedSideOutcome(
        collector_role=role,
        requested_output_path=path,
        artifact_path=path,
        artifact_sha256=digest,
        coverage="COMPLETE",
        state="PUBLISHED",
        error_code=None,
    )


def _result(
    api_path: Path,
    api_digest: str,
    render_path: Path,
    render_digest: str,
) -> PairedCollectionResult:
    return PairedCollectionResult(
        collection_session_id="must-not-enter-manifest",
        collection_order=("github-api", "github-public-render"),
        api=_published_outcome("github-api", api_path, api_digest),
        render=_published_outcome(
            "github-public-render", render_path, render_digest
        ),
    )


class HandoffTests(unittest.TestCase):
    def _published_pair(self, root: Path):
        api = _artifact("github-api", "api-a")
        render = _artifact("github-public-render", "render-a")
        api_path = root / "api.json"
        render_path = root / "render.json"
        publish_evidence(api_path, api)
        publish_evidence(render_path, render)
        return api, render, api_path, render_path

    def test_publisher_and_verifier_preserve_exact_snapshot_identity(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            api, render, api_path, render_path = self._published_pair(root)
            manifest_path = root / "handoff.json"
            manifest = publish_handoff_manifest(
                manifest_path,
                _result(api_path, api.sha256, render_path, render.sha256),
            )

            self.assertEqual(
                manifest,
                json.loads(manifest_path.read_text(encoding="utf-8")),
            )
            self.assertNotIn("collection_session_id", canonical_json_bytes(manifest).decode())
            self.assertNotIn("coverage", canonical_json_bytes(manifest).decode())
            imported = import_verified_handoff_evidence(manifest_path)
            self.assertEqual((api.sha256, render.sha256), tuple(a.sha256 for a in imported))

            replacement = _artifact("github-api", "api-b")
            api_path.unlink()
            publish_evidence(api_path, replacement)
            verify_imported_evidence(imported[0])
            self.assertEqual("api-a", imported[0].document["facts"]["value"])
            self.assertNotEqual(replacement.sha256, imported[0].sha256)

    def test_manifest_publish_is_create_new_and_cleans_failed_staging(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            api, render, api_path, render_path = self._published_pair(root)
            result = _result(api_path, api.sha256, render_path, render.sha256)
            manifest_path = root / "handoff.json"
            publish_handoff_manifest(manifest_path, result)
            original = manifest_path.read_bytes()
            with self.assertRaisesRegex(HandoffError, "refusing to overwrite"):
                publish_handoff_manifest(manifest_path, result)
            self.assertEqual(original, manifest_path.read_bytes())

            failed_path = root / "failed-handoff.json"
            with mock.patch(
                "veritrail_github.publisher.os.link",
                side_effect=OSError("synthetic link failure"),
            ):
                with self.assertRaisesRegex(HandoffError, "atomic create-new"):
                    publish_handoff_manifest(failed_path, result)
            self.assertFalse(failed_path.exists())
            self.assertEqual([], list(root.glob(".*.staging")))

    def test_verifier_rejects_missing_digest_drift_and_role_mismatch(self) -> None:
        cases = ("missing", "digest", "role")
        for case in cases:
            with self.subTest(case=case), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                api, render, api_path, render_path = self._published_pair(root)
                manifest_path = root / "handoff.json"
                manifest = build_handoff_manifest(
                    _result(api_path, api.sha256, render_path, render.sha256),
                    manifest_path=manifest_path,
                )
                if case == "missing":
                    api_path.unlink()
                elif case == "digest":
                    manifest["sides"][0]["evidence_sha256"] = "f" * 64
                else:
                    wrong = _artifact("github-public-render", "wrong-role")
                    api_path.unlink()
                    publish_evidence(api_path, wrong)
                    manifest["sides"][0]["evidence_sha256"] = wrong.sha256
                manifest_path.write_bytes(canonical_json_bytes(manifest) + b"\n")

                with self.assertRaises(HandoffError):
                    import_verified_handoff_evidence(manifest_path)

    def test_verifier_rejects_symlink_selected_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            api = _artifact("github-api", "api-a")
            render = _artifact("github-public-render", "render-a")
            api_target = root / "api-target.json"
            api_target.write_bytes(canonical_json_bytes(api.document) + b"\n")
            api_path = root / "api.json"
            try:
                api_path.symlink_to(api_target)
            except OSError as exc:
                self.skipTest(f"symlink creation unavailable: {exc}")
            render_path = root / "render.json"
            publish_evidence(render_path, render)
            manifest_path = root / "handoff.json"
            manifest = build_handoff_manifest(
                _result(api_path, api.sha256, render_path, render.sha256),
                manifest_path=manifest_path,
            )
            manifest_path.write_bytes(canonical_json_bytes(manifest) + b"\n")

            with self.assertRaises(HandoffError):
                import_verified_handoff_evidence(manifest_path)

    def test_verifier_does_not_filter_partial_or_error_coverage(self) -> None:
        for coverage in ("PARTIAL", "ERROR"):
            with self.subTest(coverage=coverage), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                api = _artifact("github-api", "api-a", coverage=coverage)
                render = _artifact(
                    "github-public-render", "render-a", coverage=coverage
                )
                api_path = root / "api.json"
                render_path = root / "render.json"
                publish_evidence(api_path, api)
                publish_evidence(render_path, render)
                manifest_path = root / "handoff.json"
                publish_handoff_manifest(
                    manifest_path,
                    _result(api_path, api.sha256, render_path, render.sha256),
                )

                imported = import_verified_handoff_evidence(manifest_path)
                self.assertEqual(2, len(imported))
                self.assertEqual(
                    coverage,
                    imported[0].document["metadata"]["veritrail_observation"][
                        "coverage"
                    ],
                )

    def test_builder_rejects_published_evidence_outside_manifest_directory(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            elsewhere = root / "elsewhere"
            elsewhere.mkdir()
            api = _artifact("github-api", "api-a")
            render = _artifact("github-public-render", "render-a")
            api_path = elsewhere / "api.json"
            render_path = root / "render.json"
            with self.assertRaisesRegex(ContractError, "share the handoff"):
                build_handoff_manifest(
                    _result(api_path, api.sha256, render_path, render.sha256),
                    manifest_path=root / "handoff.json",
                )


if __name__ == "__main__":
    unittest.main()
