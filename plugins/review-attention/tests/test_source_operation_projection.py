from __future__ import annotations

import copy
import inspect
import sys
import unittest
from pathlib import Path


PLUGIN_ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = PLUGIN_ROOT / "src"
TEST_ROOT = PLUGIN_ROOT / "tests"
for location in (SOURCE_ROOT, TEST_ROOT):
    if str(location) not in sys.path:
        sys.path.insert(0, str(location))

import test_language_support as language_support_tests  # noqa: E402
from test_execution_cell import _canonical_artifact, _seal_policy  # noqa: E402
from veritrail_review import _language_support as language_support  # noqa: E402
from veritrail_review import _source_operation_projection as projection  # noqa: E402
from veritrail_review import (  # noqa: E402
    _source_operation_projection_values as projection_values,
)
from veritrail_review._execution_cell_binding import (  # noqa: E402
    ProviderDescriptor,
    closed_test_binding,
)
from veritrail_review._relation_observation_binding import (  # noqa: E402
    closed_test_relation_observation_bindings,
)
from veritrail_review._relation_observation_domain import (  # noqa: E402
    build_declared_relation_observation_domain,
)
from veritrail_review.canonical import semantic_digest  # noqa: E402
from veritrail_review.derivation_input_contracts import DerivationInputSet  # noqa: E402


