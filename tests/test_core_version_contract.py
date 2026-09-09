from __future__ import annotations

import re
import unittest
from pathlib import Path

from veritrail import __version__


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
PYPROJECT = REPOSITORY_ROOT / "pyproject.toml"
FROZEN_CORE_BASELINE = "0.12.0"
PREVIOUS_MAINTENANCE_CORE_VERSION = "0.12.1"
STABLE_CORE_VERSION = "0.12.2"
CURRENT_SOURCE_VERSION = "0.13.0"
CURRENT_STATUS_FILES = (
    REPOSITORY_ROOT / "AGENTS.md",
    REPOSITORY_ROOT / "CONTRIBUTING.md",
    REPOSITORY_ROOT / "SECURITY.md",
)
CURRENT_MAINTENANCE_CONTRACT = (
    REPOSITORY_ROOT / "docs" / "74-core-demo-catalog-binding-maintenance-contract.md"
)
CURRENT_RELEASE_NOTES = REPOSITORY_ROOT / "docs" / "75-v0.12.2-release-notes.md"
CURRENT_RELEASE_READBACK = (
    REPOSITORY_ROOT / "docs" / "76-core-v0.12.2-release-readback-facts.md"
)
README = REPOSITORY_ROOT / "README.md"
START_HERE = REPOSITORY_ROOT / "START_HERE.md"
MILESTONES = REPOSITORY_ROOT / "docs" / "milestones.md"
BUG_TEMPLATE = REPOSITORY_ROOT / ".github" / "ISSUE_TEMPLATE" / "bug_report.yml"
BOUNDED_PROPOSAL_TEMPLATE = (
    REPOSITORY_ROOT / ".github" / "ISSUE_TEMPLATE" / "bounded_proposal.yml"
)
STARTER_README = REPOSITORY_ROOT / "starter" / "README.md"
M14_FACTS = REPOSITORY_ROOT / "docs" / "56-m14-final-validation-and-release-facts.md"
CORE_0_12_0_RELEASE_NOTES = REPOSITORY_ROOT / "docs" / "57-v0.12.0-release-notes.md"
CORE_0_12_1_CONTRACT = REPOSITORY_ROOT / "docs" / "71-core-first-run-maintenance-contract.md"
CORE_0_12_1_RELEASE_NOTES = REPOSITORY_ROOT / "docs" / "72-v0.12.1-release-notes.md"
CORE_0_12_1_READBACK = REPOSITORY_ROOT / "docs" / "73-core-v0.12.1-release-readback-facts.md"
CORE_0_13_0_CONTRACT = (
    REPOSITORY_ROOT / "docs" / "100-core-v0.13.0-acceptance-api-release-contract.md"
)
CORE_0_13_0_CANDIDATE_PLAN = (
    REPOSITORY_ROOT / "docs" / "102-core-v0.13.0-release-candidate-plan.md"
)
CORE_0_13_0_RELEASE_NOTES = REPOSITORY_ROOT / "docs" / "103-v0.13.0-release-notes.md"
STARTER_PYPROJECT = REPOSITORY_ROOT / "starter" / "pyproject.toml"
GITHUB_PLUGIN_PYPROJECT = REPOSITORY_ROOT / "plugins" / "github-evidence" / "pyproject.toml"
PUBLIC_CI = REPOSITORY_ROOT / ".github" / "workflows" / "ci.yml"


