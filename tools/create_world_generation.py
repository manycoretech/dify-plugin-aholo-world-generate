from __future__ import annotations

from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from utils.aholo_client import create_generation
from utils.errors import user_safe_error


class CreateWorldGenerationTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        try:
            result = create_generation(
                credentials=self.runtime.credentials,
                region=tool_parameters.get("region"),
                prompt=tool_parameters.get("prompt"),
                image_file=tool_parameters.get("image_file"),
                name=tool_parameters.get("name"),
                cover=tool_parameters.get("cover"),
            )
        except Exception as error:
            raise ValueError(user_safe_error(error, context="Create world generation")) from error

        yield self.create_variable_message("world_id", result["world_id"])
        yield self.create_variable_message("status", result["status"])
        yield self.create_variable_message("reference_image_url", result["reference_image_url"])
        yield self.create_json_message(result)
        yield self.create_text_message(
            f"Aholo world generation submitted. world_id={result['world_id']} status={result['status']}."
        )
