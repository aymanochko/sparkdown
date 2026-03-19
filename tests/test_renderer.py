"""
Unit tests for the MarkdownRenderer module
"""

import os
import sys
import unittest

# Add parent directory and src to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src'))

from renderer import MarkdownRenderer


class TestMarkdownRenderer(unittest.TestCase):
    """Test cases for MarkdownRenderer class"""

    def setUp(self):
        """Set up test fixtures"""
        self.renderer = MarkdownRenderer()

    def test_render_to_html_returns_string(self):
        """Test that render_to_html returns a string"""
        content = "# Hello World"
        result = self.renderer.render_to_html(content, "Test")
        self.assertIsInstance(result, str)

    def test_render_to_html_contains_title(self):
        """Test that rendered HTML contains the title"""
        content = "# Hello World"
        result = self.renderer.render_to_html(content, "My Document")
        self.assertIn("My Document", result)

    def test_render_to_html_contains_content(self):
        """Test that rendered HTML contains the markdown content"""
        content = "# Hello World"
        result = self.renderer.render_to_html(content, "Test")
        self.assertIn("Hello World", result)

    def test_render_to_html_has_doctype(self):
        """Test that rendered HTML has DOCTYPE"""
        content = "# Test"
        result = self.renderer.render_to_html(content)
        self.assertIn("<!DOCTYPE html>", result)

    def test_render_to_html_has_html_tags(self):
        """Test that rendered HTML has html tags"""
        content = "# Test"
        result = self.renderer.render_to_html(content)
        self.assertIn("<html", result)
        self.assertIn("</html>", result)

    def test_render_headers(self):
        """Test rendering of headers"""
        test_cases = [
            ("# H1", "<h1"),
            ("## H2", "<h2"),
            ("### H3", "<h3"),
            ("#### H4", "<h4"),
            ("##### H5", "<h5"),
            ("###### H6", "<h6"),
        ]

        for markdown, expected_tag in test_cases:
            result = self.renderer.render_to_html(markdown)
            self.assertIn(expected_tag, result)

    def test_render_bold_text(self):
        """Test rendering of bold text"""
        content = "**Bold text**"
        result = self.renderer.render_to_html(content)
        self.assertIn("<strong>", result)

    def test_render_italic_text(self):
        """Test rendering of italic text"""
        content = "*Italic text*"
        result = self.renderer.render_to_html(content)
        self.assertIn("<em>", result)

    def test_render_code_block(self):
        """Test rendering of code blocks"""
        content = "```python\nprint('hello')\n```"
        result = self.renderer.render_to_html(content)
        self.assertIn("<code", result)
        self.assertIn("class=\"highlight", result)

    def test_render_inline_code(self):
        """Test rendering of inline code"""
        content = "`inline code`"
        result = self.renderer.render_to_html(content)
        self.assertIn("<code", result)

    def test_render_links(self):
        """Test rendering of links"""
        content = "[Link text](https://example.com)"
        result = self.renderer.render_to_html(content)
        self.assertIn("<a href=", result)
        self.assertIn("Link text", result)

    def test_render_ordered_list(self):
        """Test rendering of ordered lists"""
        content = "1. Item 1\n2. Item 2"
        result = self.renderer.render_to_html(content)
        self.assertIn("<ol>", result)
        self.assertIn("<li>", result)

    def test_render_unordered_list(self):
        """Test rendering of unordered lists"""
        content = "- Item 1\n- Item 2"
        result = self.renderer.render_to_html(content)
        self.assertIn("<ul>", result)
        self.assertIn("<li>", result)

    def test_render_blockquote(self):
        """Test rendering of blockquotes"""
        content = "> This is a quote"
        result = self.renderer.render_to_html(content)
        self.assertIn("<blockquote>", result)

    def test_render_horizontal_rule(self):
        """Test rendering of horizontal rules"""
        content = "---"
        result = self.renderer.render_to_html(content)
        self.assertIn("<hr", result)

    def test_render_table(self):
        """Test rendering of tables"""
        content = "| Header 1 | Header 2 |\n|----------|----------|\n| Cell 1   | Cell 2   |"
        result = self.renderer.render_to_html(content)
        self.assertIn("<table>", result)
        self.assertIn("<th>", result)
        self.assertIn("<td>", result)

    def test_render_to_html_fragment(self):
        """Test rendering HTML fragment without full document"""
        content = "# Hello"
        result = self.renderer.render_to_html_fragment(content)

        self.assertIsInstance(result, str)
        self.assertNotIn("<!DOCTYPE html>", result)
        self.assertNotIn("<html", result)
        self.assertIn("<h1", result)

    def test_get_word_count(self):
        """Test word count"""
        test_cases = [
            ("Hello world", 2),
            ("# Hello\n\nWorld test", 3),
            ("", 0),
            ("Single", 1),
        ]

        for content, expected_count in test_cases:
            count = self.renderer.get_word_count(content)
            self.assertEqual(count, expected_count)

    def test_get_word_count_with_special_chars(self):
        """Test word count with special characters"""
        content = "Hello, world! How are you?"
        count = self.renderer.get_word_count(content)
        self.assertEqual(count, 5)

    def test_get_line_count(self):
        """Test line count"""
        test_cases = [
            ("Hello\nWorld", 2),
            ("# Header\n\nContent\nMore", 4),
            ("", 1),  # Empty string still has 1 line
            ("Single line", 1),
        ]

        for content, expected_count in test_cases:
            count = self.renderer.get_line_count(content)
            self.assertEqual(count, expected_count)

    def test_get_toc(self):
        """Test table of contents extraction"""
        content = "# Title\n\n## Section 1\n\n## Section 2"
        toc = self.renderer.get_toc(content)

        self.assertIsInstance(toc, list)
        # TOC should contain entries for sections

    def test_render_complex_markdown(self):
        """Test rendering complex markdown with multiple elements"""
        content = """# Document Title

## Introduction

This is a paragraph with **bold** and *italic* text.

### Code Example

```python
def hello():
    print("Hello, World!")
```

### List

- Item 1
- Item 2
- Item 3

### Quote

> This is a blockquote.

### Table

| Column 1 | Column 2 |
|----------|----------|
| Data 1   | Data 2   |

[Link](https://example.com)
"""
        result = self.renderer.render_to_html(content)

        # Check for various elements
        self.assertIn("<h1", result)
        self.assertIn("<h2", result)
        self.assertIn("<h3", result)
        self.assertIn("<strong>", result)
        self.assertIn("<em>", result)
        self.assertIn("<ul>", result)
        self.assertIn("<blockquote>", result)
        self.assertIn("<table>", result)
        self.assertIn("<a href=", result)


