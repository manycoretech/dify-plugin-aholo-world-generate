from __future__ import annotations

from typing import Any, Mapping

from manycore.aholo_sdk_core import AholoClientConfig

from utils.errors import PluginInputError


SUPPORTED_REGIONS = frozenset({"cn", "com"})
DEFAULT_REGION = "cn"
PLUGIN_USER_AGENT = "dify-plugin-aholo-world-generate/1.1.0"


def clean_string(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def get_api_key(credentials: Mapping[str, Any]) -> str:
    api_key = clean_string(credentials.get("api_key"))
    if not api_key:
        raise PluginInputError("Missing Aholo API key. Please configure the provider credentials.")
    return api_key


def normalize_region(value: Any) -> str:
    region = clean_string(value) or DEFAULT_REGION
    if region not in SUPPORTED_REGIONS:
        allowed = ", ".join(sorted(SUPPORTED_REGIONS))
        raise PluginInputError(f"Invalid region '{region}'. Allowed values are: {allowed}.")
    return region


def build_sdk_config(credentials: Mapping[str, Any], region: str) -> AholoClientConfig:
    return AholoClientConfig(
        api_key=get_api_key(credentials),
        region=normalize_region(region),
        timeout_ms=60_000,
        user_agent=PLUGIN_USER_AGENT,
    )
