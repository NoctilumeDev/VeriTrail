from __future__ import annotations

import hashlib
import tempfile
import unittest
from dataclasses import dataclass
from pathlib import Path

from scripts.download_release_asset import (
    DigestMismatch,
    DownloadAttemptResult,
    NonRetryableDownloadError,
    RetryBudgetExceeded,
    download_release_asset,
)


URL = "https://github.com/example/project/releases/download/v1/asset.bin"
PAYLOAD = b"verified release asset"
DIGEST = hashlib.sha256(PAYLOAD).hexdigest()


class FakeClock:
    def __init__(self) -> None:
        self.now = 0.0
        self.sleeps: list[float] = []

    def monotonic(self) -> float:
        return self.now

    def sleep(self, seconds: float) -> None:
        self.sleeps.append(seconds)
        self.now += seconds


@dataclass(frozen=True)
class AttemptFixture:
    result: DownloadAttemptResult
    body: bytes = b""
    elapsed: float = 0.0


class ScriptedAttemptRunner:
    def __init__(self, outcomes: list[AttemptFixture], clock: FakeClock) -> None:
        self.outcomes = list(outcomes)
        self.clock = clock
        self.timeouts: list[float] = []
        self.calls = 0

    def __call__(
        self, *, url: str, partial: Path, timeout_seconds: float
    ) -> DownloadAttemptResult:
        del url
        self.calls += 1
        self.timeouts.append(timeout_seconds)
        if not self.outcomes:
            raise AssertionError("unexpected attempt runner call")
        outcome = self.outcomes.pop(0)
        partial.write_bytes(outcome.body)
        self.clock.now += outcome.elapsed
        return outcome.result


def http_result(status: int) -> DownloadAttemptResult:
    return DownloadAttemptResult(exit_code=22, http_status=status)


def transport_result(exit_code: int) -> DownloadAttemptResult:
    return DownloadAttemptResult(exit_code=exit_code, http_status=None)


def success_result() -> DownloadAttemptResult:
    return DownloadAttemptResult(exit_code=0, http_status=200)


