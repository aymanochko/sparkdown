"""
SparkDown - Exporter Module
Handles exporting markdown to various formats
"""

import json
import csv
import io
import re
import os
import tempfile
import subprocess
from typing import List, Dict, Optional
from xml.etree.ElementTree import Element, SubElement, tostring
import yaml


class Exporter:
    """Exports markdown to various formats"""
    
    def __init__(self, renderer):
        """Initialize exporter with renderer"""
        self.renderer = renderer
    
    def export(self, markdown_content: str, output_path: str, format: str) -> bool:
        """Export markdown to specified format"""
        format_lower = format.lower()
        
        export_methods = {
            'html': self.export_to_html,
            'pdf': self.export_to_pdf,
            'docx': self.export_to_docx,
            'odt': self.export_to_odt,
            'rtf': self.export_to_rtf,
            'epub': self.export_to_epub,
            'txt': self.export_to_txt,
            'json': self.export_to_json,
            'xml': self.export_to_xml,
            'yaml': self.export_to_yaml,
            'csv': self.export_to_csv,
            'latex': self.export_to_latex,
            'mediawiki': self.export_to_mediawiki,
            'rst': self.export_to_rst,
        }
        
        if format_lower in export_methods:
            return export_methods[format_lower](markdown_content, output_path)
        else:
            raise ValueError(f"Unsupported export format: {format}")
    
    def _ensure_extension(self, path: str, extension: str) -> str:
        """Ensure file has the correct extension"""
        if not path.endswith(extension):
            path = path + extension
        return path
    
    def _run_pandoc(self, input_content: str, output_path: str, output_format: str) -> bool:
        """Run pandoc to convert markdown"""
        try:
            # Write content to temporary file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as tmp:
                tmp.write(input_content)
                tmp_path = tmp.name
            
            try:
                # Run pandoc
                result = subprocess.run(
                    ['pandoc', tmp_path, '-o', output_path, '-t', output_format],
                    capture_output=True,
                    text=True
                )
                
                if result.returncode != 0:
                    raise RuntimeError(f"Pandoc error: {result.stderr}")
                
                return True
            finally:
                if os.path.exists(tmp_path):
                    os.unlink(tmp_path)
                    
        except FileNotFoundError:
            raise ImportError("pypandoc is required for this export. Install with: pip install pypandoc")
    
    def export_to_html(self, markdown_content: str, output_path: str) -> bool:
        """Export to HTML format"""
        output_path = self._ensure_extension(output_path, '.html')
        
        html_content = self.renderer.render_to_html(markdown_content, "SparkDown Export")
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return True
    
    def export_to_pdf(self, markdown_content: str, output_path: str) -> bool:
        """Export to PDF format"""
        output_path = self._ensure_extension(output_path, '.pdf')
        return self.renderer.render_to_pdf(markdown_content, output_path)
    
    def export_to_docx(self, markdown_content: str, output_path: str) -> bool:
        """Export to DOCX format"""
        output_path = self._ensure_extension(output_path, '.docx')
        return self._run_pandoc(markdown_content, output_path, 'docx')
    
    def export_to_odt(self, markdown_content: str, output_path: str) -> bool:
        """Export to ODT format"""
        output_path = self._ensure_extension(output_path, '.odt')
        return self._run_pandoc(markdown_content, output_path, 'odt')
    
    def export_to_rtf(self, markdown_content: str, output_path: str) -> bool:
        """Export to RTF format"""
        output_path = self._ensure_extension(output_path, '.rtf')
        return self._run_pandoc(markdown_content, output_path, 'rtf')
    
    def export_to_epub(self, markdown_content: str, output_path: str) -> bool:
        """Export to EPUB format"""
        output_path = self._ensure_extension(output_path, '.epub')
        return self._run_pandoc(markdown_content, output_path, 'epub')
    
    def export_to_latex(self, markdown_content: str, output_path: str) -> bool:
        """Export to LaTeX format"""
        output_path = self._ensure_extension(output_path, '.tex')
        return self._run_pandoc(markdown_content, output_path, 'latex')
    
    def export_to_mediawiki(self, markdown_content: str, output_path: str) -> bool:
        """Export to MediaWiki format"""
        output_path = self._ensure_extension(output_path, '.wiki')
        return self._run_pandoc(markdown_content, output_path, 'mediawiki')
    
    def export_to_rst(self, markdown_content: str, output_path: str) -> bool:
        """Export to reStructuredText format"""
        output_path = self._ensure_extension(output_path, '.rst')
        return self._run_pandoc(markdown_content, output_path, 'rst')
    
    def export_to_txt(self, markdown_content: str, output_path: str) -> bool:
        """Export to plain text format"""
        output_path = self._ensure_extension(output_path, '.txt')
        
        # Extract plain text from markdown
        text = markdown_content
        
        # Remove code blocks
        text = re.sub(r'```[\s\S]*?```', '', text)
        
        # Remove inline code
        text = re.sub(r'`[^`]+`', '', text)
        
        # Remove images
        text = re.sub(r'!\[.*?\]\(.*?\)', '', text)
        
        # Remove links but keep text
        text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)
        
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', '', text)
        
        # Convert headers to uppercase
        text = re.sub(r'^######\s+(.+)$', r'\1', text, flags=re.MULTILINE)
        text = re.sub(r'^#####\s+(.+)$', r'\1', text, flags=re.MULTILINE)
        text = re.sub(r'^####\s+(.+)$', r'\1', text, flags=re.MULTILINE)
        text = re.sub(r'^###\s+(.+)$', r'\1', text, flags=re.MULTILINE)
        text = re.sub(r'^##\s+(.+)$', r'\1', text, flags=re.MULTILINE)
        text = re.sub(r'^#\s+(.+)$', r'\1', text, flags=re.MULTILINE)
        
        # Remove bold/italic markers
        text = re.sub(r'\*\*([^\*]+)\*\*', r'\1', text)
        text = re.sub(r'\*([^\*]+)\*', r'\1', text)
        text = re.sub(r'__([^_]+)__', r'\1', text)
        text = re.sub(r'_([^_]+)_', r'\1', text)
        
        # Remove blockquotes
        text = re.sub(r'^>\s+', '', text, flags=re.MULTILINE)
        
        # Remove horizontal rules
        text = re.sub(r'^[-*_]{3,}$', '', text, flags=re.MULTILINE)
        
        # Clean up extra whitespace
        text = re.sub(r'\n{3,}', '\n\n', text)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(text.strip())
        
        return True
    
    def export_to_json(self, markdown_content: str, output_path: str) -> bool:
        """Export to JSON format"""
        output_path = self._ensure_extension(output_path, '.json')
        
        # Parse markdown structure to JSON
        data = self._parse_markdown_to_json(markdown_content)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        return True
    
    def _parse_markdown_to_json(self, markdown_content: str) -> dict:
        """Parse markdown content to structured JSON"""
        lines = markdown_content.split('\n')
        blocks = []
        current_block = None
        
        for line in lines:
            # Check for headers
            header_match = re.match(r'^(#{1,6})\s+(.+)$', line)
            if header_match:
                if current_block:
                    blocks.append(current_block)
                blocks.append({
                    'type': 'header',
                    'level': len(header_match.group(1)),
                    'text': header_match.group(2)
                })
                current_block = None
                continue
            
            # Check for code blocks
            if line.startswith('```'):
                if current_block and current_block.get('type') == 'code':
                    blocks.append(current_block)
                    current_block = None
                else:
                    if current_block:
                        blocks.append(current_block)
                    current_block = {
                        'type': 'code',
                        'language': line[3:].strip(),
                        'content': ''
                    }
                continue
            
            if current_block and current_block.get('type') == 'code':
                current_block['content'] += line + '\n'
                continue
            
            # Check for blockquote
            if line.startswith('>'):
                if current_block and current_block.get('type') == 'blockquote':
                    current_block['content'] += line[1:].strip() + '\n'
                else:
                    if current_block:
                        blocks.append(current_block)
                    current_block = {
                        'type': 'blockquote',
                        'content': line[1:].strip() + '\n'
                    }
                continue
            
            # Check for horizontal rule
            if re.match(r'^[-*_]{3,}$', line):
                if current_block:
                    blocks.append(current_block)
                blocks.append({'type': 'horizontal_rule'})
                current_block = None
                continue
            
            # Regular paragraph
            if line.strip():
                if current_block and current_block.get('type') == 'paragraph':
                    current_block['content'] += ' ' + line
                else:
                    if current_block:
                        blocks.append(current_block)
                    current_block = {
                        'type': 'paragraph',
                        'content': line
                    }
            else:
                if current_block:
                    blocks.append(current_block)
                    current_block = None
        
        if current_block:
            blocks.append(current_block)
        
        return {
            'content': markdown_content,
            'blocks': blocks,
            'word_count': self.renderer.get_word_count(markdown_content),
            'line_count': self.renderer.get_line_count(markdown_content)
        }
    
    def export_to_xml(self, markdown_content: str, output_path: str) -> bool:
        """Export to XML format"""
        output_path = self._ensure_extension(output_path, '.xml')
        
        root = Element('document')
        
        # Add metadata
        meta = SubElement(root, 'metadata')
        SubElement(meta, 'word_count').text = str(self.renderer.get_word_count(markdown_content))
        SubElement(meta, 'line_count').text = str(self.renderer.get_line_count(markdown_content))
        
        # Add content
        content = SubElement(root, 'content')
        
        lines = markdown_content.split('\n')
        for line in lines:
            # Parse and add each line as appropriate element
            header_match = re.match(r'^(#{1,6})\s+(.+)$', line)
            if header_match:
                elem = SubElement(content, 'header')
                elem.set('level', str(len(header_match.group(1))))
                elem.text = header_match.group(2)
                continue
            
            if line.startswith('```'):
                elem = SubElement(content, 'code_block')
                elem.set('language', line[3:].strip())
                continue
            
            if line.strip():
                elem = SubElement(content, 'paragraph')
                elem.text = line
        
        # Write XML
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
            f.write(tostring(root, encoding='unicode'))
        
        return True
    
    def export_to_yaml(self, markdown_content: str, output_path: str) -> bool:
        """Export to YAML format"""
        output_path = self._ensure_extension(output_path, '.yaml')
        
        # Parse markdown to structured data
        data = self._parse_markdown_to_json(markdown_content)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, allow_unicode=True, default_flow_style=False)
        
        return True
    
    def export_to_csv(self, markdown_content: str, output_path: str) -> bool:
        """Export tables and structure to CSV"""
        output_path = self._ensure_extension(output_path, '.csv')
        
        # Find all tables in markdown
        tables = self._extract_tables(markdown_content)
        
        with open(output_path, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            
            if tables:
                for i, table in enumerate(tables):
                    if i > 0:
                        writer.writerow([])  # Empty row between tables
                    for row in table:
                        writer.writerow(row)
            else:
                # If no tables, export line content as CSV
                writer.writerow(['line_number', 'content'])
                for i, line in enumerate(markdown_content.split('\n'), 1):
                    writer.writerow([i, line])
        
        return True
    
    def _extract_tables(self, markdown_content: str) -> List[List[List[str]]]:
        """Extract tables from markdown"""
        tables = []
        lines = markdown_content.split('\n')
        current_table = []
        in_table = False
        
        for line in lines:
            # Check if line is a table row
            if '|' in line:
                # Skip separator row
                if re.match(r'^\|[\s\-:|]+\|$', line):
                    continue
                
                # Parse row
                cells = [cell.strip() for cell in line.split('|')[1:-1]]
                current_table.append(cells)
                in_table = True
            else:
                if in_table and current_table:
                    tables.append(current_table)
                    current_table = []
                in_table = False
        
        # Don't forget last table
        if current_table:
            tables.append(current_table)
        
        return tables


# Export format options for the UI
EXPORT_FORMATS = [
    ('HTML', 'html'),
    ('PDF', 'pdf'),
    ('DOCX', 'docx'),
    ('ODT', 'odt'),
    ('RTF', 'rtf'),
    ('EPUB', 'epub'),
    ('TXT', 'txt'),
    ('JSON', 'json'),
    ('XML', 'xml'),
    ('YAML', 'yaml'),
    ('CSV', 'csv'),
    ('LaTeX', 'latex'),
    ('MediaWiki', 'mediawiki'),
    ('reStructuredText', 'rst'),
]
