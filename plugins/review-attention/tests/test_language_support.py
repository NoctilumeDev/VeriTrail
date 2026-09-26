from __future__ import annotations

import base64
import copy
import hashlib
import inspect
import json
import sys
import unittest
from pathlib import Path
from unittest import mock


PLUGIN_ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = PLUGIN_ROOT / "src"
TEST_ROOT = PLUGIN_ROOT / "tests"
REPOSITORY_ROOT = PLUGIN_ROOT.parents[1]
FIXTURE_ROOT = (
    REPOSITORY_ROOT
    / "tests"
    / "fixtures"
    / "review-r1-derivation-input-0.1"
    / "reference-lab"
)
for location in (SOURCE_ROOT, TEST_ROOT):
    if str(location) not in sys.path:
        sys.path.insert(0, str(location))

from test_execution_cell import (  # noqa: E402
    _canonical_artifact,
    _policy_document,
    _seal_policy,
)
from veritrail_review import _language_support as language_support  # noqa: E402
from veritrail_review import _language_support_values as language_values  # noqa: E402
from veritrail_review._execution_cell_application import (  # noqa: E402
    build_request_document,
)
from veritrail_review._execution_cell_binding import closed_test_binding  # noqa: E402
from veritrail_review.canonical import semantic_digest, sha256_bytes  # noqa: E402
from veritrail_review.contracts import build_source_snapshot_document  # noqa: E402
from veritrail_review.derivation_input_contracts import DerivationInputSet  # noqa: E402


