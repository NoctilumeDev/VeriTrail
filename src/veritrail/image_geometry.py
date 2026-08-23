from __future__ import annotations

import struct
import zlib
from dataclasses import dataclass


MAX_IMAGE_WIDTH = 8192
MAX_IMAGE_HEIGHT = 8192
MAX_IMAGE_PIXELS = 16_777_216
MAX_IMAGE_DECODED_BYTES = 64 * 1024 * 1024

_PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
_PNG_BIT_DEPTHS = {
    0: {1, 2, 4, 8, 16},
    2: {8, 16},
    3: {1, 2, 4, 8},
    4: {8, 16},
    6: {8, 16},
}
_JPEG_SOF_MARKERS = {
    0xC0,
    0xC1,
    0xC2,
    0xC3,
    0xC5,
    0xC6,
    0xC7,
    0xC9,
    0xCA,
    0xCB,
    0xCD,
    0xCE,
    0xCF,
}


class ImageGeometryError(ValueError):
    """Raised when compressed image metadata is malformed or exceeds the frozen budget."""


@dataclass(frozen=True)
class ImageGeometry:
    width: int
    height: int
    pixels: int
    decoded_bytes: int


def _bounded_geometry(width: int, height: int) -> ImageGeometry:
    if width <= 0 or height <= 0:
        raise ImageGeometryError("image dimensions must be positive")
    if width > MAX_IMAGE_WIDTH or height > MAX_IMAGE_HEIGHT:
        raise ImageGeometryError(
            f"image dimensions exceed {MAX_IMAGE_WIDTH}x{MAX_IMAGE_HEIGHT}"
        )
    pixels = width * height
    decoded_bytes = pixels * 4
    if pixels > MAX_IMAGE_PIXELS:
        raise ImageGeometryError(f"image pixel count exceeds {MAX_IMAGE_PIXELS}")
    if decoded_bytes > MAX_IMAGE_DECODED_BYTES:
        raise ImageGeometryError(
            f"estimated decoded image size exceeds {MAX_IMAGE_DECODED_BYTES} bytes"
        )
    return ImageGeometry(
        width=width,
        height=height,
        pixels=pixels,
        decoded_bytes=decoded_bytes,
    )


def _parse_png(content: bytes) -> ImageGeometry:
    if not content.startswith(_PNG_SIGNATURE):
        raise ImageGeometryError("image/png attachment is missing the PNG signature")

    offset = len(_PNG_SIGNATURE)
    geometry: ImageGeometry | None = None
    saw_idat = False
    saw_iend = False
    chunk_index = 0
    while offset < len(content):
        if len(content) - offset < 12:
            raise ImageGeometryError("PNG chunk header is truncated")
        length = struct.unpack_from(">I", content, offset)[0]
        chunk_type = content[offset + 4 : offset + 8]
        chunk_end = offset + 12 + length
        if chunk_end > len(content):
            raise ImageGeometryError("PNG chunk payload is truncated")
        if len(chunk_type) != 4 or any(
            not (65 <= byte <= 90 or 97 <= byte <= 122) for byte in chunk_type
        ):
            raise ImageGeometryError("PNG chunk type is malformed")
        payload = content[offset + 8 : offset + 8 + length]
        expected_crc = struct.unpack_from(">I", content, offset + 8 + length)[0]
        actual_crc = zlib.crc32(chunk_type + payload) & 0xFFFFFFFF
        if actual_crc != expected_crc:
            raise ImageGeometryError("PNG chunk CRC is invalid")

        if chunk_index == 0:
            if chunk_type != b"IHDR" or length != 13:
                raise ImageGeometryError("PNG must begin with a 13-byte IHDR chunk")
            width, height, bit_depth, color_type, compression, filtering, interlace = (
                struct.unpack(">IIBBBBB", payload)
            )
            if bit_depth not in _PNG_BIT_DEPTHS.get(color_type, set()):
                raise ImageGeometryError("PNG IHDR bit depth or color type is invalid")
            if compression != 0 or filtering != 0 or interlace not in {0, 1}:
                raise ImageGeometryError("PNG IHDR compression, filter, or interlace is invalid")
            geometry = _bounded_geometry(width, height)
        elif chunk_type == b"IHDR":
            raise ImageGeometryError("PNG contains more than one IHDR chunk")

        if chunk_type == b"IDAT":
            saw_idat = True
        if chunk_type == b"IEND":
            if length != 0 or chunk_end != len(content):
                raise ImageGeometryError("PNG IEND chunk is malformed or not final")
            saw_iend = True
            break

        offset = chunk_end
        chunk_index += 1

    if geometry is None or not saw_idat or not saw_iend:
        raise ImageGeometryError("PNG is missing required IHDR, IDAT, or IEND chunks")
    return geometry


