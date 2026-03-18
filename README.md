# SparkDown - Markdown Editor

A feature-rich Python markdown editor with file management, preview capabilities, and extensive export options.

## Features

### File Management
- Create new markdown files
- Open existing markdown files
- Save markdown files to a specific folder
- Delete markdown files
- Change working folder

### View/Edit Modes
- **View Mode** (Default): Read-only preview of rendered markdown
- **Edit Mode**: Full text editing capability
- Toggle between modes with Ctrl+Tab or the toggle button

### Preview Features
- In-app markdown preview with live rendering
- Preview in web browser

### Export Formats
Export your markdown to:
- **HTML** - Web pages
- **PDF** - Documents
- **DOCX** - Microsoft Word
- **ODT** - OpenDocument Text
- **RTF** - Rich Text Format
- **EPUB** - E-books
- **TXT** - Plain text
- **JSON** - Structured data
- **XML** - Extensible Markup Language
- **YAML** - YAML Ain't Markup Language
- **CSV** - Comma-separated values
- **LaTeX** - Typesetting
- **MediaWiki** - Wiki format
- **reStructuredText** - Python documentation format

## Installation

### Prerequisites
- Python 3.8 or higher

### Basic Dependencies
```bash
pip install markdown Pygments
```

### Full Dependencies (for all export formats)
```bash
pip install markdown Pygments weasyprint pypandoc
```

Note: `pypandoc` requires Pandoc to be installed on your system. Download from https://pandoc.org/

## Running the Application

```bash
python src/sparkdown.py
```

Or:
```bash
python main.py
```

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| Ctrl+N | New file |
| Ctrl+O | Open file |
| Ctrl+S | Save file |
| Ctrl+Shift+S | Save As |
| Ctrl+Tab | Toggle View/Edit mode |
| Ctrl+P | Preview in browser |
| Ctrl+F | Find text |

## Default Folder

Files are saved to: `Documents/SparkDown/`

You can change this via File > Change Folder

## UI Overview

- **Sidebar**: File browser with list of markdown files
- **Editor**: Text editor with syntax highlighting
- **Preview**: Rendered markdown preview
- **Toolbar**: Quick access to common actions
- **Status Bar**: File info, word count, current mode

## License

MIT License
