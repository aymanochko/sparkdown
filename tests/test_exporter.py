"""
Unit tests for the Exporter module
"""

import unittest
import tempfile
import os
import sys
import json

# Add parent directory and src to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src'))

from exporter import Exporter, EXPORT_FORMATS
from renderer import MarkdownRenderer


class TestExporter(unittest.TestCase):
    """Test cases for Exporter class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.renderer = MarkdownRenderer()
        self.exporter = Exporter(self.renderer)
        self.temp_dir = tempfile.mkdtemp()
        self.test_content = "# Test Document\n\nThis is a **test** content."
    
    def tearDown(self):
        """Clean up test fixtures"""
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_exporter_initialization(self):
        """Test that Exporter initializes correctly"""
        self.assertIsNotNone(self.exporter)
        self.assertIsNotNone(self.exporter.renderer)
    
    def test_export_formats_list(self):
        """Test that EXPORT_FORMATS is defined"""
        self.assertIsInstance(EXPORT_FORMATS, list)
        self.assertGreater(len(EXPORT_FORMATS), 0)
    
    def test_export_formats_contain_expected_formats(self):
        """Test that EXPORT_FORMATS contains expected formats"""
        format_names = [fmt[1] for fmt in EXPORT_FORMATS]
        
        # Check for some expected formats
        expected = ['html', 'pdf', 'docx', 'txt', 'json']
        for fmt in expected:
            self.assertIn(fmt, format_names)
    
    def test_export_to_html(self):
        """Test exporting to HTML format"""
        output_path = os.path.join(self.temp_dir, 'test.html')
        result = self.exporter.export(self.test_content, output_path, 'html')
        
        self.assertTrue(result)
        self.assertTrue(os.path.exists(output_path))
        
        # Check content
        with open(output_path, 'r', encoding='utf-8') as f:
            content = f.read()
        self.assertIn("<html", content)
        # The markdown is rendered to HTML, so we check for h1 tag
        self.assertIn("<h1", content)
    
    def test_export_to_txt(self):
        """Test exporting to plain text format"""
        output_path = os.path.join(self.temp_dir, 'test.txt')
        result = self.exporter.export(self.test_content, output_path, 'txt')
        
        self.assertTrue(result)
        self.assertTrue(os.path.exists(output_path))
        
        # Check content
        with open(output_path, 'r', encoding='utf-8') as f:
            content = f.read()
        self.assertIn("Test Document", content)
        self.assertIn("test", content)
    
    def test_export_to_json(self):
        """Test exporting to JSON format"""
        output_path = os.path.join(self.temp_dir, 'test.json')
        result = self.exporter.export(self.test_content, output_path, 'json')
        
        self.assertTrue(result)
        self.assertTrue(os.path.exists(output_path))
        
        # Check content
        with open(output_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        self.assertIsInstance(data, dict)
        self.assertIn("content", data)
    
    def test_export_unsupported_format(self):
        """Test exporting to unsupported format raises ValueError"""
        output_path = os.path.join(self.temp_dir, 'test.xyz')
        
        with self.assertRaises(ValueError) as context:
            self.exporter.export(self.test_content, output_path, 'xyz')
        
        self.assertIn("Unsupported export format", str(context.exception))
    
    def test_ensure_extension(self):
        """Test that _ensure_extension adds extension if missing"""
        result = self.exporter._ensure_extension('test', '.html')
        self.assertEqual(result, 'test.html')
    
    def test_ensure_extension_already_has_extension(self):
        """Test that _ensure_extension keeps existing extension"""
        result = self.exporter._ensure_extension('test.html', '.html')
        self.assertEqual(result, 'test.html')
    
    def test_export_case_insensitive(self):
        """Test that export is case insensitive"""
        output_path = os.path.join(self.temp_dir, 'test.html')
        
        # Test with uppercase
        result = self.exporter.export(self.test_content, output_path, 'HTML')
        self.assertTrue(result)


class TestExporterFormats(unittest.TestCase):
    """Test cases for individual export formats"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.renderer = MarkdownRenderer()
        self.exporter = Exporter(self.renderer)
        self.temp_dir = tempfile.mkdtemp()
        self.test_content = "# Test\n\nHello world"
    
    def tearDown(self):
        """Clean up test fixtures"""
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_export_to_xml(self):
        """Test exporting to XML format"""
        output_path = os.path.join(self.temp_dir, 'test.xml')
        result = self.exporter.export(self.test_content, output_path, 'xml')
        
        self.assertTrue(result)
        self.assertTrue(os.path.exists(output_path))
        
        with open(output_path, 'r', encoding='utf-8') as f:
            content = f.read()
        self.assertIn('<?xml', content)
    
    def test_export_to_yaml(self):
        """Test exporting to YAML format"""
        output_path = os.path.join(self.temp_dir, 'test.yaml')
        result = self.exporter.export(self.test_content, output_path, 'yaml')
        
        self.assertTrue(result)
        self.assertTrue(os.path.exists(output_path))
    
    def test_export_to_csv(self):
        """Test exporting to CSV format"""
        output_path = os.path.join(self.temp_dir, 'test.csv')
        result = self.exporter.export(self.test_content, output_path, 'csv')
        
        self.assertTrue(result)
        self.assertTrue(os.path.exists(output_path))
    
    def test_export_to_latex(self):
        """Test exporting to LaTeX format - requires pandoc"""
        output_path = os.path.join(self.temp_dir, 'test.tex')
        try:
            result = self.exporter.export(self.test_content, output_path, 'latex')
            self.assertTrue(result)
            self.assertTrue(os.path.exists(output_path))
        except ImportError as e:
            self.skipTest(str(e))
    
    def test_export_to_mediawiki(self):
        """Test exporting to MediaWiki format - requires pandoc"""
        output_path = os.path.join(self.temp_dir, 'test.wiki')
        try:
            result = self.exporter.export(self.test_content, output_path, 'mediawiki')
            self.assertTrue(result)
            self.assertTrue(os.path.exists(output_path))
        except ImportError as e:
            self.skipTest(str(e))
    
    def test_export_to_rst(self):
        """Test exporting to reStructuredText format - requires pandoc"""
        output_path = os.path.join(self.temp_dir, 'test.rst')
        try:
            result = self.exporter.export(self.test_content, output_path, 'rst')
            self.assertTrue(result)
            self.assertTrue(os.path.exists(output_path))
        except ImportError as e:
            self.skipTest(str(e))


