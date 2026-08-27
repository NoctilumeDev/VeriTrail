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
CURRENT_SOURCE_VERSION = "0.12.2"
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


class CoreVersionContractTests(unittest.TestCase):
    def test_source_uses_the_current_released_maintenance_coordinate(self) -> None:
        pyproject = PYPROJECT.read_text(encoding="utf-8")
        match = re.search(
            r'(?ms)^\[project\]\s*.*?^version = "([^"]+)"$',
            pyproject,
        )
        self.assertIsNotNone(match, "[project].version is missing from pyproject.toml")
        project_version = match.group(1)

        self.assertEqual(project_version, CURRENT_SOURCE_VERSION)
        self.assertEqual(__version__, CURRENT_SOURCE_VERSION)
        self.assertEqual(project_version, STABLE_CORE_VERSION)
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

        self.assertIn(CURRENT_SOURCE_VERSION, contributing)
        self.assertNotIn("pending public readback", contributing.lower())

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
