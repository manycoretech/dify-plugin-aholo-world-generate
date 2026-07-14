from __future__ import annotations

from typing import Any, Mapping, Optional

from manycore.aholo_sdk_asset import create_asset_client
from manycore.aholo_sdk_world import create_world_client

from utils.config import build_sdk_config, clean_string, normalize_region
from utils.errors import PluginInputError
from utils.file_input import extract_uploaded_image


def validate_generation_inputs(prompt: str, image_file: Any) -> None:
    if not prompt and not image_file:
        raise PluginInputError("Please provide at least one of prompt or image_file.")


def create_generation(
    *,
    credentials: Mapping[str, Any],
    region: Any,
    prompt: Any = None,
    image_file: Any = None,
    name: Any = None,
) -> dict[str, Any]:
    normalized_region = normalize_region(region)
    prompt_text = clean_string(prompt)
    name_text = clean_string(name)
    validate_generation_inputs(prompt_text, image_file)

    config = build_sdk_config(credentials, normalized_region)
    reference_image_url = ""
    if image_file:
        uploaded_image = extract_uploaded_image(image_file)
        upload_result = create_asset_client(config).upload_bytes(
            uploaded_image.data,
            filename=uploaded_image.filename,
        )
        reference_image_url = upload_result.url

    resources = [{"url": reference_image_url, "type": "image"}] if reference_image_url else None
    operation = create_world_client(config).generations.create(
        prompt=prompt_text or None,
        resources=resources,
        name=name_text or None,
        x_source="dify-plugin-aholo-world-generate",
    )
    world_id = clean_string(operation.get("worldId"))
    if not world_id:
        raise PluginInputError("Aholo response is missing worldId.")

    return {
        "world_id": world_id,
        "status": clean_string(operation.get("status")) or "PENDING",
        "reference_image_url": reference_image_url or "",
    }


def retrieve_generation(
    *,
    credentials: Mapping[str, Any],
    region: Any,
    world_id: Any,
) -> dict[str, Any]:
    world_id_text = clean_string(world_id)
    if not world_id_text:
        raise PluginInputError("world_id is required.")

    config = build_sdk_config(credentials, normalize_region(region))
    detail = create_world_client(config).retrieve(
        world_id_text,
        x_source="dify-plugin-aholo-world-generate",
    )
    normalized = normalize_world_detail(detail, fallback_world_id=world_id_text)
    validate_succeeded_assets(normalized)
    return normalized


def normalize_world_detail(detail: Mapping[str, Any], *, fallback_world_id: Optional[str] = None) -> dict[str, Any]:
    assets = _mapping(detail.get("assets"))
    splats = _mapping(assets.get("splats"))
    splat_urls = _mapping(splats.get("urls"))
    imagery = _mapping(assets.get("imagery"))
    semantics = _mapping(assets.get("semanticsMetadata"))

    return {
        "world_id": clean_string(detail.get("worldId")) or clean_string(fallback_world_id),
        "status": clean_string(detail.get("status")),
        "progress": _number(detail.get("progress")),
        "pano_url": clean_string(imagery.get("panoUrl")),
        "spz_url": clean_string(splat_urls.get("spzPath")),
        "ply_url": clean_string(splat_urls.get("plyPath")),
        "lod_meta_url": clean_string(splat_urls.get("lodMetaPath")),
        "up_axis": clean_string(semantics.get("upAxis")),
        "name": clean_string(detail.get("name")),
        "cover": clean_string(detail.get("cover")),
        "scene": clean_string(detail.get("scene")),
        "create_time": _integer(detail.get("createTime")),
        "update_time": _integer(detail.get("updateTime")),
    }


def format_detail_summary(detail: Mapping[str, Any]) -> str:
    urls = [
        label
        for label, value in (
            ("pano_url", detail.get("pano_url")),
            ("spz_url", detail.get("spz_url")),
            ("ply_url", detail.get("ply_url")),
            ("lod_meta_url", detail.get("lod_meta_url")),
        )
        if value
    ]
    available = ", ".join(urls) if urls else "no asset URLs yet"
    return (
        f"Aholo world {detail.get('world_id')} status={detail.get('status') or 'UNKNOWN'} "
        f"progress={detail.get('progress', 0)}; available: {available}."
    )


def validate_succeeded_assets(detail: Mapping[str, Any]) -> None:
    if detail.get("status") != "SUCCEEDED":
        return
    missing = [
        field
        for field in ("pano_url", "spz_url", "ply_url", "up_axis")
        if not clean_string(detail.get(field))
    ]
    if missing:
        raise PluginInputError(
            "Aholo world succeeded but required assets are missing: " + ", ".join(missing) + "."
        )


def _mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _number(value: Any) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def _integer(value: Any) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0
