from __future__ import annotations

import http.client
import os
import socket
import sys
import tempfile
import threading
import unittest
from pathlib import Path
from types import SimpleNamespace

from veritrail.bootstrap_lifecycle import (
    BootstrapServiceSpec,
    materialize_bootstrap_service_specs,
    run_bootstrap_lifecycle,
)
from veritrail.bootstrap_preview import ResolvedBootstrap, ResolvedBootstrapNode
from veritrail.project_profile import seal_project_profile
from veritrail.windows_readiness import (
    OwnedReadinessObservation,
)
from veritrail.windows_service import (
    OwnedServiceStartObservation,
)

from tests.support import bootstrap_profile

ROOT = Path(__file__).resolve().parents[1]


def _free_port(excluded: set[int] | None = None) -> int:
    excluded = set() if excluded is None else excluded
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as candidate:
            candidate.bind(("127.0.0.1", 0))
            port = int(candidate.getsockname()[1])
        if port not in excluded:
            return port


def _environment(directory: Path) -> dict[str, str]:
    result = {
        "PYTHONDONTWRITEBYTECODE": "1",
        "TEMP": str(directory),
        "TMP": str(directory),
    }
    for name in ("SYSTEMROOT", "WINDIR"):
        value = os.environ.get(name)
        if value:
            result[name] = value
    return result


def _spec(
    *,
    node_id: str,
    role: str,
    port: int,
    directory: Path,
    arguments: tuple[str, ...],
    readiness_timeout_ms: int = 3_000,
) -> BootstrapServiceSpec:
    return BootstrapServiceSpec(
        node_id=node_id,
        role=role,
        executable=Path(sys.executable),
        arguments=("-m", "tests.fixtures.m10_service_helper", *arguments),
        working_directory=ROOT,
        environment=_environment(directory),
        port=port,
        readiness={
            "adapter": "HTTP_GET_LOOPBACK_OWNED_PID",
            "path": "/health",
            "expected_status": 200,
            "attempt_timeout_ms": 250,
            "total_timeout_ms": readiness_timeout_ms,
            "interval_ms": 50,
            "consecutive_successes": 2,
            "max_response_bytes": 4096,
        },
        limits={
            "max_stdout_bytes": 65_536,
            "max_stderr_bytes": 65_536,
            "max_processes": 4,
        },
        shutdown={
            "adapter": "JOB_TERMINATE_AFTER_CAPTURE",
            "process_release_timeout_ms": 3_000,
            "port_release_timeout_ms": 3_000,
            "reader_shutdown_timeout_ms": 3_000,
        },
    )


