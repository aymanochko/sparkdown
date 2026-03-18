# SparkDown - Markdown Editor Specification

## 1. Project Overview

**Project Name:** SparkDown
**Type:** Desktop Application (Python with Tkinter)
**Core Feature Summary:** A feature-rich markdown editor with file management, preview capabilities, and extensive export options to multiple formats.
**Target Users:** Writers, developers, documentation authors, and anyone working with markdown files.

## 2. UI/UX Specification

### 2.1 Layout Structure

**Main Window:**
- Single-window application with sidebar navigation
- Default size: 1200x800 pixels
- Minimum size: 900x600 pixels
- Resizable with proper responsive behavior

**Layout Regions:**
```
+----------------------------------------------------------+
|  Menu Bar (File, Edit, View, Export, Help)              |
+----------------------------------------------------------+
|  Toolbar (New, Open, Save, Delete, Preview, Export)     |
+------------------+---------------------------------------+
|                  |                                       |
|   File Browser   |         Editor/Preview Area           |
|   (250px wide)   |                                       |
|                  |   +-------------------------------+   |
|   - File list    |   | View/Edit Toggle Bar          |   |
|   - New file btn |   +-------------------------------+   |
|   - Delete btn   |   |                               |   |
|                  |   |   Markdown Content Area       |   |
|                  |   |   (Text Editor or Preview)    |   |
|                  |   |                               |   |
|                  |   +-------------------------------+   |
+------------------+---------------------------------------+
|  Status Bar (File path, Word count, Current mode)       |
+----------------------------------------------------------+
```

### 2.2 Visual Design

**Color Palette:**
- Primary Background: #1E1E1E (Dark mode default)
- Secondary Background: #252526 (Sidebar)
- Accent Color: #007ACC (Blue highlights)
- Success Color: #4EC9B0 (Teal for save confirmation)
- Warning Color: #DCDCAA (Yellow for warnings)
- Error Color: #F14C4C (Red for errors)
- Text Primary: #D4D4D4
- Text Secondary: #808080
- Border Color: #3C3C3C

**Typography:**
- Font Family (UI): Segoe UI, system-ui
- Font Family (Editor): Consolas, Courier New, monospace
- Font Sizes:
  - Menu/Toolbar: 10px
  - Editor: 14px
  - Sidebar: 12px
  - Status bar: 10px

**Spacing System:**
- Base unit: 4px
- Small padding: 8px
- Medium padding: 12px
- Large padding: 16px
- Component margins: 8px

**Visual Effects:**
- Subtle shadow on toolbar: 0 2px 4px rgba(0,0,0,0.2)
- Hover effects on buttons: lighten background by 10%
- Smooth transitions: 150ms ease-in-out

### 2.3 Components

**File Browser Panel:**
- Tree view showing markdown files
- Icons for different file states (modified, new)
- Context menu (right-click): Open, Delete, Rename
- "New File" button at top
- "Delete" button at bottom

**Editor Area:**
- Text editor with syntax highlighting for markdown
- Line numbers (optional)
- Word wrap toggle
- Find/Replace functionality

**Preview Area:**
- Rendered HTML preview of markdown
- Scrollable
- Synchronized scrolling with editor (when in split mode)

**Toolbar Buttons:**
- Icon + text labels
- States: Normal, Hover, Active, Disabled
- Tooltips on hover

**View/Edit Toggle:**
- Toggle button at top of editor area
- Two modes: "View" (preview) and "Edit" (editor)
- Visual indicator of current mode
- Keyboard shortcut: Ctrl+Tab

## 3. Functional Specification

### 3.1 Core Features

**File Operations:**
1. Create new markdown file
   - Opens a blank editor
   - Prompts for filename before saving
   
2. Open existing markdown file
   - Browse files in designated folder
   - Opens in View mode by default
   
3. Save markdown file
   - Save (Ctrl+S): Save to current path
   - Save As (Ctrl+Shift+S): Choose new location
   
4. Delete markdown file
   - Confirmation dialog before deletion
   - Removes from file system

**Folder Management:**
- Default folder: User's Documents/SparkDown
- Ability to change working folder via menu
- Auto-create folder if it doesn't exist

**View/Edit Modes:**
- View Mode (Default when opening file):
  - Read-only preview of rendered markdown
  - Toggle button to switch to edit mode
  
