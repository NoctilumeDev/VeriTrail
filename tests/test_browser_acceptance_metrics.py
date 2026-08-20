from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
RAW_ROOT_WIDTH_DELTA = (
    "document.documentElement.scrollWidth - "
    "document.documentElement.clientWidth"
)
NORMALIZED_ROOT_OVERFLOW = f"Math.max(0, {RAW_ROOT_WIDTH_DELTA})"


class BrowserAcceptanceMetricsTests(unittest.TestCase):
    def test_root_overflow_checks_ignore_reserved_scrollbar_gutter(self) -> None:
        occurrences = 0
        offenders: list[str] = []

        for path in sorted((ROOT / "scripts").glob("*acceptance.py")):
            content = path.read_text(encoding="utf-8")
            occurrences += content.count(NORMALIZED_ROOT_OVERFLOW)
            if RAW_ROOT_WIDTH_DELTA in content.replace(
                NORMALIZED_ROOT_OVERFLOW, ""
            ):
                offenders.append(path.name)

        self.assertGreater(
            occurrences,
            0,
            "acceptance scripts must retain an explicit root overflow check",
        )
        self.assertEqual(
            [],
            offenders,
            "root overflow checks must clamp negative scrollbar-gutter deltas",
        )


if __name__ == "__main__":
    unittest.main()