class LanguageSupportPrivateClassifierTests(unittest.TestCase):
    maxDiff = None

    def _inputs(
        self,
        entries: list[tuple[bytes, bytes, str, str]] | None = None,
        *,
        dispositions: dict[bytes, str] | None = None,
        source_classes: dict[bytes, str] | None = None,
        profile_mutation=None,
    ) -> DerivationInputSet:
        selected = entries or [(b"pkg/module.py", b"print('ok')\n", "100644", "REGULAR_BLOB")]
        inventory: list[dict[str, object]] = []
        blobs: dict[str, bytes] = {}
        for path, body, mode, kind in sorted(selected):
            oid = _git_blob_oid(body)
            blobs[oid] = body
            inventory.append(
                {
                    "git_path": {
                        "path_kind": "GIT_PATH",
                        "git_path_hex": path.hex(),
                    },
                    "git_mode": mode,
                    "git_object": {
                        "algorithm": "SHA1",
                        "hex": oid,
                        "object_type": "BLOB",
                    },
                    "entry_kind": kind,
                    "content": {
                        "sha256": sha256_bytes(body),
                        "size_bytes": len(body),
                    },
                }
            )
        snapshot = build_source_snapshot_document(
            repository_id="fixture/language-support",
            commit_oid={"algorithm": "SHA1", "hex": "1" * 40},
            commit_tree_oid={"algorithm": "SHA1", "hex": "2" * 40},
            analysis_tree_oid={"algorithm": "SHA1", "hex": "3" * 40},
            analysis_root={"path_kind": "REPOSITORY_ROOT"},
            inventory=inventory,
        )
        profile = json.loads(
            (FIXTURE_ROOT / "derivation-profile.json").read_text(encoding="utf-8")
        )
        if profile_mutation is not None:
            profile_mutation(profile)
            profile["profile_digest"] = semantic_digest(
                "veritrail.review.derivation-profile/0.1",
                {
                    key: copy.deepcopy(value)
                    for key, value in profile.items()
                    if key != "profile_digest"
                },
            )
        policy = _policy_document(snapshot)
        policy["derivation_profile_digest"] = profile["profile_digest"]
        dispositions = dispositions or {}
        source_classes = source_classes or {}
        for decision in policy["scope_decisions"]:
            path = bytes.fromhex(decision["git_path"]["git_path_hex"])
            disposition = dispositions.get(path, "IN_SCOPE")
            decision["disposition"] = disposition
            decision["reason_code"] = (
                "POLICY_INCLUDED" if disposition == "IN_SCOPE" else "POLICY_EXCLUDED"
            )
            decision["source_class"] = source_classes.get(path, "FIRST_PARTY")
        _seal_policy(policy)
        return DerivationInputSet.create(
            source_snapshot_canonical_bytes=_canonical_artifact(snapshot),
            review_policy_canonical_bytes=_canonical_artifact(policy),
            derivation_profile_canonical_bytes=_canonical_artifact(profile),
            verified_blob_bytes_by_object_identity=blobs,
            source_snapshot_digest=snapshot["source_snapshot_digest"],
            policy_digest=policy["policy_digest"],
            analysis_scope_digest=policy["analysis_scope_digest"],
            slice_policy_digest=policy["slice_policy_digest"],
            derivation_profile_digest=profile["profile_digest"],
        )

    def _classify_one(self, body: bytes, *, path: bytes = b"pkg/module.py"):
        result = language_support.classify_language_support(
            self._inputs([(path, body, "100644", "REGULAR_BLOB")])
        )
        return result, result.subjects_copy()[0]

    def assertClassificationFailure(self, inputs, code) -> None:  # noqa: N802
        with self.assertRaises(language_support._LanguageSupportError) as caught:
            language_support.classify_language_support(inputs)
        self.assertIs(caught.exception.code, code)

    def test_lsi2_000_direct_constructed_digest_mismatch_is_rejected(self) -> None:
        inputs = self._inputs()
        forged = DerivationInputSet.create(
            source_snapshot_canonical_bytes=inputs.source_snapshot_canonical_bytes,
            review_policy_canonical_bytes=inputs.review_policy_canonical_bytes,
            derivation_profile_canonical_bytes=inputs.derivation_profile_canonical_bytes,
            verified_blob_bytes_by_object_identity=inputs.verified_blob_bytes_by_object_identity,
            source_snapshot_digest="0" * 64,
            policy_digest=inputs.policy_digest,
            analysis_scope_digest=inputs.analysis_scope_digest,
            slice_policy_digest=inputs.slice_policy_digest,
            derivation_profile_digest=inputs.derivation_profile_digest,
        )
        self.assertClassificationFailure(
            forged,
            language_support._LanguageSupportFailureCode.INPUT_REVALIDATION_REJECTED,
        )

    def test_lsi2_001_subject_identity_binds_blob_and_policy_semantics(self) -> None:
        first, first_subject = self._classify_one(b"print('one')\n")
        second, second_subject = self._classify_one(b"print('two')\n")
        third = language_support.classify_language_support(
            self._inputs(source_classes={b"pkg/module.py": "GENERATED"})
        )
        self.assertNotEqual(
            first_subject["subject_identity"], second_subject["subject_identity"]
        )
        self.assertNotEqual(first.classification_digest, second.classification_digest)
        self.assertNotEqual(first.classification_digest, third.classification_digest)

    def test_lsi2_002_profile_drift_rejects_the_whole_qualification(self) -> None:
        inputs = self._inputs(
            profile_mutation=lambda profile: profile["accepted_source_encodings"].append(
                "ISO-8859-1"
            )
        )
        self.assertClassificationFailure(
            inputs,
            language_support._LanguageSupportFailureCode.INPUT_REVALIDATION_REJECTED,
        )

    def test_lsc2_001_002_003_closed_resolver_has_no_ambient_authority(self) -> None:
        for token in ("cp65001", "CP65001", "u8", "utf", "utf8", "UTF8", "utf8_ucs2", "utf8_ucs4"):
            with self.subTest(token=token):
                with mock.patch("codecs.lookup", side_effect=AssertionError("ambient lookup")):
                    _, subject = self._classify_one(
                        f"# coding: {token}\nprint('ok')\n".encode("ascii")
                    )
                self.assertEqual(subject["disposition"], "ELIGIBLE")
                self.assertEqual(subject["effective_source_encoding"], "UTF-8")
        for token in ("utf.8", "windows-31j"):
            with self.subTest(token=token):
                _, subject = self._classify_one(
                    f"# coding: {token}\nprint('ok')\n".encode("ascii")
                )
                self.assertEqual(subject["disposition"], "UNSUPPORTED")
                self.assertEqual(
                    subject["reason_codes"], ["UNSUPPORTED_SOURCE_ENCODING"]
                )

    def test_lsc2_004_bom_consistency_uses_get_normal_name(self) -> None:
        for token in ("cp65001", "utf8"):
            with self.subTest(token=token):
                _, subject = self._classify_one(
                    b"\xef\xbb\xbf" + f"# coding: {token}\n".encode("ascii")
                )
                self.assertEqual(subject["disposition"], "UNSUPPORTED")
        _, consistent = self._classify_one(
            b"\xef\xbb\xbf# coding: utf-8-sig\nprint('ok')\n"
        )
        self.assertEqual(consistent["disposition"], "ELIGIBLE")
        self.assertEqual(consistent["effective_source_encoding"], "UTF-8-SIG")

    def test_lsc2_005_nonaccepted_decodable_source_does_not_expand_profile(self) -> None:
        _, subject = self._classify_one(
            b"# coding: latin-1\nname = '\xe9'\n"
        )
        self.assertEqual(subject["disposition"], "UNSUPPORTED")
        self.assertEqual(subject["reason_codes"], ["UNSUPPORTED_SOURCE_ENCODING"])

    def test_lsi2_004_lsc2_006_accepted_cookie_requires_whole_source_decode(self) -> None:
        _, subject = self._classify_one(
            b"# coding: utf-8\nprint('ok')\n\xff"
        )
        self.assertEqual(subject["disposition"], "UNSUPPORTED")
        self.assertEqual(subject["reason_codes"], ["UNSUPPORTED_SOURCE_ENCODING"])

    def test_lsi2_005_complete_reason_set_is_not_first_failure(self) -> None:
        inputs = self._inputs(
            [(b"pkg/module.txt", b"target.py", "120000", "SYMLINK_BLOB")],
            source_classes={b"pkg/module.txt": "UNCLASSIFIED"},
        )
        subject = language_support.classify_language_support(inputs).subjects_copy()[0]
        self.assertEqual(subject["disposition"], "UNSUPPORTED")
        self.assertEqual(
            subject["reason_codes"],
            [
                "UNCLASSIFIED_SOURCE",
                "UNSUPPORTED_ENTRY_KIND",
                "UNSUPPORTED_LANGUAGE",
            ],
        )

        _, independently_applicable = self._classify_one(b"\xff")
        unclassified = language_support.classify_language_support(
            self._inputs(
                [(b"pkg/module.py", b"\xff", "100644", "REGULAR_BLOB")],
                source_classes={b"pkg/module.py": "UNCLASSIFIED"},
            )
        ).subjects_copy()[0]
        self.assertEqual(
            unclassified["reason_codes"],
            ["UNCLASSIFIED_SOURCE", "UNSUPPORTED_SOURCE_ENCODING"],
        )
        self.assertEqual(
            independently_applicable["reason_codes"],
            ["UNSUPPORTED_SOURCE_ENCODING"],
        )

    def test_lsi2_006_inapplicable_encoding_does_not_invent_reason(self) -> None:
        for entry in (
            (b"pkg/module.txt", b"\xff", "100644", "REGULAR_BLOB"),
            (b"pkg/link.py", b"\xff", "120000", "SYMLINK_BLOB"),
        ):
            with self.subTest(path=entry[0]):
                subject = language_support.classify_language_support(
                    self._inputs([entry])
                ).subjects_copy()[0]
                self.assertNotIn("UNSUPPORTED_SOURCE_ENCODING", subject["reason_codes"])

    def test_lsi2_007_empty_denominator_is_only_a_known_empty_classification(self) -> None:
        result = language_support.classify_language_support(
            self._inputs(dispositions={b"pkg/module.py": "OUT_OF_SCOPE"})
        )
        document = result.classification_document_copy()
        self.assertEqual(document["subjects"], [])
        self.assertEqual(result.denominator_count, 0)
        self.assertNotIn("closure_status", document)
        self.assertNotIn("coverage", document)

    def test_lsc_008_exactly_one_closure_is_sorted_and_self_validating(self) -> None:
        inputs = self._inputs(
            [
                (b"pkg/z.py", b"print('z')\n", "100644", "REGULAR_BLOB"),
                (b"pkg/a.py", b"# coding: utf.8\n", "100644", "REGULAR_BLOB"),
            ]
        )
        result = language_support.classify_language_support(inputs)
        paths = [
            item["semantic_input"]["inventory_item"]["git_path"]["git_path_hex"]
            for item in result.subjects_copy()
        ]
        self.assertEqual(paths, [b"pkg/a.py".hex(), b"pkg/z.py".hex()])
        self.assertEqual(
            (result.denominator_count, result.eligible_count, result.unsupported_count),
            (2, 1, 1),
        )

        original = language_support._classify_subject
        duplicate = original(
            item=inputs.source_snapshot_document_copy()["inventory"][0],
            decision=inputs.review_policy_document_copy()["scope_decisions"][0],
            profile=inputs.derivation_profile_document_copy(),
            blobs=inputs.verified_blob_bytes_by_object_identity,
        )
        with mock.patch.object(
            language_support,
            "_classify_subject",
            return_value=duplicate,
        ):
            self.assertClassificationFailure(
                inputs,
                language_support._LanguageSupportFailureCode.CLASSIFICATION_INTEGRITY_REJECTED,
            )

    def test_lsi2_008_same_semantics_do_not_carry_live_authority(self) -> None:
        inputs = self._inputs()
        first = language_support.classify_language_support(inputs)
        second = language_support.classify_language_support(inputs)
        self.assertEqual(first.classification_digest, second.classification_digest)
        self.assertEqual(
            first.classification_document_bytes, second.classification_document_bytes
        )
        forbidden = {"attempt", "budget", "deadline", "continuation", "provider"}
        self.assertTrue(
            forbidden.isdisjoint(
                name.lower() for name in first.__dataclass_fields__  # type: ignore[attr-defined]
            )
        )

    def test_lsi2_009_classifier_does_not_filter_current_execution_request(self) -> None:
        inputs = self._inputs(
            [(b"pkg/module.py", b"# coding: utf.8\n", "100644", "REGULAR_BLOB")]
        )
        result = language_support.classify_language_support(inputs)
        self.assertEqual(result.unsupported_count, 1)
        request = build_request_document(
            inputs=inputs,
            derivation_id="language-support-boundary",
            request_provenance={},
            descriptor=closed_test_binding("stable-a").descriptor,
        )
        self.assertEqual(len(request["source_blobs"]), 1)
        self.assertEqual(
            base64.b64decode(request["source_blobs"][0]["content_base64"]),
            b"# coding: utf.8\n",
        )

    def test_lsi2_010_use_time_seals_reject_input_and_result_mutation(self) -> None:
        inputs = self._inputs()
        object.__setattr__(inputs, "policy_digest", "0" * 64)
        self.assertClassificationFailure(
            inputs,
            language_support._LanguageSupportFailureCode.INPUT_REVALIDATION_REJECTED,
        )

        result = language_support.classify_language_support(self._inputs())
        copied = result.subjects_copy()[0]
        copied["semantic_input"]["scope_semantics"]["source_class"] = "UNCLASSIFIED"
        self.assertEqual(
            result.subjects_copy()[0]["semantic_input"]["scope_semantics"]["source_class"],
            "FIRST_PARTY",
        )
        object.__setattr__(result, "classification_digest", "0" * 64)
        with self.assertRaises(ValueError):
            result.classification_document_copy()

    def test_lsc_007_lsc2_011_invalid_syntax_is_not_a_language_support_reason(self) -> None:
        _, subject = self._classify_one(b"def bad(:\n")
        self.assertEqual(subject["disposition"], "ELIGIBLE")
        self.assertEqual(subject["reason_codes"], [])
        self.assertNotIn("UNSUPPORTED_SYNTAX_VERSION", subject["reason_codes"])

    def test_lsc2_000_function_identity_is_explicitly_0_2(self) -> None:
        result = language_support.classify_language_support(self._inputs())
        document = result.classification_document_copy()
        self.assertEqual(
            document["language_support_function"],
            "r1-python-language-support/0.2",
        )
        self.assertNotIn(b"r1-python-language-support/0.1", result.classification_document_bytes)

    def test_lsc2_008_integrity_failure_cannot_be_rewritten_as_unsupported(self) -> None:
        inputs = self._inputs()
        blobs = dict(inputs.verified_blob_bytes_by_object_identity)
        oid = next(iter(blobs))
        blobs[oid] = b"tampered"
        forged = DerivationInputSet.create(
            source_snapshot_canonical_bytes=inputs.source_snapshot_canonical_bytes,
            review_policy_canonical_bytes=inputs.review_policy_canonical_bytes,
            derivation_profile_canonical_bytes=inputs.derivation_profile_canonical_bytes,
            verified_blob_bytes_by_object_identity=blobs,
            source_snapshot_digest=inputs.source_snapshot_digest,
            policy_digest=inputs.policy_digest,
            analysis_scope_digest=inputs.analysis_scope_digest,
            slice_policy_digest=inputs.slice_policy_digest,
            derivation_profile_digest=inputs.derivation_profile_digest,
        )
        self.assertClassificationFailure(
            forged,
            language_support._LanguageSupportFailureCode.INPUT_REVALIDATION_REJECTED,
        )

    def test_lsc2_007_compatibility_gate_is_closed_even_if_called_directly(self) -> None:
        profile = self._inputs().derivation_profile_document_copy()
        profile["accepted_source_encodings"].append("ISO-8859-1")
        with self.assertRaises(language_support._LanguageSupportError) as caught:
            language_support._require_function_profile_compatibility(profile)
        self.assertIs(
            caught.exception.code,
            language_support._LanguageSupportFailureCode.FUNCTION_PROFILE_INCOMPATIBLE,
        )

    def test_lsi2_011_finite_classifier_has_no_corpus_or_caller_override(self) -> None:
        self.assertEqual(
            tuple(inspect.signature(language_support.classify_language_support).parameters),
            ("inputs",),
        )
        self.assertFalse(hasattr(language_support, "corpus_is_complete"))

    def test_private_boundary_has_no_top_level_export_or_public_artifact(self) -> None:
        import veritrail_review

        self.assertNotIn("classify_language_support", veritrail_review.__all__)
        self.assertNotIn("OwnedLanguageSupportClassification", veritrail_review.__all__)
        result = language_support.classify_language_support(self._inputs())
        self.assertIs(type(result), language_values.OwnedLanguageSupportClassification)
        self.assertNotIn("artifact_kind", result.classification_document_copy())


def _git_blob_oid(body: bytes) -> str:
    header = b"blob " + str(len(body)).encode("ascii") + b"\x00"
    return hashlib.sha1(header + body).hexdigest()


if __name__ == "__main__":
    unittest.main()
