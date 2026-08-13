from __future__ import annotations

import threading
import unittest

from veritrail.stop_control import StopSignal, requested_stop_reason


class StopSignalTests(unittest.TestCase):
    def test_external_event_maps_to_user_cancel(self) -> None:
        event = threading.Event()
        signal = StopSignal(event)
        self.assertIsNone(requested_stop_reason(signal))
        event.set()
        self.assertEqual("USER_CANCELLED", requested_stop_reason(signal))

    def test_hard_memory_limit_upgrades_soft_limit_but_not_user_cancel(self) -> None:
        resource_signal = StopSignal()
        self.assertTrue(resource_signal.request("RESOURCE_MEMORY_SOFT_LIMIT"))
        self.assertTrue(resource_signal.request("RESOURCE_MEMORY_HARD_LIMIT"))
        self.assertEqual("RESOURCE_MEMORY_HARD_LIMIT", resource_signal.reason())
        self.assertTrue(resource_signal.request("USER_CANCELLED"))
        self.assertEqual("USER_CANCELLED", resource_signal.reason())

        user_signal = StopSignal()
        self.assertTrue(user_signal.request("USER_CANCELLED"))
        self.assertFalse(user_signal.request("RESOURCE_MEMORY_HARD_LIMIT"))
        self.assertEqual("USER_CANCELLED", user_signal.reason())

        external = threading.Event()
        external.set()
        external_signal = StopSignal(external)
        self.assertFalse(external_signal.request("RESOURCE_MEMORY_HARD_LIMIT"))
        self.assertEqual("USER_CANCELLED", external_signal.reason())

        late_external = threading.Event()
        late_external_signal = StopSignal(late_external)
        self.assertTrue(
            late_external_signal.request("RESOURCE_MEMORY_HARD_LIMIT")
        )
        late_external.set()
        self.assertEqual("USER_CANCELLED", late_external_signal.reason())


if __name__ == "__main__":
    unittest.main()
