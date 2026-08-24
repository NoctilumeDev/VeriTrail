from __future__ import annotations

import unittest

from scripts.entry_layer_e1_acceptance import AcceptanceFailure
from scripts.entry_layer_e3_acceptance import (
    PRESETS,
    require_release_python_series,
    stable_preset_facts,
)


class EntryLayerE3AcceptanceTests(unittest.TestCase):
    def test_candidate_requires_exact_dual_python_series(self) -> None:
        require_release_python_series(["3.10.6", "3.13.13"])
        with self.assertRaises(AcceptanceFailure):
            require_release_python_series(["3.10.6"])
        with self.assertRaises(AcceptanceFailure):
            require_release_python_series(["3.10.6", "3.11.9"])

    def test_presets_are_explicit_and_bounded(self) -> None:
        self.assertEqual(PRESETS, ("single-webapp", "static-site"))

    def test_optimized_marker_is_not_a_semantic_fact(self) -> None:
        normal = {"state": "PASS", "preset": "static-site", "optimized": False}
        optimized = {"state": "PASS", "preset": "static-site", "optimized": True}
        self.assertEqual(stable_preset_facts(normal), stable_preset_facts(optimized))


if __name__ == "__main__":
    unittest.main()
