from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from veritrail.errors import ValidationError
from veritrail.jsonio import load_json_object


class JsonIoTests(unittest.TestCase):
    def test_bounded_loader_rejects_oversized_input_before_parsing(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "large.json"
            path.write_bytes(b'{"value":"' + b"x" * 64 + b'"}')
            with self.assertRaisesRegex(ValidationError, "limit is 16 bytes"):
                load_json_object(path, label="test JSON", max_bytes=16)

    def test_bounded_loader_refuses_hardlinked_input(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            original = root / "original.json"
            linked = root / "linked.json"
            original.write_text('{"value":true}', encoding="utf-8")
            try:
                linked.hardlink_to(original)
            except OSError as exc:
                self.skipTest(f"hard links unavailable: {exc}")
            with self.assertRaisesRegex(ValidationError, "unsafe or unavailable"):
                load_json_object(linked, label="test JSON", max_bytes=1024)


if __name__ == "__main__":
    unittest.main()
