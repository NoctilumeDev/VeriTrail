from __future__ import annotations


class StarterError(Exception):
    """Expected, privacy-safe Starter failure."""

    def __init__(self, code: str, messages: list[str] | tuple[str, ...], *, exit_code: int) -> None:
        self.code = code
        self.messages = tuple(messages)
        self.exit_code = exit_code
        super().__init__("; ".join(self.messages))


def invalid(*messages: str) -> StarterError:
    return StarterError("INVALID_INPUT", list(messages), exit_code=2)


def conflict(*messages: str) -> StarterError:
    return StarterError("OUTPUT_CONFLICT", list(messages), exit_code=3)


def unsupported(*messages: str) -> StarterError:
    return StarterError("UNSUPPORTED", list(messages), exit_code=4)


def incompatible(*messages: str) -> StarterError:
    return StarterError("CORE_INCOMPATIBLE", list(messages), exit_code=5)


def needs_input(*messages: str) -> StarterError:
    return StarterError("NEEDS_INPUT", list(messages), exit_code=6)


def workspace_invalid(*messages: str) -> StarterError:
    return StarterError("WORKSPACE_INVALID", list(messages), exit_code=7)


def environment_not_ready(*messages: str) -> StarterError:
    return StarterError("ENVIRONMENT_NOT_READY", list(messages), exit_code=8)
