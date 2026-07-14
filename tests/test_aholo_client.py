from __future__ import annotations

from types import SimpleNamespace

import pytest

from manycore.aholo_sdk_core import AholoError

from utils.aholo_client import (
    create_generation,
    normalize_world_detail,
    validate_generation_inputs,
    validate_succeeded_assets,
)
from utils.errors import PluginInputError, user_safe_error
from utils.file_input import extract_uploaded_image


PNG_BYTES = b"\x89PNG\r\n\x1a\nimage-bytes"


class FakeAssetClient:
    def __init__(self) -> None:
        self.uploads = []

    def upload_bytes(self, data: bytes, *, filename: str):
        self.uploads.append((data, filename))
        return SimpleNamespace(url="https://assets.example/uploaded.png")


class FakeGenerations:
    def __init__(self) -> None:
        self.calls = []

    def create(self, **kwargs):
        self.calls.append(kwargs)
        return {"worldId": "world_123"}


class FakeWorldClient:
    def __init__(self) -> None:
        self.generations = FakeGenerations()


def test_validate_generation_inputs_requires_prompt_or_image() -> None:
    with pytest.raises(PluginInputError, match="at least one"):
        validate_generation_inputs("", None)


def test_extract_uploaded_image_reads_dify_file_object() -> None:
    file_obj = SimpleNamespace(filename="room.PNG", blob=PNG_BYTES, mime_type="image/png")

    uploaded = extract_uploaded_image(file_obj)

    assert uploaded.filename == "room.PNG"
    assert uploaded.data == PNG_BYTES
    assert uploaded.mime_type == "image/png"


def test_extract_uploaded_image_rejects_non_image_extension() -> None:
    file_obj = SimpleNamespace(filename="room.txt", blob=PNG_BYTES, mime_type="text/plain")

    with pytest.raises(PluginInputError, match="Unsupported image_file extension"):
        extract_uploaded_image(file_obj)


def test_extract_uploaded_image_rejects_fake_image_content() -> None:
    file_obj = SimpleNamespace(filename="room.png", blob=b"not-a-png", mime_type="image/png")

    with pytest.raises(PluginInputError, match="content does not match"):
        extract_uploaded_image(file_obj)


def test_create_generation_uploads_file_then_submits_world(monkeypatch: pytest.MonkeyPatch) -> None:
    fake_asset = FakeAssetClient()
    fake_world = FakeWorldClient()
    monkeypatch.setattr("utils.aholo_client.create_asset_client", lambda config: fake_asset)
    monkeypatch.setattr("utils.aholo_client.create_world_client", lambda config: fake_world)
    file_obj = SimpleNamespace(filename="room.png", blob=PNG_BYTES, mime_type="image/png")

    result = create_generation(
        credentials={"api_key": "test-key"},
        region="cn",
        prompt="modern living room",
        image_file=file_obj,
        name="Demo",
    )

    assert fake_asset.uploads == [(PNG_BYTES, "room.png")]
    assert fake_world.generations.calls == [
        {
            "prompt": "modern living room",
            "resources": [{"url": "https://assets.example/uploaded.png", "type": "image"}],
            "name": "Demo",
            "x_source": "dify-plugin-aholo-world-generate",
        }
    ]
    assert result == {
        "world_id": "world_123",
        "status": "PENDING",
        "reference_image_url": "https://assets.example/uploaded.png",
    }


def test_normalize_world_detail_flattens_asset_fields() -> None:
    detail = {
        "worldId": "world_123",
        "status": "SUCCEEDED",
        "progress": 100,
        "name": "Demo",
        "cover": "https://example.com/cover.png",
        "scene": "space",
        "createTime": 1710000000,
        "updateTime": 1710000300,
        "assets": {
            "imagery": {"panoUrl": "https://example.com/pano.jpg"},
            "splats": {
                "urls": {
                    "spzPath": "https://example.com/model.spz",
                    "plyPath": "https://example.com/model.ply",
                    "lodMetaPath": "https://example.com/lod.json",
                }
            },
            "semanticsMetadata": {"upAxis": "Y"},
        },
    }

    normalized = normalize_world_detail(detail)

    assert normalized["world_id"] == "world_123"
    assert normalized["pano_url"] == "https://example.com/pano.jpg"
    assert normalized["spz_url"] == "https://example.com/model.spz"
    assert normalized["ply_url"] == "https://example.com/model.ply"
    assert normalized["lod_meta_url"] == "https://example.com/lod.json"
    assert normalized["up_axis"] == "Y"
    assert normalized["create_time"] == 1710000000


def test_validate_succeeded_assets_requires_success_assets() -> None:
    with pytest.raises(PluginInputError, match="required assets are missing"):
        validate_succeeded_assets(
            {
                "world_id": "world_123",
                "status": "SUCCEEDED",
                "pano_url": "",
                "spz_url": "https://example.com/model.spz",
                "ply_url": "https://example.com/model.ply",
                "up_axis": "Y",
            }
        )


def test_user_safe_error_does_not_expose_raw_aholo_error_message() -> None:
    error = AholoError("secret header value leaked", status_code=500, status="INTERNAL")

    message = user_safe_error(error, context="Create world generation")

    assert "secret header value leaked" not in message
    assert "status_code=500" in message
