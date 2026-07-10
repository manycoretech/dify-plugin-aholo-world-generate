from __future__ import annotations

from manycore.aholo_sdk_core import AholoError, AuthenticationError, PollingTimeoutError, RateLimitError


class PluginInputError(ValueError):
    """Raised when a Dify tool input is invalid."""


def user_safe_error(error: Exception, *, context: str) -> str:
    if isinstance(error, PluginInputError):
        return str(error)
    if isinstance(error, AuthenticationError):
        return f"{context} failed: Aholo API key is invalid or not authorized for the selected region."
    if isinstance(error, RateLimitError):
        return f"{context} failed: Aholo API rate limit was reached. Please retry later."
    if isinstance(error, PollingTimeoutError):
        return f"{context} timed out after {error.timeout_ms} ms."
    if isinstance(error, AholoError):
        detail_parts = [error.__class__.__name__]
        if error.status_code:
            detail_parts.append(f"status_code={error.status_code}")
        if error.status:
            detail_parts.append(f"status={error.status}")
        if error.biz_code:
            detail_parts.append(f"biz_code={error.biz_code}")
        return f"{context} failed: {' '.join(detail_parts)}."
    return f"{context} failed unexpectedly. Please check the inputs and retry."