class CoreVersionContractTests(unittest.TestCase):
    def test_source_uses_the_unreleased_0_13_0_candidate_coordinate(self) -> None:
        pyproject = PYPROJECT.read_text(encoding="utf-8")
        match = re.search(
            r'(?ms)^\[project\]\s*.*?^version = "([^"]+)"$',
            pyproject,
        )
        self.assertIsNotNone(match, "[project].version is missing from pyproject.toml")
        project_version = match.group(1)

        self.assertEqual(project_version, CURRENT_SOURCE_VERSION)
        self.assertEqual(__version__, CURRENT_SOURCE_VERSION)
        self.assertNotEqual(project_version, STABLE_CORE_VERSION)
        self.assertNotEqual(project_version, FROZEN_CORE_BASELINE)
        self.assertNotEqual(project_version, PREVIOUS_MAINTENANCE_CORE_VERSION)

        self.assertIn('"Development Status :: 4 - Beta"', pyproject)
        self.assertIn('"Programming Language :: Python :: 3.10"', pyproject)
        self.assertIn('"Programming Language :: Python :: 3.13"', pyproject)
        self.assertNotIn('"Development Status :: 2 - Pre-Alpha"', pyproject)

    def test_current_release_and_historical_coordinates_are_not_conflated(self) -> None:
        agents, contributing, security = (
            path.read_text(encoding="utf-8") for path in CURRENT_STATUS_FILES
        )
        self.assertIn("Core `0.12.2` 现在是仓库 Latest", agents)
        self.assertIn("docs/76-core-v0.12.2-release-readback-facts.md", agents)
        self.assertRegex(
            contributing,
            r"Core `0\.12\.2` is the current released\s+maintenance coordinate",
        )
        self.assertRegex(
            security,
            r"Core 0\.12\.2 is the current released maintenance\s+coordinate",
        )
        self.assertNotRegex(
            agents,
            r"(?s)`0\.12\.1`.{0,250}(?:当前仓库 Latest|当前公开稳定 Core)",
        )
        self.assertNotRegex(
            contributing,
            r"Core `0\.12\.1` is the current released|"
            r"latest publicly released Core coordinate remains `0\.12\.1`",
        )
        self.assertNotRegex(
            security,
            r"Core 0\.12\.1 is the current released maintenance",
        )
        for content in (agents, contributing, security):
            self.assertNotIn("0.12.1.dev0", content)

        self.assertIn("0.13.0 / RELEASE CANDIDATE", agents)
        self.assertIn("unreleased Core `0.13.0`", contributing)
        self.assertIn("unreleased Core 0.13.0 candidate", security)

        contract = CURRENT_MAINTENANCE_CONTRACT.read_text(encoding="utf-8")
        self.assertIn(PREVIOUS_MAINTENANCE_CORE_VERSION, contract)
        self.assertRegex(
            contract,
            r"(?m)^> 状态：`RELEASED / MAINTENANCE FROZEN`$",
        )
        self.assertRegex(
            contract,
            r"(?m)^> 当前稳定 Core：`0\.12\.2` @ 不可移动标签 `v0\.12\.2`$",
        )
        self.assertNotIn("RELEASE CANDIDATE / PENDING PUBLIC READBACK", contract)

        release_notes = CURRENT_RELEASE_NOTES.read_text(encoding="utf-8")
        self.assertIn(PREVIOUS_MAINTENANCE_CORE_VERSION, release_notes)
        self.assertRegex(
            release_notes,
            r"(?m)^> 状态：`RELEASED / MAINTENANCE FROZEN`$",
        )
        self.assertRegex(
            release_notes,
            r"(?m)^> 当前公开稳定 Core：`0\.12\.2`$",
        )
        self.assertNotIn("PENDING PUBLIC READBACK", release_notes)
        self.assertIn("veritrail-0.12.2-py3-none-any.whl", release_notes)

        release_readback = CURRENT_RELEASE_READBACK.read_text(encoding="utf-8")
        self.assertRegex(
            release_readback,
            r"(?m)^- 状态：`RELEASED / MAINTENANCE FROZEN`；$",
        )
        self.assertRegex(release_readback, r"(?m)^- 版本：`0\.12\.2`；$")
        self.assertIn(
            "f961930ae1e69d7d88849fa2b0d40befb3e94c89", release_readback
        )
        self.assertIn(
            "2177bb2cc02d9ef9068e7b7132983c5edb82be6c", release_readback
        )
        self.assertIn("ARTIFACT_ROOT_MISMATCH", release_readback)
        self.assertIn("没有 GitHub-hosted post-release execution log", release_readback)

        readme = README.read_text(encoding="utf-8")
        self.assertIn(
            "[![Core v0.12.2](https://img.shields.io/badge/Core-v0.12.2-0B4B50)]"
            "(https://github.com/NoctilumeDev/VeriTrail/releases/tag/v0.12.2)",
            readme,
        )
        self.assertIn(
            "| 直接使用稳定内核 | [Core 0.12.2]"
            "(https://github.com/NoctilumeDev/VeriTrail/releases/tag/v0.12.2) |",
            readme,
        )
        self.assertIn(
            "[Core 0.12.2 发布与公开读回事实]"
            "(docs/76-core-v0.12.2-release-readback-facts.md)",
            readme,
        )
        self.assertNotIn("[![Core v0.12.1]", readme)
        self.assertNotIn("| 直接使用稳定内核 | [Core 0.12.1]", readme)
        self.assertIn(
            "[0.13.0 Release Notes](docs/103-v0.13.0-release-notes.md)",
            readme,
        )

        start_here = START_HERE.read_text(encoding="utf-8")
        self.assertIn(
            "> 当前稳定内核：[`VeriTrail Core 0.12.2`]"
            "(https://github.com/NoctilumeDev/VeriTrail/releases/tag/v0.12.2)",
            start_here,
        )
        self.assertIn(
            "releases/download/v0.12.2/veritrail-0.12.2-py3-none-any.whl",
            start_here,
        )
        self.assertNotIn(
            "> 当前稳定内核：[`VeriTrail Core 0.12.1`]", start_here
        )
        self.assertNotIn(
            "releases/download/v0.12.1/veritrail-0.12.1-py3-none-any.whl",
            start_here,
        )
        self.assertIn(
            "[0.13.0 Release Notes](docs/103-v0.13.0-release-notes.md)",
            start_here,
        )

        milestones = MILESTONES.read_text(encoding="utf-8")
        self.assertIn(
            "[Core 0.12.2 发布与公开读回事实]"
            "(76-core-v0.12.2-release-readback-facts.md)",
            milestones,
        )
        self.assertRegex(
            milestones,
            r"Core `0\.12\.2` 状态为\s+`RELEASED / MAINTENANCE FROZEN`",
        )
        self.assertNotIn("`0.12.2` 维护发布候选", milestones)
        self.assertIn(
            "[0.13.0 Release Notes](103-v0.13.0-release-notes.md)",
            milestones,
        )

        self.assertIn(CURRENT_SOURCE_VERSION, contributing)
        self.assertIn("source version is not a public install coordinate", contributing)

        candidate_contract = CORE_0_13_0_CONTRACT.read_text(encoding="utf-8")
        candidate_plan = CORE_0_13_0_CANDIDATE_PLAN.read_text(encoding="utf-8")
        candidate_notes = CORE_0_13_0_RELEASE_NOTES.read_text(encoding="utf-8")
        self.assertIn("PUBLICATION_IDENTITY_MISMATCH", candidate_contract)
        self.assertIn("C1_IMPLEMENTING", candidate_plan)
        self.assertIn("SOURCE_FORWARD_COMPATIBILITY", candidate_plan)
        self.assertRegex(
            candidate_notes,
            r"(?m)^> 状态：`RELEASE CANDIDATE / PENDING PUBLIC READBACK`$",
        )
        self.assertRegex(
            candidate_notes,
            r"(?m)^> 当前公开稳定 Core：`0\.12\.2`$",
        )
        self.assertRegex(
            candidate_notes,
            r"(?m)^> 候选源码版本：`0\.13\.0`$",
        )

        bug_template = BUG_TEMPLATE.read_text(encoding="utf-8")
        self.assertIn("placeholder: v0.12.2 or 40-character commit SHA", bug_template)
        self.assertNotIn("placeholder: v0.12.1 or 40-character commit SHA", bug_template)

        bounded_proposal = BOUNDED_PROPOSAL_TEMPLATE.read_text(encoding="utf-8")
        self.assertIn(
            "Core v0.12.0/v0.12.1/v0.12.2 or historical entry-layer releases",
            bounded_proposal,
        )

        starter_readme = STARTER_README.read_text(encoding="utf-8")
        self.assertIn(
            "releases/download/v0.12.2/veritrail-0.12.2-py3-none-any.whl",
            starter_readme,
        )
        self.assertNotIn(
            "releases/download/v0.12.1/veritrail-0.12.1-py3-none-any.whl",
            starter_readme,
        )
        self.assertNotIn(
            "current 0.12.1 maintenance release",
            starter_readme,
        )

    def test_consumer_compatibility_coordinates_remain_separate(self) -> None:
        starter_pyproject = STARTER_PYPROJECT.read_text(encoding="utf-8")
        starter_doctor = (
            REPOSITORY_ROOT / "starter" / "src" / "veritrail_starter" / "doctor.py"
        ).read_text(encoding="utf-8")
        github_plugin_pyproject = GITHUB_PLUGIN_PYPROJECT.read_text(encoding="utf-8")
        public_ci = PUBLIC_CI.read_text(encoding="utf-8")

        self.assertIn('"veritrail>=0.12,<0.13"', starter_pyproject)
        self.assertIn("Starter 0.2 requires VeriTrail Core >=0.12,<0.13", starter_doctor)
        self.assertIn('dependencies = ["veritrail==0.12.2"]', github_plugin_pyproject)
        self.assertIn(
            "Verify Starter 0.2.0 rejects the Core 0.13.0 candidate",
            public_ci,
        )
        self.assertIn(
            "python -m pip install --no-deps --editable ./plugins/github-evidence",
            public_ci,
        )
        self.assertIn(
            "Run Starter and Authoring Skill 0.2.0 on their declared Core 0.12.2 lane",
            public_ci,
        )
        self.assertIn(
            "authoring_skill_acceptance.py --python $venvPython --preset static-site --optimized",
            public_ci,
        )
        self.assertNotIn("Run the real Authoring Skill DRAFT chain", public_ci)
        self.assertNotIn("Starter for source-forward compatibility only", public_ci)
        self.assertGreaterEqual(public_ci.count("veritrail.__version__ == '0.13.0'"), 5)
        self.assertIn("GitHub Evidence for source-forward compatibility only", public_ci)
        self.assertIn("capabilities_absent", public_ci)
        self.assertIn("'veritrail-github-evidence' not in installed", public_ci)

    def test_starter_020_rejects_the_core_0130_candidate(self) -> None:
        from veritrail_starter.doctor import require_compatible_core
        from veritrail_starter.errors import StarterError

        with self.assertRaises(StarterError) as caught:
            require_compatible_core()
        self.assertEqual(caught.exception.code, "CORE_INCOMPATIBLE")
        self.assertEqual(caught.exception.exit_code, 5)

    def test_historical_release_coordinates_remain_explicit(self) -> None:
        m14_facts = M14_FACTS.read_text(encoding="utf-8")
        self.assertIn("- 结论：`FROZEN / RELEASED`；", m14_facts)
        self.assertIn("- 稳定版本：`0.12.0`；", m14_facts)
        self.assertIn("- 注释标签：`v0.12.0`；", m14_facts)

        release_0_12_0 = CORE_0_12_0_RELEASE_NOTES.read_text(encoding="utf-8")
        self.assertIn("# VeriTrail 0.12.0 Release Notes", release_0_12_0)
        self.assertIn("VeriTrail 0.12.0 是首个稳定 GitHub Release", release_0_12_0)

        contract_0_12_1 = CORE_0_12_1_CONTRACT.read_text(encoding="utf-8")
        self.assertRegex(
            contract_0_12_1,
            r"(?m)^> 状态：`RELEASED / MAINTENANCE FROZEN`$",
        )
        self.assertRegex(
            contract_0_12_1,
            r"(?m)^> 稳定基线：`VeriTrail Core 0\.12\.0` @ 不可移动标签 `v0\.12\.0`$",
        )
        self.assertRegex(
            contract_0_12_1,
            r"(?m)^> 发布坐标：`0\.12\.1` @ 受保护注释标签 `v0\.12\.1`$",
        )

        release_0_12_1 = CORE_0_12_1_RELEASE_NOTES.read_text(encoding="utf-8")
        self.assertIn("# VeriTrail 0.12.1 Release Notes", release_0_12_1)
        self.assertIn("VeriTrail 0.12.1 是 Core 0.12.0 之后的有界维护版", release_0_12_1)

        readback_0_12_1 = CORE_0_12_1_READBACK.read_text(encoding="utf-8")
        self.assertIn("- 状态：`RELEASED / MAINTENANCE FROZEN`；", readback_0_12_1)
        self.assertIn("- 版本：`0.12.1`；", readback_0_12_1)
        self.assertIn(
            "0bdedebd27d35c093b6bfba575e1b81305375a10", readback_0_12_1
        )


if __name__ == "__main__":
    unittest.main()