- Edit Mode:
  - Full text editing capability
  - Toggle button to switch to view mode
  - Unsaved changes indicator

### 3.2 Preview Features

**In-App Preview:**
- Real-time markdown rendering
- Support for:
  - Headers (H1-H6)
  - Bold, italic, strikethrough
  - Lists (ordered, unordered, nested)
  - Code blocks with syntax highlighting
  - Tables
  - Links and images
  - Blockquotes
  - Horizontal rules
  - Task lists

**Browser Preview:**
- Open current file in default web browser
- Uses temporary HTML file
- Auto-refresh on content change (optional)

### 3.3 Export Functionality

**Supported Export Formats:**

| Format | Extension | Method |
|--------|-----------|--------|
| HTML | .html | markdown + custom template |
| PDF | .pdf | weasyprint |
| DOCX | .docx | pypandoc |
| ODT | .odt | pypandoc |
| RTF | .rtf | pypandoc |
| EPUB | .epub | pypandoc |
| TXT | .txt | plain text extraction |
| JSON | .json | custom converter |
| XML | .xml | custom converter |
| YAML | .yaml | custom converter |
| CSV | .csv | table extraction |
| LaTeX | .tex | pypandoc |
| MediaWiki | .wiki | pypandoc |
| reStructuredText | .rst | pypandoc |

**Export Options:**
- Export current file
- Export with custom filename
- Export to custom location

### 3.4 User Interactions and Flows

**New File Flow:**
1. User clicks "New" or presses Ctrl+N
2. Editor clears, shows blank document
3. User types content
4. User clicks "Save" → prompts for filename
5. File saved to working folder

**Open File Flow:**
1. User clicks file in sidebar or uses File > Open
2. File loads into editor in View mode
3. User can toggle to Edit mode
4. Changes tracked with indicator

**Delete File Flow:**
1. User selects file in sidebar
2. User clicks Delete or right-click > Delete
3. Confirmation dialog appears
4. On confirm, file removed from disk and sidebar

**Export Flow:**
1. User clicks Export in menu/toolbar
2. Export dialog shows format options
3. User selects format
4. File dialog for destination (optional)
5. Export completed, success notification

### 3.5 Data Flow & Processing

**Key Modules:**

1. **FileManager** (`file_manager.py`)
   - `list_files(folder_path)` - List markdown files
   - `read_file(file_path)` - Read file content
   - `write_file(file_path, content)` - Write file
   - `delete_file(file_path)` - Delete file
   - `create_backup(file_path)` - Create backup

2. **MarkdownRenderer** (`renderer.py`)
   - `render_to_html(markdown_content)` - Convert to HTML
   - `render_to_pdf(markdown_content, output_path)` - Convert to PDF
   - `get_toc(markdown_content)` - Generate table of contents

3. **ExportManager** (`exporter.py`)
   - `export_to_format(content, format, output_path)` - Main export
   - Individual methods for each format

4. **UIController** (`ui_controller.py`)
   - Handle all UI interactions
   - Manage view/edit state
   - Update sidebar

### 3.6 Edge Cases

- Empty file handling
- Very large files (>1MB) - show warning
- Invalid markdown syntax - graceful degradation
- Network folder access - timeout handling
- File permission errors - user notification
- Unsaved changes on close - prompt to save
- Duplicate filenames - auto-rename or overwrite prompt

## 4. Acceptance Criteria

### 4.1 Success Conditions

1. **File Operations:**
   - [ ] Can create new markdown files
   - [ ] Can open existing markdown files
   - [ ] Can save markdown files
   - [ ] Can delete markdown files
   - [ ] Files saved to correct folder

2. **View/Edit Modes:**
   - [ ] Files open in View mode by default
   - [ ] Toggle button switches between modes
   - [ ] View mode shows rendered preview
   - [ ] Edit mode allows text modification

3. **Preview:**
   - [ ] Markdown renders correctly in preview
   - [ ] Browser preview opens in external browser

4. **Export:**
   - [ ] All 16 formats export successfully
   - [ ] Exported files are valid and readable

### 4.2 Visual Checkpoints

1. Application launches with dark theme
2. Sidebar shows markdown files from working folder
3. Editor area shows content clearly
4. Toggle button clearly indicates current mode
5. All menu items accessible
6. Toolbar buttons have icons and respond to hover
7. Status bar shows relevant information
