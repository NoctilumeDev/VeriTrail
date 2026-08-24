from __future__ import annotations

import gzip
import io
import tarfile
import tempfile
import unittest
from pathlib import Path

from scripts.entry_layer_e1_acceptance import AcceptanceFailure
from scripts.entry_layer_e3_acceptance import (
    PRESETS,
    RELEASE_SOURCE_DATE_EPOCH,
    normalize_sdist,
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

    def test_sdist_normalization_removes_archive_time_variance(self) -> None:
        with tempfile.TemporaryDirectory() as raw_temp:
            root = Path(raw_temp)
            outputs: list[bytes] = []
            for index, mtime in enumerate((1, 2)):
                path = root / f"candidate-{index}.tar.gz"
                with path.open("wb") as raw_output:
                    with gzip.GzipFile(
                        filename=f"candidate-{index}.tar",
                        mode="wb",
                        fileobj=raw_output,
                        mtime=mtime,
                    ) as compressed_output:
                        with tarfile.open(fileobj=compressed_output, mode="w") as archive:
                            member = tarfile.TarInfo("package/value.txt")
                            member.size = 5
                            member.mtime = mtime
                            member.uid = index + 1
                            member.gid = index + 2
                            archive.addfile(member, io.BytesIO(b"value"))
                normalize_sdist(path)
                outputs.append(path.read_bytes())

            self.assertEqual(outputs[0], outputs[1])
            with tarfile.open(fileobj=io.BytesIO(outputs[0]), mode="r:gz") as archive:
                member = archive.getmember("package/value.txt")
                self.assertEqual(member.mtime, RELEASE_SOURCE_DATE_EPOCH)
                self.assertEqual(member.uid, 0)
                self.assertEqual(member.gid, 0)


if __name__ == "__main__":
    unittest.main()
