from __future__ import annotations

from collections.abc import Sequence


_GENERIC_FORBIDDEN_ENTRY_POINTS = {
    "-c",
    "/c",
    "-e",
    "--eval",
    "-command",
}


def is_forbidden_inline_literal(value: str, tool_binding: object = None) -> bool:
    """Reject sealed literals that encode code in an interpreter option."""

    normalized = value.casefold()
    if normalized in _GENERIC_FORBIDDEN_ENTRY_POINTS:
        return True
    binding = tool_binding.casefold() if isinstance(tool_binding, str) else ""
    if binding.startswith("python"):
        return forbidden_runtime_argument("python", [value]) is not None
    if binding.startswith("node"):
        return forbidden_runtime_argument("node", [value]) is not None
    return normalized.startswith("--eval=")


def forbidden_runtime_argument(
    family: str,
    arguments: Sequence[str],
) -> str | None:
    """Return the first alternate program entry point before ``--``."""

    if family == "python":
        index = 0
        while index < len(arguments):
            argument = arguments[index]
            if argument == "--":
                break
            if not argument.startswith("-") or argument == "-":
                index += 1
                continue
            if argument.startswith("--"):
                index += 1
                continue

            for option_index, option in enumerate(argument[1:], start=1):
                if option == "c":
                    return argument
                if option == "m":
                    return None
                if option in {"W", "X"}:
                    if option_index == len(argument) - 1:
                        index += 1
                    break
            index += 1
        return None

    for argument in arguments:
        if argument == "--":
            break
        normalized = argument.casefold()
        if family == "node" and (
            normalized
            in {
                "-e",
                "-p",
                "-r",
                "--eval",
                "--print",
                "--import",
                "--require",
                "--loader",
                "--experimental-loader",
            }
            or normalized.startswith(("-e", "-p", "-r"))
            or normalized.startswith(
                (
                    "--eval=",
                    "--print=",
                    "--import=",
                    "--require=",
                    "--loader=",
                    "--experimental-loader=",
                )
            )
        ):
            return argument
    return None
