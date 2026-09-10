from __future__ import annotations

import argparse
import hashlib
import hmac
import math
import os
import re
import shutil
import socket
import subprocess
import sys
import tempfile
import time
import urllib.parse
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Sequence


DEFAULT_RETRY_BUDGET_SECONDS = 60.0
DEFAULT_REQUEST_TIMEOUT_SECONDS = 15.0
DEFAULT_BACKOFF_SECONDS = (2.0, 4.0, 8.0, 16.0)
RETRYABLE_HTTP_STATUSES = frozenset({408, 429, 500, 502, 503, 504})
RETRYABLE_CURL_EXIT_CODES = frozenset({5, 6, 7, 18, 28, 35, 52, 55, 56, 92})
SHA256_PATTERN = re.compile(r"[0-9a-f]{64}")
READ_CHUNK_BYTES = 64 * 1024


class ReleaseAssetDownloadError(RuntimeError):
    pass


class RetryBudgetExceeded(ReleaseAssetDownloadError):
    pass


class NonRetryableDownloadError(ReleaseAssetDownloadError):
    pass


class DigestMismatch(NonRetryableDownloadError):
    pass


@dataclass(frozen=True)
class DownloadAttemptResult:
    exit_code: int
    http_status: int | None


def _default_reporter(message: str) -> None:
    print(message, file=sys.stderr, flush=True)


def _validate_inputs(
    *,
    url: str,
    output: Path,
    expected_sha256: str,
    retry_budget_seconds: float,
    request_timeout_seconds: float,
    backoff_seconds: Sequence[float],
) -> None:
    parsed = urllib.parse.urlsplit(url)
    if parsed.scheme != "https" or not parsed.netloc:
        raise NonRetryableDownloadError("release asset URL must be absolute HTTPS")
    if SHA256_PATTERN.fullmatch(expected_sha256) is None:
        raise NonRetryableDownloadError("expected SHA-256 must be 64 lowercase hex characters")
    if output.exists():
        raise NonRetryableDownloadError(f"refusing to overwrite existing target: {output}")
    if not output.parent.is_dir():
        raise NonRetryableDownloadError(f"output parent directory does not exist: {output.parent}")
    if not math.isfinite(retry_budget_seconds) or retry_budget_seconds <= 0:
        raise NonRetryableDownloadError("retry budget must be positive")
    if not math.isfinite(request_timeout_seconds) or request_timeout_seconds <= 0:
        raise NonRetryableDownloadError("request timeout must be positive")
    if any(not math.isfinite(delay) or delay < 0 for delay in backoff_seconds):
        raise NonRetryableDownloadError("backoff delays must be finite and non-negative")


def _temporary_path(output: Path) -> Path:
    descriptor, raw_path = tempfile.mkstemp(
        dir=output.parent,
        prefix=f".{output.name}.",
        suffix=".part",
    )
    os.close(descriptor)
    return Path(raw_path)


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        while True:
            chunk = source.read(READ_CHUNK_BYTES)
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()


def _publish_verified_partial(partial: Path, output: Path) -> None:
    try:
        os.link(partial, output)
    except FileExistsError as exc:
        raise NonRetryableDownloadError(
            f"refusing to overwrite target created during download: {output}"
        ) from exc
    except OSError as exc:
        raise NonRetryableDownloadError(
            f"failed to publish verified release asset: {type(exc).__name__}"
        ) from exc


def _parse_http_status(stdout: str) -> int | None:
    candidate = stdout.strip().splitlines()
    if not candidate:
        return None
    value = candidate[-1].strip()
    if len(value) != 3 or not value.isascii() or not value.isdigit():
        return None
    return int(value)


def _run_curl_attempt(*, url: str, partial: Path, timeout_seconds: float) -> DownloadAttemptResult:
    curl = shutil.which("curl.exe") or shutil.which("curl")
    if curl is None:
        raise NonRetryableDownloadError("curl executable is unavailable")
    timeout_text = f"{max(timeout_seconds, 0.001):.3f}"
    command = [
        curl,
        "--fail",
        "--location",
        "--silent",
        "--show-error",
        "--proto",
        "=https",
        "--proto-redir",
        "=https",
        "--connect-timeout",
        timeout_text,
        "--max-time",
        timeout_text,
        "--header",
        "Accept: application/octet-stream",
        "--user-agent",
        "VeriTrail-release-asset-gate/1",
        "--output",
        str(partial),
        "--write-out",
        "%{http_code}",
        url,
    ]
    try:
        completed = subprocess.run(
            command,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout_seconds,
            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
        )
    except subprocess.TimeoutExpired as exc:
        raise socket.timeout("curl exceeded the remaining request budget") from exc
    return DownloadAttemptResult(
        exit_code=completed.returncode,
        http_status=_parse_http_status(completed.stdout),
    )