class BootstrapLifecycleTests(unittest.TestCase):
    def _ports(self) -> tuple[int, int]:
        dependency = _free_port()
        application = _free_port({dependency})
        return dependency, application

    @unittest.skipUnless(os.name == "nt", "M10 service lifecycle is Windows-only")
    def test_two_nodes_start_serially_expose_dependency_fact_and_teardown_in_reverse(self) -> None:
        with tempfile.TemporaryDirectory() as raw_directory:
            directory = Path(raw_directory)
            dependency_port, application_port = self._ports()
            specs = (
                _spec(
                    node_id="dependency",
                    role="DEPENDENCY",
                    port=dependency_port,
                    directory=directory,
                    arguments=("child-listener", str(dependency_port)),
                ),
                _spec(
                    node_id="application",
                    role="APPLICATION",
                    port=application_port,
                    directory=directory,
                    arguments=(
                        "application",
                        str(application_port),
                        f"http://127.0.0.1:{dependency_port}",
                    ),
                ),
            )
            observed: list[bytes] = []

            def inspect_application() -> None:
                connection = http.client.HTTPConnection(
                    "127.0.0.1", application_port, timeout=1
                )
                try:
                    connection.request("GET", "/")
                    response = connection.getresponse()
                    observed.append(response.read(4096))
                    self.assertEqual(200, response.status)
                finally:
                    connection.close()

            result = run_bootstrap_lifecycle(
                specs,
                lifecycle_timeout_ms=15_000,
                on_services_ready=inspect_application,
            )
            self.assertTrue(result.services_ready)
            self.assertTrue(result.ready_callback_completed)
            self.assertEqual(b'{"dependency_status": 200}', observed[0])
            self.assertEqual(("dependency", "application"), result.actual_start_order)
            self.assertEqual(("application", "dependency"), result.actual_teardown_order)
            self.assertEqual("NONE", result.stop_reason)
            self.assertTrue(result.cleanup_complete)
            self.assertTrue(all(node.teardown is not None for node in result.nodes))

    @unittest.skipUnless(os.name == "nt", "M10 service lifecycle is Windows-only")
    def test_dependency_early_exit_prevents_application_creation(self) -> None:
        with tempfile.TemporaryDirectory() as raw_directory:
            directory = Path(raw_directory)
            dependency_port, application_port = self._ports()
            specs = (
                _spec(
                    node_id="dependency",
                    role="DEPENDENCY",
                    port=dependency_port,
                    directory=directory,
                    arguments=("early-exit", "17"),
                ),
                _spec(
                    node_id="application",
                    role="APPLICATION",
                    port=application_port,
                    directory=directory,
                    arguments=("serve", str(application_port)),
                ),
            )
            result = run_bootstrap_lifecycle(specs, lifecycle_timeout_ms=10_000)
            self.assertEqual(("dependency",), result.actual_start_order)
            self.assertEqual(("dependency",), result.actual_teardown_order)
            self.assertEqual("NODE_EARLY_EXIT", result.stop_reason)
            self.assertIsNone(result.nodes[1].start)
            self.assertTrue(result.cleanup_complete)

    @unittest.skipUnless(os.name == "nt", "M10 service lifecycle is Windows-only")
    def test_application_readiness_timeout_cleans_both_nodes_in_reverse(self) -> None:
        with tempfile.TemporaryDirectory() as raw_directory:
            directory = Path(raw_directory)
            dependency_port, application_port = self._ports()
            specs = (
                _spec(
                    node_id="dependency",
                    role="DEPENDENCY",
                    port=dependency_port,
                    directory=directory,
                    arguments=("serve", str(dependency_port)),
                ),
                _spec(
                    node_id="application",
                    role="APPLICATION",
                    port=application_port,
                    directory=directory,
                    arguments=("sleep", "30"),
                    readiness_timeout_ms=500,
                ),
            )
            result = run_bootstrap_lifecycle(specs, lifecycle_timeout_ms=10_000)
            self.assertFalse(result.services_ready)
            self.assertEqual("READINESS_TIMEOUT", result.stop_reason)
            self.assertEqual(("dependency", "application"), result.actual_start_order)
            self.assertEqual(("application", "dependency"), result.actual_teardown_order)
            self.assertTrue(result.cleanup_complete)

    @unittest.skipUnless(os.name == "nt", "M10 service lifecycle is Windows-only")
    def test_cancel_after_services_ready_preserves_fact_and_cleans_both_nodes(self) -> None:
        with tempfile.TemporaryDirectory() as raw_directory:
            directory = Path(raw_directory)
            dependency_port, application_port = self._ports()
            specs = (
                _spec(
                    node_id="dependency",
                    role="DEPENDENCY",
                    port=dependency_port,
                    directory=directory,
                    arguments=("serve", str(dependency_port)),
                ),
                _spec(
                    node_id="application",
                    role="APPLICATION",
                    port=application_port,
                    directory=directory,
                    arguments=("serve", str(application_port)),
                ),
            )
            cancellation = threading.Event()
            result = run_bootstrap_lifecycle(
                specs,
                lifecycle_timeout_ms=10_000,
                cancel_event=cancellation,
                on_services_ready=cancellation.set,
            )
            self.assertTrue(result.services_ready)
            self.assertTrue(result.ready_callback_completed)
            self.assertEqual("USER_CANCELLED", result.trigger_reason)
            self.assertEqual("USER_CANCELLED", result.stop_reason)
            self.assertEqual(("application", "dependency"), result.actual_teardown_order)
            self.assertTrue(result.cleanup_complete)

    def test_teardown_failure_does_not_block_remaining_reverse_cleanup(self) -> None:
        with tempfile.TemporaryDirectory() as raw_directory:
            directory = Path(raw_directory)
            dependency_port, application_port = self._ports()
            specs = (
                _spec(
                    node_id="dependency",
                    role="DEPENDENCY",
                    port=dependency_port,
                    directory=directory,
                    arguments=("sleep", "30"),
                ),
                _spec(
                    node_id="application",
                    role="APPLICATION",
                    port=application_port,
                    directory=directory,
                    arguments=("sleep", "30"),
                ),
            )
            terminated: list[str] = []
            sequence: list[str] = []

            class FakeSession:
                def __init__(self, node_id: str) -> None:
                    self.node_id = node_id
                    self.start_observation = OwnedServiceStartObservation(
                        parent_in_job=False,
                        process_created=True,
                        target_assigned=True,
                        target_resumed=True,
                        active_process_limit=4,
                        active_process_limit_enforced=True,
                        cleanup_complete=False,
                        error_type=None,
                        elapsed_ms=1.0,
                    )

                def terminate(self) -> object:
                    terminated.append(self.node_id)
                    sequence.append(f"teardown:{self.node_id}")
                    if self.node_id == "application":
                        raise RuntimeError("injected teardown failure")
                    return SimpleNamespace(cleanup_complete=True)

            def factory(**values: object) -> FakeSession:
                return FakeSession(str(values["node_id"]))

            def ready(*args: object, **kwargs: object) -> OwnedReadinessObservation:
                return OwnedReadinessObservation(
                    ready=True,
                    attempts=(),
                    error_type=None,
                    elapsed_ms=1.0,
                )

            def finalize(snapshot: object) -> None:
                sequence.append("evidence-finalized")
                nodes = getattr(snapshot, "nodes")
                self.assertTrue(all(node.teardown is None for node in nodes))

            result = run_bootstrap_lifecycle(
                specs,
                lifecycle_timeout_ms=5_000,
                session_factory=factory,
                readiness_probe=ready,
                on_evidence_finalize=finalize,
            )
            self.assertEqual(["application", "dependency"], terminated)
            self.assertEqual(
                ["evidence-finalized", "teardown:application", "teardown:dependency"],
                sequence,
            )
            self.assertTrue(
                any(event.stage == "EVIDENCE_FINALIZED" for event in result.events)
            )
            self.assertEqual(("application", "dependency"), result.teardown_attempt_order)
            self.assertEqual(("dependency",), result.actual_teardown_order)
            self.assertEqual("NONE", result.trigger_reason)
            self.assertEqual("CLEANUP_ERROR", result.stop_reason)
            self.assertFalse(result.cleanup_complete)

    def test_evidence_finalization_failure_precedes_and_does_not_skip_cleanup(self) -> None:
        with tempfile.TemporaryDirectory() as raw_directory:
            directory = Path(raw_directory)
            dependency_port, application_port = self._ports()
            specs = (
                _spec(
                    node_id="dependency",
                    role="DEPENDENCY",
                    port=dependency_port,
                    directory=directory,
                    arguments=("sleep", "30"),
                ),
                _spec(
                    node_id="application",
                    role="APPLICATION",
                    port=application_port,
                    directory=directory,
                    arguments=("sleep", "30"),
                ),
            )
            terminated: list[str] = []

            class FakeSession:
                def __init__(self, node_id: str) -> None:
                    self.node_id = node_id
                    self.start_observation = OwnedServiceStartObservation(
                        parent_in_job=False,
                        process_created=True,
                        target_assigned=True,
                        target_resumed=True,
                        active_process_limit=4,
                        active_process_limit_enforced=True,
                        cleanup_complete=False,
                        error_type=None,
                        elapsed_ms=1.0,
                    )

                def terminate(self) -> object:
                    terminated.append(self.node_id)
                    return SimpleNamespace(cleanup_complete=True)

            def factory(**values: object) -> FakeSession:
                return FakeSession(str(values["node_id"]))

            def ready(*args: object, **kwargs: object) -> OwnedReadinessObservation:
                return OwnedReadinessObservation(
                    ready=True,
                    attempts=(),
                    error_type=None,
                    elapsed_ms=1.0,
                )

            def fail_finalization(snapshot: object) -> None:
                raise RuntimeError("injected evidence finalization failure")

            result = run_bootstrap_lifecycle(
                specs,
                lifecycle_timeout_ms=5_000,
                session_factory=factory,
                readiness_probe=ready,
                on_evidence_finalize=fail_finalization,
            )
            self.assertEqual("EVIDENCE_ERROR", result.trigger_reason)
            self.assertEqual("EVIDENCE_ERROR", result.stop_reason)
            self.assertTrue(result.cleanup_complete)
            self.assertEqual(["application", "dependency"], terminated)
            failed = next(
                index
                for index, event in enumerate(result.events)
                if event.stage == "EVIDENCE_FINALIZATION"
            )
            first_teardown = next(
                index
                for index, event in enumerate(result.events)
                if event.stage.startswith("TEARDOWN_")
            )
            self.assertLess(failed, first_teardown)

    def test_materialization_keeps_paths_and_environment_values_in_memory(self) -> None:
        with tempfile.TemporaryDirectory() as raw_directory:
            root = Path(raw_directory)
            subject = root / "subject"
            subject.mkdir()
            run_work = root / "run-work"
            run_work.mkdir()
            profile = seal_project_profile(bootstrap_profile())
            resolved = ResolvedBootstrap(
                preview={},
                subject_root=subject,
                nodes=tuple(
                    ResolvedBootstrapNode(
                        node_id=node_id,
                        executable=Path(sys.executable),
                        executable_identity={},
                        working_directory=subject,
                        inherited_environment={"SYSTEMROOT": "C:\\Windows"},
                        explicit_environment={"PYTHONDONTWRITEBYTECODE": "1"},
                    )
                    for node_id in profile["start_order"]
                ),
            )
            dependency, application = materialize_bootstrap_service_specs(
                profile,
                resolved,
                run_work=run_work,
            )
            self.assertEqual("18771", dependency.arguments[2])
            self.assertEqual("http://127.0.0.1:18771", application.arguments[3])
            self.assertEqual(
                str((run_work / "application").resolve()),
                application.arguments[4],
            )
            self.assertEqual(application.environment["TEMP"], application.environment["TMP"])
            self.assertTrue(Path(application.environment["TEMP"]).is_dir())


if __name__ == "__main__":
    unittest.main()