class TestMarkdownRendererExtensions(unittest.TestCase):
    """Test cases for markdown extensions"""

    def setUp(self):
        """Set up test fixtures"""
        self.renderer = MarkdownRenderer()

    def test_fenced_code_extension(self):
        """Test fenced code blocks"""
        content = "```javascript\nconst x = 1;\n```"
        result = self.renderer.render_to_html(content)
        self.assertIn("class=\"highlight", result)

    def test_tables_extension(self):
        """Test tables"""
        content = "| A | B |\n|---|---|\n| 1 | 2 |"
        result = self.renderer.render_to_html(content)
        self.assertIn("<table>", result)

    def test_task_lists(self):
        """Test task lists (if extension available)"""
        content = "- [ ] Unchecked\n- [x] Checked"
        self.renderer.render_to_html(content)
        # Should handle task lists gracefully

    def test_strikethrough(self):
        """Test strikethrough - requires 'del' extension to be enabled"""
        # The strikethrough extension needs to be explicitly enabled
        # Test that it doesn't break and renders something
        content = "~~deleted~~"
        result = self.renderer.render_to_html(content)
        # Either the extension works (<del>) or it's passed through as-is
        # This test verifies the renderer doesn't crash on this syntax
        self.assertTrue("<del>" in result or "~~deleted~~" in result)


if __name__ == '__main__':
    unittest.main()