def _parse_jpeg(content: bytes) -> ImageGeometry:
    if len(content) < 4 or content[:2] != b"\xff\xd8":
        raise ImageGeometryError("image/jpeg attachment is missing the JPEG SOI marker")

    offset = 2
    geometry: ImageGeometry | None = None
    in_scan = False
    while offset < len(content):
        if in_scan:
            marker_start = content.find(b"\xff", offset)
            if marker_start < 0 or marker_start + 1 >= len(content):
                raise ImageGeometryError("JPEG entropy stream is truncated")
            marker = content[marker_start + 1]
            if marker == 0x00:
                offset = marker_start + 2
                continue
            if marker == 0xFF:
                offset = marker_start + 1
                continue
            if 0xD0 <= marker <= 0xD7:
                offset = marker_start + 2
                continue
            offset = marker_start
            in_scan = False
            continue

        if content[offset] != 0xFF:
            raise ImageGeometryError("JPEG marker prefix is malformed")
        while offset < len(content) and content[offset] == 0xFF:
            offset += 1
        if offset >= len(content):
            raise ImageGeometryError("JPEG marker is truncated")
        marker = content[offset]
        offset += 1
        if marker == 0x00:
            raise ImageGeometryError("JPEG contains an escaped byte outside scan data")
        if marker == 0xD9:
            if geometry is None or offset != len(content):
                raise ImageGeometryError("JPEG EOI marker is missing metadata or is not final")
            return geometry
        if marker == 0xD8:
            raise ImageGeometryError("JPEG contains an unexpected SOI marker")
        if marker == 0x01 or 0xD0 <= marker <= 0xD7:
            continue
        if len(content) - offset < 2:
            raise ImageGeometryError("JPEG segment length is truncated")
        segment_length = struct.unpack_from(">H", content, offset)[0]
        if segment_length < 2 or offset + segment_length > len(content):
            raise ImageGeometryError("JPEG segment is malformed or truncated")
        payload_start = offset + 2
        payload_end = offset + segment_length

        if marker in _JPEG_SOF_MARKERS:
            if segment_length < 8:
                raise ImageGeometryError("JPEG SOF segment is too short")
            precision = content[payload_start]
            height, width = struct.unpack_from(">HH", content, payload_start + 1)
            components = content[payload_start + 5]
            if precision not in {8, 12} or components == 0:
                raise ImageGeometryError("JPEG SOF precision or component count is invalid")
            if segment_length != 8 + 3 * components:
                raise ImageGeometryError("JPEG SOF component metadata is malformed")
            next_geometry = _bounded_geometry(width, height)
            if geometry is not None and geometry != next_geometry:
                raise ImageGeometryError("JPEG contains conflicting SOF dimensions")
            geometry = next_geometry

        offset = payload_end
        if marker == 0xDA:
            if geometry is None:
                raise ImageGeometryError("JPEG scan begins before SOF dimensions")
            in_scan = True

    raise ImageGeometryError("JPEG is missing a final EOI marker")


def parse_image_geometry(content: bytes, media_type: str) -> ImageGeometry:
    if not isinstance(content, bytes):
        raise ImageGeometryError("image content must be bytes")
    if media_type == "image/png":
        return _parse_png(content)
    if media_type == "image/jpeg":
        return _parse_jpeg(content)
    raise ImageGeometryError(f"unsupported image media type: {media_type}")