class TestExporterIntegration(unittest.TestCase):
    """Integration tests for the Exporter"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.renderer = MarkdownRenderer()
        self.exporter = Exporter(self.renderer)
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Clean up test fixtures"""
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_export_multiple_formats(self):
        """Test exporting to multiple formats"""
        content = "# Test Document\n\nSome content here."
        formats = ['html', 'txt', 'json', 'xml']
        
        for fmt in formats:
            output_path = os.path.join(self.temp_dir, f'test.{fmt}')
            result = self.exporter.export(content, output_path, fmt)
            self.assertTrue(result, f"Failed to export to {fmt}")
            self.assertTrue(os.path.exists(output_path))
    
    def test_export_with_complex_markdown(self):
        """Test exporting complex markdown content"""
        content = """# Title

## Section 1

- Item 1
- Item 2

## Section 2

| A | B |
|---|---|
| 1 | 2 |

```python
x = 1
```
"""
        output_path = os.path.join(self.temp_dir, 'complex.html')
        result = self.exporter.export(content, output_path, 'html')
        
        self.assertTrue(result)
        
        with open(output_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Verify some elements are present
        self.assertIn("<h1", html_content)
        self.assertIn("<ul>", html_content)
        self.assertIn("<table>", html_content)


if __name__ == '__main__':
    unittest.main()
