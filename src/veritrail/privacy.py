from __future__ import annotations

import re
from typing import Any

SENSITIVE_KEYS = {
    "authorization",
    "cookie",
    "set-cookie",
    "password",
    "passwd",
    "secret",
    "client-secret",
    "api-key",
    "apikey",
    "access-token",
    "refresh-token",
    "private-key",
    "connection-string",
    "username",
    "user-name",
    "account",
    "account-name",
    "hostname",
    "host-name",
    "computer-name",
    "session",
    "session-id",
    "sid",
    "credential",
    "auth",
}
KEY_NORMALIZER = re.compile(r"[_\s]+")
BEARER_PATTERN = re.compile(r"(?i)\bBearer\s+[A-Za-z0-9._~+/=-]+")
TOKEN_PATTERN = re.compile(r"\b(?:gh[opsu]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,})\b")
GENERIC_API_TOKEN_PATTERN = re.compile(r"\b(?:sk-[A-Za-z0-9_-]{20,}|AKIA[0-9A-Z]{16})\b")
CREDENTIAL_ASSIGNMENT_PATTERN = re.compile(
    r"(?i)\b(password|passwd|token|secret|api[_-]?key|session(?:[_-]?id)?|sid|credential|auth|cookie)\s*[:=]\s*(?!\[REDACTED\])[^\s,;]+"
)
BASIC_AUTH_HEADER_PATTERN = re.compile(
    r"(?im)^(\s*(?:proxy-)?authorization\s*:\s*)(?:basic|digest|ntlm|negotiate)?\s*[^\r\n]+"
)
COOKIE_HEADER_PATTERN = re.compile(r"(?im)^(\s*(?:set-cookie|cookie)\s*:\s*)[^\r\n]+")
BASIC_AUTH_URL_PATTERN = re.compile(r"(?i)([a-z][a-z0-9+.-]*://)[^/@\s:]+:[^/@\s]+@")
WINDOWS_USER_PATTERN = re.compile(r"(?i)\b[A-Z]:[\\/]Users[\\/][^\\/\s]+")
POSIX_USER_PATTERN = re.compile(r"/(?:Users|home)/[^/\s]+")
EMAIL_PATTERN = re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.IGNORECASE)
IPV4_PATTERN = re.compile(
    r"(?<![\d.])(?!127\.0\.0\.1(?![\d.]))(?:\d{1,3}\.){3}\d{1,3}(?![\d.])"
)
PEM_PATTERN = re.compile(
    r"-----BEGIN [A-Z ]*PRIVATE KEY-----.*?-----END [A-Z ]*PRIVATE KEY-----",
    re.DOTALL,
)


def _normalized_key(key: str) -> str:
    return KEY_NORMALIZER.sub("-", key.strip().lower())


def _is_sensitive_key(key: str) -> bool:
    normalized = _normalized_key(key)
    return (
        normalized in SENSITIVE_KEYS
        or normalized.endswith("-token")
        or normalized.endswith("-secret")
        or normalized.endswith("-password")
        or normalized.endswith("-private-key")
        or normalized.endswith("-api-key")
        or normalized.endswith("-authorization")
        or normalized.endswith("-auth-token")
    )


def redact_string(value: str) -> tuple[str, int]:
    result = value
    replacements = 0
    for pattern, replacement in (
        (PEM_PATTERN, "[REDACTED_PRIVATE_KEY]"),
        (BEARER_PATTERN, "Bearer [REDACTED]"),
        (TOKEN_PATTERN, "[REDACTED_TOKEN]"),
        (GENERIC_API_TOKEN_PATTERN, "[REDACTED_TOKEN]"),
        (BASIC_AUTH_HEADER_PATTERN, r"\1[REDACTED]"),
        (COOKIE_HEADER_PATTERN, r"\1[REDACTED]"),
        (CREDENTIAL_ASSIGNMENT_PATTERN, r"\1=[REDACTED]"),
        (BASIC_AUTH_URL_PATTERN, r"\1[REDACTED]@"),
        (WINDOWS_USER_PATTERN, "<USER_HOME>"),
        (POSIX_USER_PATTERN, "<USER_HOME>"),
        (EMAIL_PATTERN, "[REDACTED_EMAIL]"),
        (IPV4_PATTERN, "[REDACTED_IP]"),
    ):
        result, count = pattern.subn(replacement, result)
        replacements += count
    return result, replacements


def redact_value(value: Any) -> tuple[Any, int]:
    if isinstance(value, dict):
        redacted: dict[str, Any] = {}
        count = 0
        semantic_header_is_sensitive = any(
            _is_sensitive_key(item)
            for key, item in value.items()
            if _normalized_key(str(key)) in {"name", "header", "header-name"}
            and isinstance(item, str)
        )
        for key, item in value.items():
            normalized_key = _normalized_key(str(key))
            if _is_sensitive_key(str(key)) or (
                semantic_header_is_sensitive and normalized_key in {"value", "values"}
            ):
                redacted[str(key)] = "[REDACTED]"
                count += 1
            else:
                redacted_item, item_count = redact_value(item)
                redacted[str(key)] = redacted_item
                count += item_count
        return redacted, count
    if isinstance(value, list):
        redacted_items: list[Any] = []
        count = 0
        for item in value:
            redacted_item, item_count = redact_value(item)
            redacted_items.append(redacted_item)
            count += item_count
        return redacted_items, count
    if isinstance(value, str):
        return redact_string(value)
    return value, 0