class ReleaseAssetDownloadTests(unittest.TestCase):
    def run_download(
        self,
        root: Path,
        runner: ScriptedAttemptRunner,
        clock: FakeClock,
        **overrides: object,
    ) -> Path:
        output = root / "asset.bin"
        arguments: dict[str, object] = {
            "url": URL,
            "output": output,
            "expected_sha256": DIGEST,
            "attempt_runner": runner,
            "monotonic": clock.monotonic,
            "sleep": clock.sleep,
            "reporter": lambda _: None,
        }
        arguments.update(overrides)
        download_release_asset(**arguments)  # type: ignore[arg-type]
        return output

    def test_retries_500_with_exponential_backoff_then_publishes_verified_bytes(self) -> None:
        with tempfile.TemporaryDirectory(prefix="veritrail-release-download-") as raw_temp:
            root = Path(raw_temp)
            clock = FakeClock()
            runner = ScriptedAttemptRunner(
                [
                    AttemptFixture(http_result(500)),
                    AttemptFixture(http_result(503)),
                    AttemptFixture(success_result(), PAYLOAD),
                ],
                clock,
            )

            output = self.run_download(root, runner, clock)

            self.assertEqual(output.read_bytes(), PAYLOAD)
            self.assertEqual(clock.sleeps, [2.0, 4.0])
            self.assertEqual(runner.calls, 3)

    def test_capped_backoff_can_use_remaining_absolute_budget(self) -> None:
        with tempfile.TemporaryDirectory(prefix="veritrail-release-download-") as raw_temp:
            root = Path(raw_temp)
            clock = FakeClock()
            runner = ScriptedAttemptRunner(
                [
                    *[AttemptFixture(http_result(500)) for _ in range(5)],
                    AttemptFixture(success_result(), PAYLOAD),
                ],
                clock,
            )

            output = self.run_download(root, runner, clock)

            self.assertEqual(output.read_bytes(), PAYLOAD)
            self.assertEqual(runner.calls, 6)
            self.assertEqual(clock.sleeps, [2.0, 4.0, 8.0, 16.0, 16.0])
            self.assertEqual(clock.now, 46.0)

    def test_capped_backoff_stops_at_the_shared_absolute_budget(self) -> None:
        with tempfile.TemporaryDirectory(prefix="veritrail-release-download-") as raw_temp:
            root = Path(raw_temp)
            clock = FakeClock()
            runner = ScriptedAttemptRunner(
                [AttemptFixture(http_result(500)) for _ in range(6)], clock
            )

            with self.assertRaises(RetryBudgetExceeded):
                self.run_download(root, runner, clock)

            self.assertEqual(runner.calls, 6)
            self.assertEqual(clock.sleeps, [2.0, 4.0, 8.0, 16.0, 16.0])
            self.assertEqual(clock.now, 46.0)
            self.assertFalse((root / "asset.bin").exists())
            self.assertEqual(list(root.glob(".*.part")), [])

    def test_404_fails_immediately_without_retry(self) -> None:
        with tempfile.TemporaryDirectory(prefix="veritrail-release-download-") as raw_temp:
            root = Path(raw_temp)
            clock = FakeClock()
            runner = ScriptedAttemptRunner([AttemptFixture(http_result(404))], clock)

            with self.assertRaises(NonRetryableDownloadError):
                self.run_download(root, runner, clock)

            self.assertEqual(runner.calls, 1)
            self.assertEqual(clock.sleeps, [])
            self.assertFalse((root / "asset.bin").exists())

    def test_digest_mismatch_fails_immediately_without_retry(self) -> None:
        with tempfile.TemporaryDirectory(prefix="veritrail-release-download-") as raw_temp:
            root = Path(raw_temp)
            clock = FakeClock()
            runner = ScriptedAttemptRunner(
                [
                    AttemptFixture(success_result(), b"wrong"),
                    AttemptFixture(success_result(), PAYLOAD),
                ],
                clock,
            )

            with self.assertRaises(DigestMismatch):
                self.run_download(root, runner, clock)

            self.assertEqual(runner.calls, 1)
            self.assertEqual(clock.sleeps, [])
            self.assertFalse((root / "asset.bin").exists())

    def test_connection_reset_and_timeout_exit_codes_can_recover(self) -> None:
        with tempfile.TemporaryDirectory(prefix="veritrail-release-download-") as raw_temp:
            root = Path(raw_temp)
            clock = FakeClock()
            runner = ScriptedAttemptRunner(
                [
                    AttemptFixture(transport_result(56)),
                    AttemptFixture(transport_result(28)),
                    AttemptFixture(success_result(), PAYLOAD),
                ],
                clock,
            )

            output = self.run_download(root, runner, clock)

            self.assertEqual(output.read_bytes(), PAYLOAD)
            self.assertEqual(clock.sleeps, [2.0, 4.0])

    def test_all_attempts_share_one_absolute_budget(self) -> None:
        with tempfile.TemporaryDirectory(prefix="veritrail-release-download-") as raw_temp:
            root = Path(raw_temp)
            clock = FakeClock()
            runner = ScriptedAttemptRunner(
                [
                    AttemptFixture(transport_result(28), elapsed=7.0),
                    AttemptFixture(transport_result(28), elapsed=10.0),
                ],
                clock,
            )

            with self.assertRaises(RetryBudgetExceeded):
                self.run_download(
                    root,
                    runner,
                    clock,
                    retry_budget_seconds=20.0,
                    request_timeout_seconds=15.0,
                )

            self.assertEqual(runner.timeouts, [15.0, 11.0])
            self.assertEqual(clock.sleeps, [2.0])
            self.assertEqual(clock.now, 19.0)

    def test_success_returned_after_absolute_deadline_is_not_published(self) -> None:
        with tempfile.TemporaryDirectory(prefix="veritrail-release-download-") as raw_temp:
            root = Path(raw_temp)
            clock = FakeClock()
            runner = ScriptedAttemptRunner(
                [AttemptFixture(success_result(), PAYLOAD, elapsed=21.0)], clock
            )

            with self.assertRaises(RetryBudgetExceeded):
                self.run_download(
                    root,
                    runner,
                    clock,
                    retry_budget_seconds=20.0,
                    request_timeout_seconds=15.0,
                )

            self.assertFalse((root / "asset.bin").exists())
            self.assertEqual(list(root.glob(".*.part")), [])

    def test_certificate_validation_error_is_not_retried(self) -> None:
        with tempfile.TemporaryDirectory(prefix="veritrail-release-download-") as raw_temp:
            root = Path(raw_temp)
            clock = FakeClock()
            runner = ScriptedAttemptRunner(
                [AttemptFixture(transport_result(60))], clock
            )

            with self.assertRaises(NonRetryableDownloadError):
                self.run_download(root, runner, clock)

            self.assertEqual(runner.calls, 1)
            self.assertEqual(clock.sleeps, [])

    def test_existing_target_is_rejected_before_download_attempt(self) -> None:
        with tempfile.TemporaryDirectory(prefix="veritrail-release-download-") as raw_temp:
            root = Path(raw_temp)
            output = root / "asset.bin"
            output.write_bytes(b"existing")
            clock = FakeClock()
            runner = ScriptedAttemptRunner(
                [AttemptFixture(success_result(), PAYLOAD)], clock
            )

            with self.assertRaises(NonRetryableDownloadError):
                self.run_download(root, runner, clock)

            self.assertEqual(runner.calls, 0)
            self.assertEqual(output.read_bytes(), b"existing")

    def test_non_finite_budget_is_rejected_before_download_attempt(self) -> None:
        with tempfile.TemporaryDirectory(prefix="veritrail-release-download-") as raw_temp:
            root = Path(raw_temp)
            clock = FakeClock()
            runner = ScriptedAttemptRunner(
                [AttemptFixture(success_result(), PAYLOAD)], clock
            )

            with self.assertRaises(NonRetryableDownloadError):
                self.run_download(root, runner, clock, retry_budget_seconds=float("nan"))

            self.assertEqual(runner.calls, 0)

    def test_partial_file_is_removed_before_retry_and_after_failure(self) -> None:
        with tempfile.TemporaryDirectory(prefix="veritrail-release-download-") as raw_temp:
            root = Path(raw_temp)
            clock = FakeClock()
            runner = ScriptedAttemptRunner(
                [
                    AttemptFixture(transport_result(56), b"partial"),
                    AttemptFixture(http_result(404)),
                ],
                clock,
            )

            with self.assertRaises(NonRetryableDownloadError):
                self.run_download(root, runner, clock)

            self.assertEqual(runner.calls, 2)
            self.assertEqual(list(root.glob(".*.part")), [])
            self.assertFalse((root / "asset.bin").exists())


if __name__ == "__main__":
    unittest.main()
