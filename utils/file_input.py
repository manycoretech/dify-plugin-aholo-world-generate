from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any

from utils.errors import PluginInputError


SUPPORTED_IMAGE_EXTENSIONS = frozenset({".jpg", ".jpeg", ".png", ".webp"})
SUPPORTED_IMAGE_MIME_TYPES = frozenset({"image/jpeg", "image/png", "image/webp"})
MAX_IMAGE_FILE_BYTES = 50 * 1024 * 1024


@dataclass(frozen=True)
class UploadedImage:
    filename: str
    data: bytes
    mime_type: str


def extract_uploaded_image(file_obj: Any) -> UploadedImage:
    filename = str(getattr(file_obj, "filename", "") or "reference-image").strip()
    data = getattr(file_obj, "blob", None)
    mime_type = str(getattr(file_obj, "mime_type", "") or "").strip().lower()

    if data is None:
        raise PluginInputError("image_file is invalid: missing file bytes.")
    if not isinstance(data, bytes):
        raise PluginInputError("image_file is invalid: file bytes must be a bytes object.")
    if not data:
        raise PluginInputError("image_file is invalid: file bytes are empty.")
    if len(data) > MAX_IMAGE_FILE_BYTES:
        raise PluginInputError("image_file is too large. Maximum supported size is 50 MiB.")

    extension = os.path.splitext(filename)[1].lower()
    if extension not in SUPPORTED_IMAGE_EXTENSIONS:
        allowed = ", ".join(sorted(SUPPORTED_IMAGE_EXTENSIONS))
        raise PluginInputError(f"Unsupported image_file extension '{extension or '<none>'}'. Allowed: {allowed}.")
    if mime_type and mime_type not in SUPPORTED_IMAGE_MIME_TYPES:
        allowed_mime_types = ", ".join(sorted(SUPPORTED_IMAGE_MIME_TYPES))
        raise PluginInputError(f"Unsupported image_file MIME type '{mime_type}'. Allowed: {allowed_mime_types}.")
    if not _looks_like_supported_image(data, extension):
        raise PluginInputError("image_file content does not match a supported image format.")

    return UploadedImage(filename=filename, data=data, mime_type=mime_type or "application/octet-stream")


def _looks_like_supported_image(data: bytes, extension: str) -> bool:
    if extension in {".jpg", ".jpeg"}:
        return data.startswith(b"\xff\xd8\xff")
    if extension == ".png":
        return data.startswith(b"\x89PNG\r\n\x1a\n")
    if extension == ".webp":
        return len(data) >= 12 and data[:4] == b"RIFF" and data[8:12] == b"WEBP"
    return False
