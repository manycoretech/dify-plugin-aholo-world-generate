from __future__ import annotations

from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from utils.aholo_client import format_detail_summary, retrieve_generation
from utils.errors import user_safe_error


DETAIL_VARIABLES = (
    "world_id",
    "status",
    "progress",
    "pano_url",
    "spz_url",
    "ply_url",
    "lod_meta_url",
    "up_axis",
    "name",
    "cover",
    "scene",
    "create_time",
    "update_time",
)


class GetWorldGenerationTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        try:
            detail = retrieve_generation(
                credentials=self.runtime.credentials,
                region=tool_parameters.get("region"),
                world_id=tool_parameters.get("world_id"),
            )
        except Exception as error:
            raise ValueError(user_safe_error(error, context="Get world generation")) from error

        for variable_name in DETAIL_VARIABLES:
            yield self.create_variable_message(variable_name, detail[variable_name])
        yield self.create_json_message(detail)
        yield self.create_text_message(format_detail_summary(detail))
