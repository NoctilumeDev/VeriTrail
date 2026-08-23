from __future__ import annotations

import unittest

from veritrail.markdown import markdown_code, markdown_json, markdown_text


class MarkdownTests(unittest.TestCase):
    def test_text_and_json_cannot_create_links_images_or_raw_html(self) -> None:
        payload = "safe` ![probe](https://attacker.invalid/pixel) <img src=x>\nnext"
        for rendered in (markdown_text(payload), markdown_json({"value": payload})):
            self.assertNotIn("![probe](", rendered)
            self.assertNotIn("<img", rendered)
            self.assertNotIn("\n", rendered)
            self.assertIn("\\!\\[probe\\]\\(", rendered)

    def test_inline_code_uses_a_delimiter_longer_than_imported_backticks(self) -> None:
        rendered = markdown_code("before``after ![probe](https://attacker.invalid)")
        self.assertTrue(rendered.startswith("```") and rendered.endswith("```"))
        self.assertEqual(2, rendered.count("```"))

    def test_text_neutralizes_gfm_bare_url_and_email_autolinks(self) -> None:
        rendered = markdown_text(
            "HTTPS://example.invalid/path www.example.invalid user+tag@example.invalid"
        )

        self.assertNotIn("HTTPS://", rendered)
        self.assertNotIn("www\\.example", rendered)
        self.assertNotIn("user\\+tag@", rendered)
        self.assertEqual(3, rendered.count("\u2060"))

    def test_text_preserves_ordinary_non_link_content(self) -> None:
        self.assertEqual("普通文本 123 / local:path", markdown_text("普通文本 123 / local:path"))


if __name__ == "__main__":
    unittest.main()