class SourceOperationProjectionStageATests(unittest.TestCase):
    maxDiff = None

    def setUp(self) -> None:
        helper = language_support_tests.LanguageSupportPrivateClassifierTests()
        self.inputs = helper._inputs(
            [
                (b"pkg/a.py", b"print('a')\n", "100644", "REGULAR_BLOB"),
                (b"pkg/b.py", b"print('b')\n", "100644", "REGULAR_BLOB"),
                (
                    b"pkg/c.py",
                    b"# coding: utf.8\n",
                    "100644",
                    "REGULAR_BLOB",
                ),
                (b"pkg/out.py", b"print('out')\n", "100644", "REGULAR_BLOB"),
            ],
            dispositions={b"pkg/out.py": "OUT_OF_SCOPE"},
        )
        self.classification = language_support.classify_language_support(self.inputs)
        self.fact_descriptor = closed_test_binding("stable-a").descriptor
        self.other_fact_descriptor = closed_test_binding("stable-b").descriptor
        self.observer_a = _descriptor("observer-a")
        self.observer_b = _descriptor("observer-b")

    def test_a_001_fact_projection_is_exact_eligible_upper_bound(self) -> None:
        value = projection.build_fact_derivation_source_operation_projection(
            self.classification, self.fact_descriptor
        )
        document = value.projection_document_copy()
        eligible = self._eligible_by_path()
        self.assertEqual(
            document["eligible_subject_ids"],
            [eligible[b"pkg/a.py"], eligible[b"pkg/b.py"]],
        )
        self.assertEqual(
            document["operation_subject_ids"], document["eligible_subject_ids"]
        )
        self.assertEqual(
            document["operation_coordinate"],
            {
                "operation_kind": "FACT_DERIVATION",
                "provider_descriptor": self.fact_descriptor.document(),
                "fact_set_digest": None,
                "observation_domain_digest": None,
                "assigned_observation_item_ids": [],
            },
        )
        self.assertNotIn("source_blobs", document)
        self.assertNotIn("artifact_kind", document)

    def test_a_002_provider_identity_changes_projection_identity(self) -> None:
        first = projection.build_fact_derivation_source_operation_projection(
            self.classification, self.fact_descriptor
        )
        second = projection.build_fact_derivation_source_operation_projection(
            self.classification, self.other_fact_descriptor
        )
        self.assertEqual(first.operation_subject_ids, second.operation_subject_ids)
        self.assertNotEqual(
            first.source_operation_projection_digest,
            second.source_operation_projection_digest,
        )
        self.assertNotEqual(
            first.projection_document_bytes, second.projection_document_bytes
        )

    def test_a_003_relation_derivation_uses_only_fact_referenced_paths(self) -> None:
        fact_set = self._fact_set([self._module_fact(b"pkg/b.py")])
        value = projection.build_relation_derivation_source_operation_projection(
            self.classification, self.fact_descriptor, fact_set
        )
        eligible = self._eligible_by_path()
        self.assertEqual(value.eligible_subject_ids, tuple(eligible.values()))
        self.assertEqual(value.operation_subject_ids, (eligible[b"pkg/b.py"],))
        coordinate = value.projection_document_copy()["operation_coordinate"]
        self.assertEqual(coordinate["fact_set_digest"], fact_set["fact_set_digest"])
        self.assertIsNone(coordinate["observation_domain_digest"])
        self.assertEqual(coordinate["assigned_observation_item_ids"], [])

        both = self._fact_set(
            [self._module_fact(b"pkg/b.py"), self._module_fact(b"pkg/a.py")]
        )
        ordered = projection.build_relation_derivation_source_operation_projection(
            self.classification, self.fact_descriptor, both
        )
        self.assertEqual(
            ordered.operation_subject_ids,
            (eligible[b"pkg/a.py"], eligible[b"pkg/b.py"]),
        )

        same_path_larger_world = self._fact_set(
            [
                self._module_fact(b"pkg/b.py"),
                self._import_fact(b"pkg/b.py"),
            ]
        )
        rebound = projection.build_relation_derivation_source_operation_projection(
            self.classification,
            self.fact_descriptor,
            same_path_larger_world,
        )
        self.assertEqual(rebound.operation_subject_ids, value.operation_subject_ids)
        self.assertNotEqual(
            rebound.source_operation_projection_digest,
            value.source_operation_projection_digest,
        )

    def test_a_004_relation_fact_set_cannot_reference_unsupported_or_foreign_path(
        self,
    ) -> None:
        for path in (b"pkg/c.py", b"pkg/foreign.py"):
            with self.subTest(path=path):
                fact_set = self._fact_set(
                    [self._module_fact(path, validate_path=False)]
                )
                with self.assertRaisesRegex(ValueError, "invalid exact FactSet"):
                    projection.build_relation_derivation_source_operation_projection(
                        self.classification, self.fact_descriptor, fact_set
                    )

    def test_a_005_relation_fact_set_dangling_and_digest_tamper_fail_closed(
        self,
    ) -> None:
        valid = self._fact_set([self._module_fact(b"pkg/a.py")])
        for mutate in (
            lambda item: item.__setitem__("fact_set_digest", "0" * 64),
            lambda item: item.__setitem__("source_snapshot_digest", "0" * 64),
            lambda item: item["facts"][0]["source_anchor"]["git_path"].__setitem__(
                "git_path_hex", b"pkg/b.py".hex()
            ),
        ):
            with self.subTest(mutate=mutate):
                changed = copy.deepcopy(valid)
                mutate(changed)
                with self.assertRaisesRegex(ValueError, "invalid exact FactSet"):
                    projection.build_relation_derivation_source_operation_projection(
                        self.classification, self.fact_descriptor, changed
                    )

    def test_a_006_observation_projection_uses_only_exact_provider_assignment(
        self,
    ) -> None:
        facts = [self._module_fact(b"pkg/a.py"), self._module_fact(b"pkg/b.py")]
        fact_set = self._fact_set(facts)
        domain, assigned = self._observation_domain(
            fact_set,
            {
                self.observer_a: [facts[1]["fact_id"]],
                self.observer_b: [facts[0]["fact_id"]],
            },
        )
        first = projection.build_relation_observation_source_operation_projection(
            self.classification, self.observer_a, fact_set, domain
        )
        second = projection.build_relation_observation_source_operation_projection(
            self.classification, self.observer_b, fact_set, domain
        )
        eligible = self._eligible_by_path()
        self.assertEqual(first.operation_subject_ids, (eligible[b"pkg/b.py"],))
        self.assertEqual(second.operation_subject_ids, (eligible[b"pkg/a.py"],))
        self.assertEqual(
            first.assigned_observation_item_ids,
            tuple(assigned[self.observer_a.provider_id]),
        )
        self.assertEqual(
            second.assigned_observation_item_ids,
            tuple(assigned[self.observer_b.provider_id]),
        )
        self.assertNotEqual(
            first.source_operation_projection_digest,
            second.source_operation_projection_digest,
        )

    def test_a_007_observation_domain_and_assignment_tamper_fail_closed(self) -> None:
        fact = self._module_fact(b"pkg/a.py")
        fact_set = self._fact_set([fact])
        domain, _ = self._observation_domain(
            fact_set, {self.observer_a: [fact["fact_id"]]}
        )
        variants = []
        bad_digest = copy.deepcopy(domain)
        bad_digest["observation_domain_digest"] = "0" * 64
        variants.append(bad_digest)
        dangling = copy.deepcopy(domain)
        dangling["provider_responsibilities"][0][
            "assigned_observation_item_ids"
        ] = ["0" * 64]
        dangling = self._reseal_domain(dangling)
        variants.append(dangling)
        foreign_fact = copy.deepcopy(domain)
        foreign_fact["observation_items"][0]["subject_fact_id"] = "0" * 64
        foreign_fact["observation_items"][0] = self._reseal_item(
            foreign_fact["observation_items"][0]
        )
        foreign_fact = self._reseal_domain(foreign_fact)
        variants.append(foreign_fact)
        for changed in variants:
            with self.subTest(domain=changed):
                with self.assertRaisesRegex(ValueError, "invalid exact observation"):
                    projection.build_relation_observation_source_operation_projection(
                        self.classification, self.observer_a, fact_set, changed
                    )

    def test_a_008_multiple_items_for_one_fact_remain_one_operation_source(
        self,
    ) -> None:
        fact = self._module_fact(b"pkg/a.py")
        fact_set = self._fact_set([fact])
        domain, _ = self._observation_domain(
            fact_set, {self.observer_a: [fact["fact_id"]]}
        )
        single = projection.build_relation_observation_source_operation_projection(
            self.classification, self.observer_a, fact_set, domain
        )
        second = self._reseal_item(
            {
                "source_snapshot_digest": self.classification.source_snapshot_digest,
                "derivation_profile_digest": (
                    self.classification.derivation_profile_digest
                ),
                "fact_set_digest": fact_set["fact_set_digest"],
                "relation_kind": "IMPORT_TARGET_LITERAL",
                "subject_role": "SOURCE_FACT",
                "subject_fact_id": fact["fact_id"],
            }
        )
        domain["observation_items"].append(second)
        assigned = domain["provider_responsibilities"][0][
            "assigned_observation_item_ids"
        ]
        assigned.append(second["observation_item_id"])
        assigned.sort()
        domain = self._reseal_domain(domain)
        value = projection.build_relation_observation_source_operation_projection(
            self.classification, self.observer_a, fact_set, domain
        )
        self.assertEqual(len(value.assigned_observation_item_ids), 2)
        self.assertEqual(
            value.operation_subject_ids,
            (self._eligible_by_path()[b"pkg/a.py"],),
        )
        self.assertEqual(value.operation_subject_ids, single.operation_subject_ids)
        self.assertNotEqual(
            value.source_operation_projection_digest,
            single.source_operation_projection_digest,
        )

    def test_a_009_existing_closed_observation_domain_is_consumed_exactly(
        self,
    ) -> None:
        policy = self.inputs.review_policy_document_copy()
        policy["provider_requirements"].append(
            {
                "capability_id": "review-relation-derivation",
                "required": True,
                "composition_mode": "CUMULATIVE",
            }
        )
        _seal_policy(policy)
        inputs = DerivationInputSet.create(
            source_snapshot_canonical_bytes=(
                self.inputs.source_snapshot_canonical_bytes
            ),
            review_policy_canonical_bytes=_canonical_artifact(policy),
            derivation_profile_canonical_bytes=(
                self.inputs.derivation_profile_canonical_bytes
            ),
            verified_blob_bytes_by_object_identity=(
                self.inputs.verified_blob_bytes_by_object_identity
            ),
            source_snapshot_digest=self.inputs.source_snapshot_digest,
            policy_digest=policy["policy_digest"],
            analysis_scope_digest=policy["analysis_scope_digest"],
            slice_policy_digest=policy["slice_policy_digest"],
            derivation_profile_digest=self.inputs.derivation_profile_digest,
        )
        classification = language_support.classify_language_support(inputs)
        module = self._module_fact(b"pkg/a.py", classification=classification)
        imported = self._import_fact(
            b"pkg/a.py", classification=classification
        )
        fact_set = self._fact_set(
            [module, imported], classification=classification
        )
        bindings = closed_test_relation_observation_bindings()
        domain = build_declared_relation_observation_domain(
            inputs, fact_set, bindings
        )
        value = projection.build_relation_observation_source_operation_projection(
            classification, bindings[1].descriptor, fact_set, domain
        )
        responsibility = next(
            item
            for item in domain["provider_responsibilities"]
            if item["provider_descriptor"] == bindings[1].descriptor.document()
        )
        self.assertEqual(
            value.assigned_observation_item_ids,
            tuple(responsibility["assigned_observation_item_ids"]),
        )
        self.assertEqual(len(value.assigned_observation_item_ids), 2)
        self.assertEqual(
            value.operation_subject_ids,
            (self._eligible_by_path(classification)[b"pkg/a.py"],),
        )

    def test_a_010_empty_worlds_remain_distinct(self) -> None:
        helper = language_support_tests.LanguageSupportPrivateClassifierTests()
        denominator_empty = language_support.classify_language_support(
            helper._inputs(dispositions={b"pkg/module.py": "OUT_OF_SCOPE"})
        )
        all_unsupported = language_support.classify_language_support(
            helper._inputs(
                [
                    (
                        b"pkg/module.py",
                        b"# coding: utf.8\n",
                        "100644",
                        "REGULAR_BLOB",
                    )
                ]
            )
        )
        empty_a = projection.build_fact_derivation_source_operation_projection(
            denominator_empty, self.fact_descriptor
        )
        empty_b = projection.build_fact_derivation_source_operation_projection(
            all_unsupported, self.fact_descriptor
        )
        later_empty = projection.build_relation_derivation_source_operation_projection(
            self.classification, self.fact_descriptor, self._fact_set([])
        )
        self.assertEqual(empty_a.operation_subject_ids, ())
        self.assertEqual(empty_b.operation_subject_ids, ())
        self.assertEqual(later_empty.operation_subject_ids, ())
        self.assertEqual(
            later_empty.eligible_subject_ids,
            tuple(self._eligible_by_path().values()),
        )
        self.assertEqual(
            len(
                {
                    empty_a.source_operation_projection_digest,
                    empty_b.source_operation_projection_digest,
                    later_empty.source_operation_projection_digest,
                }
            ),
            3,
        )

    def test_a_011_projection_is_deterministic_and_has_no_caller_path_parameter(
        self,
    ) -> None:
        fact_set = self._fact_set([self._module_fact(b"pkg/b.py")])
        first = projection.build_relation_derivation_source_operation_projection(
            self.classification, self.fact_descriptor, fact_set
        )
        second = projection.build_relation_derivation_source_operation_projection(
            self.classification, self.fact_descriptor, copy.deepcopy(fact_set)
        )
        self.assertEqual(
            first.projection_document_bytes, second.projection_document_bytes
        )
        self.assertEqual(
            tuple(
                inspect.signature(
                    projection.build_relation_derivation_source_operation_projection
                ).parameters
            ),
            ("classification", "descriptor", "fact_set_document"),
        )

    def test_a_012_copy_and_use_time_seals_reject_mutation(self) -> None:
        value = projection.build_fact_derivation_source_operation_projection(
            self.classification, self.fact_descriptor
        )
        copied = value.projection_document_copy()
        copied["eligible_subject_ids"].clear()
        self.assertNotEqual(copied, value.projection_document_copy())
        object.__setattr__(value, "classification_digest", "0" * 64)
        with self.assertRaises(ValueError):
            value.projection_document_copy()

    def test_a_013_direct_construction_and_authority_fields_are_absent(self) -> None:
        value = projection.build_fact_derivation_source_operation_projection(
            self.classification, self.fact_descriptor
        )
        forbidden = {
            "attempt",
            "budget",
            "deadline",
            "continuation",
            "eligibility",
            "claim",
            "artifact",
            "evidence",
            "coverage",
        }
        self.assertTrue(
            forbidden.isdisjoint(
                name.lower()
                for name in value.__dataclass_fields__  # type: ignore[attr-defined]
            )
        )
        forged = projection_values.OwnedSourceOperationProjection(
            source_snapshot_digest=value.source_snapshot_digest,
            policy_digest=value.policy_digest,
            analysis_scope_digest=value.analysis_scope_digest,
            derivation_profile_digest=value.derivation_profile_digest,
            language_support_function=value.language_support_function,
            classification_digest=value.classification_digest,
            operation_kind=value.operation_kind,
            provider_descriptor_bytes=value.provider_descriptor_bytes,
            fact_set_digest=value.fact_set_digest,
            observation_domain_digest=value.observation_domain_digest,
            assigned_observation_item_ids=value.assigned_observation_item_ids,
            eligible_subject_ids=value.eligible_subject_ids,
            operation_subject_ids=value.operation_subject_ids,
            source_operation_projection_digest=(
                value.source_operation_projection_digest
            ),
            projection_document_bytes=value.projection_document_bytes,
            _state_seal=value._state_seal,
            _construction_token=object(),
        )
        with self.assertRaises(ValueError):
            forged.projection_document_copy()

    def test_a_014_private_boundary_has_no_top_level_export(self) -> None:
        import veritrail_review

        self.assertNotIn(
            "OwnedSourceOperationProjection", veritrail_review.__all__
        )
        self.assertNotIn(
            "build_fact_derivation_source_operation_projection",
            veritrail_review.__all__,
        )

    def _eligible_by_path(
        self,
        classification=None,
    ) -> dict[bytes, str]:
        classification = classification or self.classification
        result: dict[bytes, str] = {}
        for subject in classification.subjects_copy():
            if subject["disposition"] != "ELIGIBLE":
                continue
            path_hex = subject["semantic_input"]["inventory_item"]["git_path"][
                "git_path_hex"
            ]
            result[bytes.fromhex(path_hex)] = subject["subject_identity"]
        return result

    def _subject(self, path: bytes, *, classification=None) -> dict[str, object]:
        classification = classification or self.classification
        for subject in classification.subjects_copy():
            path_hex = subject["semantic_input"]["inventory_item"]["git_path"][
                "git_path_hex"
            ]
            if bytes.fromhex(path_hex) == path:
                return subject
        raise KeyError(path)

    def _module_fact(
        self,
        path: bytes,
        *,
        validate_path: bool = True,
        classification=None,
    ) -> dict[str, object]:
        classification = classification or self.classification
        if validate_path:
            subject = self._subject(path, classification=classification)
            inventory = subject["semantic_input"]["inventory_item"]
            size = inventory["content"]["size_bytes"]
        else:
            size = 1
        anchor = {
            "git_path": {"path_kind": "GIT_PATH", "git_path_hex": path.hex()},
            "start_byte": 0,
            "end_byte": size,
        }
        subject_digest = semantic_digest(
            "veritrail.review.fact-subject/0.1",
            {
                "source_snapshot_digest": classification.source_snapshot_digest,
                "derivation_profile_digest": (
                    classification.derivation_profile_digest
                ),
                "source_anchor": anchor,
                "subject_space": "MODULE_ENTITY",
                "local_ordinal": 0,
            },
        )
        attributes = {"module_key_parts": None}
        fact_id = semantic_digest(
            "veritrail.review.code-fact/0.1",
            {
                "subject_key_digest": subject_digest,
                "fact_kind": "MODULE",
                "semantic_attributes": attributes,
            },
        )
        return {
            "fact_id": fact_id,
            "subject_key_digest": subject_digest,
            "subject_space": "MODULE_ENTITY",
            "fact_kind": "MODULE",
            "source_snapshot_digest": classification.source_snapshot_digest,
            "derivation_profile_digest": (
                classification.derivation_profile_digest
            ),
            "source_anchor": anchor,
            "local_ordinal": 0,
            "semantic_attributes": attributes,
            "provenance_refs": ["fixture-provider-run"],
        }

    def _import_fact(self, path: bytes, *, classification=None) -> dict[str, object]:
        classification = classification or self.classification
        subject = self._subject(path, classification=classification)
        inventory = subject["semantic_input"]["inventory_item"]
        size = inventory["content"]["size_bytes"]
        anchor = {
            "git_path": {"path_kind": "GIT_PATH", "git_path_hex": path.hex()},
            "start_byte": 0,
            "end_byte": min(size, 1),
        }
        subject_digest = semantic_digest(
            "veritrail.review.fact-subject/0.1",
            {
                "source_snapshot_digest": classification.source_snapshot_digest,
                "derivation_profile_digest": classification.derivation_profile_digest,
                "source_anchor": anchor,
                "subject_space": "IMPORT_ALIAS",
                "local_ordinal": 0,
            },
        )
        attributes = {
            "import_form": "IMPORT",
            "relative_level": 0,
            "module_parts": ["fixture"],
            "imported_name": None,
            "alias_name": None,
        }
        fact_id = semantic_digest(
            "veritrail.review.code-fact/0.1",
            {
                "subject_key_digest": subject_digest,
                "fact_kind": "IMPORT_DECLARATION",
                "semantic_attributes": attributes,
            },
        )
        return {
            "fact_id": fact_id,
            "subject_key_digest": subject_digest,
            "subject_space": "IMPORT_ALIAS",
            "fact_kind": "IMPORT_DECLARATION",
            "source_snapshot_digest": classification.source_snapshot_digest,
            "derivation_profile_digest": classification.derivation_profile_digest,
            "source_anchor": anchor,
            "local_ordinal": 0,
            "semantic_attributes": attributes,
            "provenance_refs": ["fixture-provider-run"],
        }

    def _fact_set(
        self,
        facts: list[dict[str, object]],
        *,
        classification=None,
    ) -> dict[str, object]:
        classification = classification or self.classification
        ordered = sorted(copy.deepcopy(facts), key=lambda item: item["fact_id"])
        semantic_facts = [
            {
                key: copy.deepcopy(value)
                for key, value in fact.items()
                if key != "provenance_refs"
            }
            for fact in ordered
        ]
        digest = semantic_digest(
            "veritrail.review.fact-set/0.1",
            {
                "source_snapshot_digest": classification.source_snapshot_digest,
                "analysis_scope_digest": classification.analysis_scope_digest,
                "derivation_profile_digest": (
                    classification.derivation_profile_digest
                ),
                "facts": semantic_facts,
                "conflicts": [],
            },
        )
        return {
            "artifact_kind": "FACT_SET",
            "schema_version": "0.1",
            "canonicalization_profile": "veritrail-json-c14n/1",
            "source_snapshot_digest": classification.source_snapshot_digest,
            "policy_digest": classification.policy_digest,
            "analysis_scope_digest": classification.analysis_scope_digest,
            "derivation_profile_digest": classification.derivation_profile_digest,
            "facts": ordered,
            "conflicts": [],
            "fact_set_digest": digest,
        }

    def _observation_domain(
        self,
        fact_set: dict[str, object],
        assignments: dict[ProviderDescriptor, list[str]],
    ) -> tuple[dict[str, object], dict[str, list[str]]]:
        facts = {fact["fact_id"]: fact for fact in fact_set["facts"]}
        items = []
        item_ids_by_provider: dict[str, list[str]] = {}
        responsibilities = []
        for descriptor, fact_ids in assignments.items():
            assigned_ids = []
            for fact_id in fact_ids:
                self.assertIn(fact_id, facts)
                item = self._reseal_item(
                    {
                        "source_snapshot_digest": (
                            self.classification.source_snapshot_digest
                        ),
                        "derivation_profile_digest": (
                            self.classification.derivation_profile_digest
                        ),
                        "fact_set_digest": fact_set["fact_set_digest"],
                        "relation_kind": "LEXICAL_CONTAINS",
                        "subject_role": "TARGET_FACT",
                        "subject_fact_id": fact_id,
                    }
                )
                items.append(item)
                assigned_ids.append(item["observation_item_id"])
            assigned_ids.sort()
            item_ids_by_provider[descriptor.provider_id] = assigned_ids
            responsibilities.append(
                {
                    "provider_descriptor": descriptor.document(),
                    "required": True,
                    "assigned_observation_item_ids": assigned_ids,
                }
            )
        items.sort(key=lambda item: item["observation_item_id"])
        responsibilities.sort(
            key=lambda item: tuple(item["provider_descriptor"].values())
        )
        domain = {
            "source_snapshot_digest": self.classification.source_snapshot_digest,
            "policy_digest": self.classification.policy_digest,
            "analysis_scope_digest": self.classification.analysis_scope_digest,
            "derivation_profile_digest": self.classification.derivation_profile_digest,
            "fact_set_digest": fact_set["fact_set_digest"],
            "observation_profile_id": "fixture-observation-profile",
            "observation_profile_version": "0.1-test",
            "observation_profile_digest": semantic_digest(
                "fixture.observation-profile/0.1", {}
            ),
            "capability_id": "fixture-relation-observation",
            "required": True,
            "composition_mode": "CUMULATIVE",
            "observation_items": items,
            "provider_responsibilities": responsibilities,
        }
        return self._reseal_domain(domain), item_ids_by_provider

    @staticmethod
    def _reseal_item(item: dict[str, object]) -> dict[str, object]:
        unsigned = {
            key: copy.deepcopy(value)
            for key, value in item.items()
            if key != "observation_item_id"
        }
        return {
            "observation_item_id": semantic_digest(
                "veritrail.review.relation-observation-item/0.1", unsigned
            ),
            **unsigned,
        }

    @staticmethod
    def _reseal_domain(domain: dict[str, object]) -> dict[str, object]:
        owned = copy.deepcopy(domain)
        owned.pop("observation_domain_digest", None)
        payload = {
            key: copy.deepcopy(value)
            for key, value in owned.items()
            if key != "policy_digest"
        }
        owned["observation_domain_digest"] = semantic_digest(
            "veritrail.review.relation-observation-domain/0.1", payload
        )
        return owned


def _descriptor(provider_id: str) -> ProviderDescriptor:
    return ProviderDescriptor(
        capability_id="fixture-relation-observation",
        provider_id=provider_id,
        provider_version="0.1-test",
        parser_id="fixture-parser",
        parser_version="0.1-test",
        runtime_id="fixture-runtime",
        runtime_version="0.1-test",
    )


if __name__ == "__main__":
    unittest.main()
