from __future__ import annotations

import struct
import unittest
import zlib

from veritrail.errors import ValidationError
from veritrail.evidence import create_attachment
from veritrail.image_geometry import ImageGeometryError, parse_image_geometry


def _png_chunk(chunk_type: bytes, payload: bytes) -> bytes:
    crc = zlib.crc32(chunk_type + payload) & 0xFFFFFFFF
    return struct.pack(">I", len(payload)) + chunk_type + payload + struct.pack(">I", crc)


def _png(width: int, height: int) -> bytes:
    ihdr = struct.pack(">IIBBBBB", width, height, 8, 6, 0, 0, 0)
    return b"".join(
        (
            b"\x89PNG\r\n\x1a\n",
            _png_chunk(b"IHDR", ihdr),
            _png_chunk(b"IDAT", zlib.compress(b"\x00")),
            _png_chunk(b"IEND", b""),
        )
    )


def _jpeg(width: int, height: int) -> bytes:
    sof = bytes((8,)) + struct.pack(">HH", height, width) + bytes((1, 1, 0x11, 0))
    scan = bytes((1, 1, 0, 0, 63, 0))
    return b"".join(
        (
            b"\xff\xd8",
            b"\xff\xc0" + struct.pack(">H", len(sof) + 2) + sof,
            b"\xff\xda" + struct.pack(">H", len(scan) + 2) + scan,
            b"\x00\xff\xd9",
        )
    )


class ImageGeometryTests(unittest.TestCase):
    def test_accepts_bounded_png_and_jpeg_metadata(self) -> None:
        png = parse_image_geometry(_png(1920, 1080), "image/png")
        jpeg = parse_image_geometry(_jpeg(1280, 720), "image/jpeg")

        self.assertEqual((png.width, png.height, png.pixels), (1920, 1080, 2_073_600))
        self.assertEqual((jpeg.width, jpeg.height, jpeg.pixels), (1280, 720, 921_600))

    def test_rejects_images_over_frozen_geometry_or_decode_budget(self) -> None:
        cases = (
            (_png(8193, 1), "image/png"),
            (_png(4097, 4097), "image/png"),
            (_jpeg(8193, 1), "image/jpeg"),
        )
        for content, media_type in cases:
            with self.subTest(media_type=media_type, size=len(content)):
                with self.assertRaises(ImageGeometryError):
                    parse_image_geometry(content, media_type)

    def test_rejects_malformed_images_with_correct_signature(self) -> None:
        cases = (
            (b"\x89PNG\r\n\x1a\n", "image/png"),
            (_png(1, 1)[:-4], "image/png"),
            (b"\xff\xd8\xff\xd9", "image/jpeg"),
            (_jpeg(1, 1)[:-2], "image/jpeg"),
        )
        for content, media_type in cases:
            with self.subTest(media_type=media_type, size=len(content)):
                with self.assertRaises(ImageGeometryError):
                    parse_image_geometry(content, media_type)

    def test_attachment_creation_enforces_geometry_before_hashing(self) -> None:
        attachment = create_attachment(
            path="attachments/browser/desktop-step.png",
            content=_png(1440, 960),
            media_type="image/png",
            logical_name="desktop-step",
        )
        self.assertGreater(attachment.size, 0)

        with self.assertRaisesRegex(ValidationError, "dimensions exceed"):
            create_attachment(
                path="attachments/browser/oversized.png",
                content=_png(8193, 1),
                media_type="image/png",
                logical_name="oversized-image",
            )


if __name__ == "__main__":
    unittest.main()