def _classify_attempt_failure(result: DownloadAttemptResult, attempt: int) -> str:
    if result.exit_code == 22:
        if result.http_status in RETRYABLE_HTTP_STATUSES:
            return f"retryable_http status={result.http_status}"
        status = "unknown" if result.http_status is None else str(result.http_status)
        raise NonRetryableDownloadError(
            f"attempt {attempt} returned non-retryable HTTP status: {status}"
        )
    if result.exit_code in RETRYABLE_CURL_EXIT_CODES:
        return f"retryable_transport curl_exit={result.exit_code}"
    raise NonRetryableDownloadError(
        f"attempt {attempt} failed with non-retryable curl exit: {result.exit_code}"
    )


def download_release_asset(
    *,
    url: str,
    output: Path,
    expected_sha256: str,
    retry_budget_seconds: float = DEFAULT_RETRY_BUDGET_SECONDS,
    request_timeout_seconds: float = DEFAULT_REQUEST_TIMEOUT_SECONDS,
    backoff_seconds: Sequence[float] = DEFAULT_BACKOFF_SECONDS,
    attempt_runner: Callable[..., DownloadAttemptResult] = _run_curl_attempt,
    monotonic: Callable[[], float] = time.monotonic,
    sleep: Callable[[float], None] = time.sleep,
    reporter: Callable[[str], None] = _default_reporter,
) -> str:
    output = Path(output)
    _validate_inputs(
        url=url,
        output=output,
        expected_sha256=expected_sha256,
        retry_budget_seconds=retry_budget_seconds,
        request_timeout_seconds=request_timeout_seconds,
        backoff_seconds=backoff_seconds,
    )

    started = monotonic()
    deadline = started + retry_budget_seconds
    attempt = 1

    while True:
        remaining = deadline - monotonic()
        if remaining <= 0:
            raise RetryBudgetExceeded(
                f"release asset recovery budget exhausted before attempt {attempt}"
            )
        timeout = min(request_timeout_seconds, remaining)
        partial = _temporary_path(output)
        attempt_started = monotonic()
        try:
            result = attempt_runner(url=url, partial=partial, timeout_seconds=timeout)
            attempt_elapsed = monotonic() - attempt_started
            if monotonic() > deadline:
                raise RetryBudgetExceeded(
                    f"release asset recovery budget expired during attempt {attempt}"
                )
            if result.exit_code == 0:
                if result.http_status is None or not 200 <= result.http_status < 300:
                    raise NonRetryableDownloadError(
                        f"attempt {attempt} returned unexpected HTTP status: {result.http_status}"
                    )
                observed = _sha256_file(partial)
                if not hmac.compare_digest(observed, expected_sha256):
                    raise DigestMismatch(
                        "release asset SHA-256 mismatch: "
                        f"expected {expected_sha256}, observed {observed}"
                    )
                _publish_verified_partial(partial, output)
                reporter(
                    "release_asset_download "
                    f"outcome=success attempt={attempt} elapsed_seconds={attempt_elapsed:.3f} "
                    f"sha256={observed}"
                )
                return observed
            failure = _classify_attempt_failure(result, attempt)
            cause: BaseException | None = None
        except (DigestMismatch, NonRetryableDownloadError):
            raise
        except (TimeoutError, socket.timeout, ConnectionError) as exc:
            attempt_elapsed = monotonic() - attempt_started
            failure = f"retryable_transport error={type(exc).__name__}"
            cause = exc
        finally:
            partial.unlink(missing_ok=True)

        if not backoff_seconds or (
            attempt > len(backoff_seconds) and backoff_seconds[-1] == 0
        ):
            error = ReleaseAssetDownloadError(
                f"release asset download exhausted {attempt} attempts after {failure}"
            )
            if cause is None:
                raise error
            raise error from cause

        delay = backoff_seconds[min(attempt - 1, len(backoff_seconds) - 1)]
        remaining = deadline - monotonic()
        if remaining <= delay:
            error = RetryBudgetExceeded(
                "release asset recovery budget cannot fund the next bounded retry "
                f"after {failure}"
            )
            if cause is None:
                raise error
            raise error from cause
        reporter(
            "release_asset_download "
            f"outcome=retry attempt={attempt} elapsed_seconds={attempt_elapsed:.3f} "
            f"{failure} next_delay_seconds={delay:g} "
            f"remaining_budget_seconds={remaining:.3f}"
        )
        sleep(delay)
        attempt += 1

    raise AssertionError("unreachable")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Download one immutable release asset under a shared retry deadline."
    )
    parser.add_argument("--url", required=True)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--sha256", required=True)
    parser.add_argument(
        "--retry-budget-seconds",
        type=float,
        default=DEFAULT_RETRY_BUDGET_SECONDS,
    )
    parser.add_argument(
        "--request-timeout-seconds",
        type=float,
        default=DEFAULT_REQUEST_TIMEOUT_SECONDS,
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        download_release_asset(
            url=args.url,
            output=args.output,
            expected_sha256=args.sha256,
            retry_budget_seconds=args.retry_budget_seconds,
            request_timeout_seconds=args.request_timeout_seconds,
        )
    except ReleaseAssetDownloadError as exc:
        print(f"release_asset_download outcome=failure reason={exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
