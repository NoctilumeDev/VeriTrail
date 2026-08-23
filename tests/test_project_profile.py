from __future__ import annotations

import copy
import io
import json
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

from veritrail.cli import main
from veritrail.errors import SafetyError, ValidationError
from veritrail.project_profile import (
    NODE_FIELDS,
    PROFILE_FIELDS,
    seal_project_profile,
    validate_project_profile,
    verify_sealed_project_profile,
)

from tests.support import ROOT, bootstrap_profile


class ProjectProfileTests(unittest.TestCase):
    def test_json_schema_and_python_validator_publish_the_same_field_sets(self) -> None:
        schema = json.loads(
            (ROOT / "schemas" / "project-profile-0.1.schema.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual(PROFILE_FIELDS - {"seal"}, set(schema["required"]))
        self.assertEqual(NODE_FIELDS, set(schema["$defs"]["node"]["required"]))

    def test_profile_seal_is_stable_and_detects_mutation(self) -> None:
        first = seal_project_profile(bootstrap_profile())
        second = seal_project_profile(bootstrap_profile())
        self.assertEqual(first["seal"], second["seal"])
        verify_sealed_project_profile(first)

        mutated = copy.deepcopy(first)
        mutated["lifecycle_timeout_ms"] += 1
        with self.assertRaisesRegex(ValidationError, "seal does not match"):
            verify_sealed_project_profile(mutated)

    def test_topology_order_and_reference_boundaries_are_strict(self) -> None:
        cases = {
            "third node": lambda profile: profile["nodes"].append(
                copy.deepcopy(profile["nodes"][0])
            ),
            "duplicate role": lambda profile: profile["nodes"][1].update(
                role="DEPENDENCY"
            ),
            "wrong dependency": lambda profile: profile["nodes"][1].update(
                depends_on=[]
            ),
            "wrong start": lambda profile: profile.update(
                start_order=["application", "dependency"]
            ),
            "wrong teardown": lambda profile: profile.update(
                teardown_order=["dependency", "application"]
            ),
            "same port": lambda profile: profile["nodes"][1].update(port=18771),
            "forward reference": lambda profile: profile["nodes"][0]["arguments"].append(
                {"node_origin": "application"}
            ),
            "overlapping roots": lambda profile: profile.update(
                subject_watch_roots=["src", "src/veritrail"]
            ),
        }
        for label, mutate in cases.items():
            with self.subTest(case=label):
                profile = bootstrap_profile()
                mutate(profile)
                with self.assertRaises(ValidationError):
                    validate_project_profile(profile)

    def test_unknown_shell_secret_and_unsafe_path_are_rejected(self) -> None:
        cases = {
            "unknown": lambda profile: profile.update(surprise=True),
            "inline": lambda profile: profile["nodes"][0]["arguments"].append(
                {"literal": "-c"}
            ),
            "personal path": lambda profile: profile["nodes"][0]["arguments"].append(
                {"literal": "C:\\Users\\example\\project"}
            ),
            "unsafe workdir": lambda profile: profile["nodes"][0].update(
                working_directory="../outside"
            ),
            "arbitrary env": lambda profile: profile["nodes"][0]["environment"].update(
                set={"PYTHONPATH": "plugins"}
            ),
            "query readiness": lambda profile: profile["nodes"][0]["readiness"].update(
                path="/health?secret=value"
            ),
            "missing memory bound": lambda profile: profile["nodes"][0]["limits"].pop(
                "max_job_memory_mb"
            ),
            "oversized memory bound": lambda profile: profile["nodes"][0]["limits"].update(
                max_job_memory_mb=4096
            ),
        }
        for label, mutate in cases.items():
            with self.subTest(case=label):
                profile = bootstrap_profile()
                mutate(profile)
                with self.assertRaises(ValidationError):
                    validate_project_profile(profile)

    def test_profile_rejects_attached_inline_programs(self) -> None:
        for binding, literal in (
            ("python-dependency", "-cprint('bypass')"),
            ("python-dependency", "-icprint('cluster bypass')"),
            ("python-dependency", "-qcprint('cluster bypass')"),
            ("node-dependency", "-econsole.log('bypass')"),
            ("node-dependency", "--eval=1+1"),
            ("node-dependency", "--loader"),
            ("node-dependency", "--experimental-loader"),
        ):
            with self.subTest(binding=binding, literal=literal):
                profile = bootstrap_profile()
                profile["nodes"][0]["tool_binding"] = binding
                profile["nodes"][0]["arguments"].append({"literal": literal})
                with self.assertRaisesRegex(ValidationError, "forbidden inline"):
                    validate_project_profile(profile)

    def test_profile_seal_cli_writes_canonical_new_file_and_refuses_overwrite(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            draft = root / "profile.json"
            output = root / "sealed-profile.json"
            draft.write_text(json.dumps(bootstrap_profile()), encoding="utf-8")
            stdout = io.StringIO()
            stderr = io.StringIO()
            with redirect_stdout(stdout), redirect_stderr(stderr):
                code = main(
                    [
                        "bootstrap-profile-seal",
                        "--profile",
                        str(draft),
                        "--output",
                        str(output),
                    ]
                )
            self.assertEqual(0, code)
            self.assertEqual("", stderr.getvalue())
            sealed = json.loads(output.read_text(encoding="utf-8"))
            verify_sealed_project_profile(sealed)
            self.assertEqual("bootstrap-profile-seal", json.loads(stdout.getvalue())["command"])
            with self.assertRaises(SafetyError):
                from veritrail.project_profile import write_sealed_project_profile

                write_sealed_project_profile(output, sealed)


if __name__ == "__main__":
    unittest.main()
