from __future__ import annotations

from typing import Any

from dify_plugin import ToolProvider
from dify_plugin.errors.tool import ToolProviderCredentialValidationError

from utils.config import get_api_key


class AholoProvider(ToolProvider):
    def _validate_credentials(self, credentials: dict[str, Any]) -> None:
        try:
            get_api_key(credentials)
        except Exception as error:
            raise ToolProviderCredentialValidationError(str(error)) from error
