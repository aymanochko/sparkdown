"""
SparkDown - Main Application
A feature-rich markdown editor with file management and export capabilities
"""

import os
import tempfile
import threading
import tkinter as tk
import webbrowser
from tkinter import Menu, filedialog, messagebox, ttk

from exporter import EXPORT_FORMATS, Exporter

# Import our modules
from file_manager import FileManager
from renderer import MarkdownRenderer


class SparkDownApp:
    """Main application class for SparkDown"""

    # Class-level default attributes for test compatibility
    # These allow tests to work without calling __init__
    current_file = None
    has_unsaved_changes = False
    content_modified = False
    is_edit_mode = True
    file_manager = None
    renderer = None
    exporter = None
    preview_frame = None
    editor_frame = None
    editor = None
    unsaved_label = None
    root = None

    def __init__(self, root):
        """Initialize the application"""
        self.root = root
        self.root.title("SparkDown - Markdown Editor")
        self.root.geometry("1200x800")
        self.root.minsize(900, 600)

        # Initialize components
        self.file_manager = FileManager()
        self.renderer = MarkdownRenderer()
        self.exporter = Exporter(self.renderer)

        # Application state
        self.current_file = None
        self.is_edit_mode = False
        self.has_unsaved_changes = False
        self.content_modified = False

        # Setup UI
        self.setup_styles()
        self.create_menu()
        self.create_toolbar()
        self.create_main_layout()
        self.create_status_bar()

        # Set initial mode
        self.is_edit_mode = True

        # Bind events
        self.bind_events()

        # Initial file list
        self.refresh_file_list()

        # Create welcome content
        self.show_welcome()

    def setup_styles(self):
        """Setup custom styles"""
        # Ensure root is initialized before configuring
        assert self.root is not None, "root must be initialized before setup_styles"

        self.style = ttk.Style()
        self.style.theme_use('clam')

        # Dark theme colors
        self.colors = {
            'bg_primary': '#1E1E1E',
            'bg_secondary': '#252526',
            'bg_tertiary': '#2D2D2D',
            'accent': '#007ACC',
            'success': '#4EC9B0',
            'warning': '#DCDCAA',
            'error': '#F14C4C',
            'text_primary': '#D4D4D4',
            'text_secondary': '#808080',
            'border': '#3C3C3C',
            'hover': '#3C3C3C',
            'heading_color': '#569CD6',
            'link_color': '#4EC9B0',
            'code_color': '#CE9178'
        }

        # Configure styles
        self.root.configure(bg=self.colors['bg_primary'])

        self.style.configure('Dark.TFrame', background=self.colors['bg_primary'])
        self.style.configure('Sidebar.TFrame', background=self.colors['bg_secondary'])
        self.style.configure('Dark.TLabel', background=self.colors['bg_primary'],
                           foreground=self.colors['text_primary'])
        self.style.configure('Dark.TButton', background=self.colors['bg_tertiary'],
                           foreground=self.colors['text_primary'], bordercolor=self.colors['border'])
        self.style.configure('Toolbar.TButton', background=self.colors['bg_secondary'],
                           foreground=self.colors['text_primary'], borderwidth=0,
                           padding=5)
        self.style.map('Toolbar.TButton',
                      background=[('active', self.colors['hover'])])

        # Configure treeview
        self.style.configure('FileList.Treeview',
                           background=self.colors['bg_secondary'],
                           foreground=self.colors['text_primary'],
                           fieldbackground=self.colors['bg_secondary'],
                           bordercolor=self.colors['border'])
        self.style.configure('FileList.Treeview.Item',
                           background=self.colors['bg_secondary'],
                           foreground=self.colors['text_primary'])

    def create_menu(self):
        """Create the menu bar"""
        self.menubar = Menu(self.root, bg=self.colors['bg_secondary'],
                           fg=self.colors['text_primary'])
        self.root.config(menu=self.menubar)

        # File menu
        file_menu = Menu(self.menubar, tearoff=0, bg=self.colors['bg_secondary'],
                        fg=self.colors['text_primary'])
        self.menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New", accelerator="Ctrl+N", command=self.new_file)
        file_menu.add_command(label="Open...", accelerator="Ctrl+O", command=self.open_file)
        file_menu.add_command(label="Save", accelerator="Ctrl+S", command=self.save_file)
        file_menu.add_command(label="Save As...", accelerator="Ctrl+Shift+S", command=self.save_file_as)
        file_menu.add_separator()
        file_menu.add_command(label="Change Folder...", command=self.change_folder)
        file_menu.add_command(label="Open Folder", command=self.open_folder)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit_app)

        # Edit menu
        edit_menu = Menu(self.menubar, tearoff=0, bg=self.colors['bg_secondary'],
                        fg=self.colors['text_primary'])
        self.menubar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Undo", accelerator="Ctrl+Z", command=self.undo)
        edit_menu.add_command(label="Redo", accelerator="Ctrl+Y", command=self.redo)
        edit_menu.add_separator()
        edit_menu.add_command(label="Cut", accelerator="Ctrl+X", command=self.cut)
        edit_menu.add_command(label="Copy", accelerator="Ctrl+C", command=self.copy)
        edit_menu.add_command(label="Paste", accelerator="Ctrl+V", command=self.paste)
        edit_menu.add_separator()
        edit_menu.add_command(label="Find...", accelerator="Ctrl+F", command=self.find)

        # View menu
        view_menu = Menu(self.menubar, tearoff=0, bg=self.colors['bg_secondary'],
                        fg=self.colors['text_primary'])
        self.menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="Toggle View/Edit", accelerator="Ctrl+Tab",
                             command=self.toggle_mode)
        view_menu.add_command(label="Preview in Browser", accelerator="Ctrl+P",
                             command=self.preview_in_browser)
        view_menu.add_separator()
        view_menu.add_command(label="Refresh File List", command=self.refresh_file_list)

        # Export menu
        export_menu = Menu(self.menubar, tearoff=0, bg=self.colors['bg_secondary'],
                          fg=self.colors['text_primary'])
        self.menubar.add_cascade(label="Export", menu=export_menu)

        # Add export format options
        for name, fmt in EXPORT_FORMATS:
            export_menu.add_command(label=f"Export to {name}",
                                   command=lambda f=fmt: self.export_file(f))

        # Help menu
        help_menu = Menu(self.menubar, tearoff=0, bg=self.colors['bg_secondary'],
                        fg=self.colors['text_primary'])
        self.menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About SparkDown", command=self.show_about)

    def create_toolbar(self):
        """Create the toolbar"""
        self.toolbar = tk.Frame(self.root, bg=self.colors['bg_secondary'],
                               height=40, relief=tk.RAISED)
        self.toolbar.pack(side=tk.TOP, fill=tk.X)

        # Toolbar buttons
        btn_config = {'bg': self.colors['bg_secondary'], 'fg': self.colors['text_primary'],
                     'activebackground': self.colors['hover'], 'activeforeground': self.colors['text_primary'],
                     'relief': tk.FLAT, 'padx': 10, 'pady': 5}

        self.btn_new = tk.Button(self.toolbar, text="📄 New", command=self.new_file, **btn_config)
        self.btn_new.pack(side=tk.LEFT, padx=2, pady=2)

        self.btn_open = tk.Button(self.toolbar, text="📂 Open", command=self.open_selected_file, **btn_config)
        self.btn_open.pack(side=tk.LEFT, padx=2, pady=2)

        self.btn_save = tk.Button(self.toolbar, text="💾 Save", command=self.save_file, **btn_config)
        self.btn_save.pack(side=tk.LEFT, padx=2, pady=2)

        self.btn_delete = tk.Button(self.toolbar, text="🗑 Delete", command=self.delete_file, **btn_config)
        self.btn_delete.pack(side=tk.LEFT, padx=2, pady=2)

        # Separator
        tk.Frame(self.toolbar, bg=self.colors['border'], width=1).pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)

        self.btn_preview = tk.Button(self.toolbar, text="👁 Preview", command=self.toggle_mode, **btn_config)
        self.btn_preview.pack(side=tk.LEFT, padx=2, pady=2)

        self.btn_browser = tk.Button(self.toolbar, text="🌐 Browser", command=self.preview_in_browser, **btn_config)
        self.btn_browser.pack(side=tk.LEFT, padx=2, pady=2)

        # Separator
        tk.Frame(self.toolbar, bg=self.colors['border'], width=1).pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)

        # Mode toggle button
        self.btn_toggle = tk.Button(self.toolbar, text="🔄 Switch to Edit",
                                    command=self.toggle_mode, **btn_config)
        self.btn_toggle.pack(side=tk.LEFT, padx=2, pady=2)

        # Status indicator
        self.mode_label = tk.Label(self.toolbar, text="VIEW MODE",
                                   bg=self.colors['accent'], fg='white',
                                   padx=10, pady=5, font=('Segoe UI', 9, 'bold'))
        self.mode_label.pack(side=tk.RIGHT, padx=10)

    def create_main_layout(self):
        """Create the main layout with sidebar and editor"""
        # Main container
        self.main_container = tk.Frame(self.root, bg=self.colors['bg_primary'])
        self.main_container.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Create PanedWindow for resizable panes
        self.paned = ttk.PanedWindow(self.main_container, orient=tk.HORIZONTAL)
        self.paned.pack(fill=tk.BOTH, expand=True)

        # Left sidebar - File list
        self.sidebar = tk.Frame(self.paned, bg=self.colors['bg_secondary'], width=250)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)

        # Sidebar header
        sidebar_header = tk.Frame(self.sidebar, bg=self.colors['bg_tertiary'])
        sidebar_header.pack(fill=tk.X, padx=5, pady=5)

        tk.Label(sidebar_header, text="📁 Files", bg=self.colors['bg_tertiary'],
                fg=self.colors['text_primary'], font=('Segoe UI', 11, 'bold')).pack(side=tk.LEFT, padx=5)

        # Folder path label
        self.folder_label = tk.Label(self.sidebar, text="", bg=self.colors['bg_secondary'],
                                    fg=self.colors['text_secondary'], font=('Segoe UI', 8))
        self.folder_label.pack(fill=tk.X, padx=5, pady=(0, 5))
        self.update_folder_label()

        # File listbox
        self.file_listbox = tk.Listbox(self.sidebar, bg=self.colors['bg_secondary'],
                                       fg=self.colors['text_primary'],
                                       selectbackground=self.colors['accent'],
                                       borderwidth=0, highlightthickness=0,
                                       font=('Segoe UI', 10))
        self.file_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.file_listbox.bind('<Double-Button-1>', lambda e: self.open_selected_file())
        self.file_listbox.bind('<Return>', lambda e: self.open_selected_file())

        # Sidebar buttons
        sidebar_btns = tk.Frame(self.sidebar, bg=self.colors['bg_secondary'])
        sidebar_btns.pack(fill=tk.X, padx=5, pady=5)

        tk.Button(sidebar_btns, text="+ New File", command=self.new_file,
                 bg=self.colors['accent'], fg='white', relief=tk.FLAT,
                 padx=10, pady=5).pack(side=tk.LEFT, padx=2)

        tk.Button(sidebar_btns, text="🗑 Delete", command=self.delete_file,
                 bg=self.colors['error'], fg='white', relief=tk.FLAT,
                 padx=10, pady=5).pack(side=tk.RIGHT, padx=2)

        # Add sidebar to paned window
        self.paned.add(self.sidebar, weight=0)

        # Right side - Editor/Preview area
        self.content_area = tk.Frame(self.paned, bg=self.colors['bg_primary'])
        self.paned.add(self.content_area, weight=1)

        # Mode indicator bar
        self.mode_bar = tk.Frame(self.content_area, bg=self.colors['bg_tertiary'], height=35)
        self.mode_bar.pack(fill=tk.X)

        # Toggle button in mode bar
        self.toggle_btn = tk.Button(self.mode_bar, text="✏️ Edit Mode",
                                   command=self.toggle_mode,
                                   bg=self.colors['bg_tertiary'], fg=self.colors['text_primary'],
                                   relief=tk.FLAT, padx=15, pady=5)
        self.toggle_btn.pack(side=tk.LEFT, padx=5)

        # Unsaved indicator
        self.unsaved_label = tk.Label(self.mode_bar, text="", bg=self.colors['bg_tertiary'],
                                      fg=self.colors['warning'], font=('Segoe UI', 10, 'bold'))
        self.unsaved_label.pack(side=tk.LEFT, padx=5)

        # Editor frame
        self.editor_frame = tk.Frame(self.content_area, bg=self.colors['bg_primary'])
        self.editor_frame.pack(fill=tk.BOTH, expand=True)

        # Text editor
        self.editor = tk.Text(self.editor_frame, bg=self.colors['bg_primary'],
                             fg=self.colors['text_primary'], insertbackground='white',
                             font=('Consolas', 14), wrap=tk.WORD, borderwidth=0,
                             padx=15, pady=15, undo=True)
        self.editor.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Scrollbar for editor
        editor_scroll = tk.Scrollbar(self.editor_frame, command=self.editor.yview)
        editor_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.editor.config(yscrollcommand=editor_scroll.set)

        # Preview frame (hidden by default)
        self.preview_frame = tk.Frame(self.content_area, bg=self.colors['bg_primary'])

        # Preview text (using Text widget to display HTML)
        self.preview = tk.Text(self.preview_frame, bg=self.colors['bg_primary'],
                              fg=self.colors['text_primary'],
                              font=('Segoe UI', 12), wrap=tk.WORD, borderwidth=0,
                              padx=15, pady=15, state=tk.DISABLED)
        self.preview.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Scrollbar for preview
        preview_scroll = tk.Scrollbar(self.preview_frame, command=self.preview.yview)
        preview_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.preview.config(yscrollcommand=preview_scroll.set)

        # Initially show editor (but don't call show_editor yet)
        # Will be handled by show_welcome() later

    def create_status_bar(self):
        """Create the status bar"""
        self.status_bar = tk.Frame(self.root, bg=self.colors['bg_tertiary'], height=25)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        # File path
        self.status_file = tk.Label(self.status_bar, text="No file open",
                                    bg=self.colors['bg_tertiary'],
                                    fg=self.colors['text_secondary'], anchor=tk.W)
        self.status_file.pack(side=tk.LEFT, padx=10)

        # Word count
        self.status_words = tk.Label(self.status_bar, text="",
                                     bg=self.colors['bg_tertiary'],
                                     fg=self.colors['text_secondary'])
        self.status_words.pack(side=tk.RIGHT, padx=10)

        # Mode
        self.status_mode = tk.Label(self.status_bar, text="View Mode",
                                     bg=self.colors['bg_tertiary'],
                                     fg=self.colors['accent'])
        self.status_mode.pack(side=tk.RIGHT, padx=10)

    def bind_events(self):
        """Bind keyboard shortcuts"""
        self.root.bind('<Control-n>', lambda e: self.new_file())
        self.root.bind('<Control-o>', lambda e: self.open_file())
        self.root.bind('<Control-s>', lambda e: self.save_file())
        self.root.bind('<Control-S>', lambda e: self.save_file_as())
        self.root.bind('<Control-Tab>', lambda e: self.toggle_mode())
        self.root.bind('<Control-p>', lambda e: self.preview_in_browser())

        # Track changes
        self.editor.bind('<<Modified>>', self.on_content_change)

        # Confirm close with unsaved changes
        self.root.protocol("WM_DELETE_WINDOW", self.quit_app)

    def on_content_change(self, event=None):
        """Handle content changes"""
        if self.editor.edit_modified():
            self.has_unsaved_changes = True
            self.content_modified = True
            self.unsaved_label.config(text="● Modified")
            self.editor.edit_modified(False)
        self.update_word_count()

    def update_word_count(self):
        """Update word count in status bar"""
        content = self.editor.get(1.0, tk.END)
        word_count = self.renderer.get_word_count(content)
        line_count = self.renderer.get_line_count(content)
        self.status_words.config(text=f"Words: {word_count} | Lines: {line_count}")

    def update_folder_label(self):
        """Update the folder path label"""
        path = self.file_manager.folder_path
        if len(path) > 40:
            path = "..." + path[-37:]
        self.folder_label.config(text=path)

    def refresh_file_list(self):
        """Refresh the file list in sidebar"""
        self.file_listbox.delete(0, tk.END)
        files = self.file_manager.list_files()
        for f in files:
            self.file_listbox.insert(tk.END, f"📄 {f}")

    def show_welcome(self):
        """Show welcome content"""
        welcome_content = """# Welcome to SparkDown

SparkDown is a powerful markdown editor with many features:

## Features

- **File Management**: Create, open, save, and delete markdown files
- **View/Edit Modes**: Toggle between view and edit modes
- **Live Preview**: See your markdown rendered in real-time
- **Browser Preview**: Open your document in a web browser
- **Export**: Export to multiple formats including:
  - HTML, PDF, DOCX, ODT, RTF, EPUB
  - TXT, JSON, XML, YAML, CSV
  - LaTeX, MediaWiki, reStructuredText

## Getting Started

1. Click **New** to create a new file
2. Or select an existing file from the sidebar
3. Use the toggle button to switch between View and Edit modes
4. Save your work with **Ctrl+S**

## Markdown Syntax

### Headers
```markdown
# H1
## H2
### H3
```

### Text Formatting
- **Bold** or __bold__
- *Italic* or _italic_
- ~~Strikethrough~~

### Lists
- Item 1
- Item 2
  - Nested item

### Code
Inline `code` or code blocks:
```python
def hello():
    print("Hello, World!")
```

---

*Start editing to see the magic!*
"""
        self.editor.delete(1.0, tk.END)
        self.editor.insert(1.0, welcome_content)
        self.current_file = None
        self.has_unsaved_changes = False
        self.is_edit_mode = True
        self.show_editor()
        self.update_title()

    def update_title(self):
        """Update window title"""
        title = "SparkDown"
        if self.current_file:
            title = f"{self.current_file} - SparkDown"
        if self.has_unsaved_changes:
            title = "● " + title
        self.root.title(title)

    def new_file(self):
        """Create a new file"""
        if self.has_unsaved_changes:
            if not messagebox.askyesno("Unsaved Changes",
                                        "You have unsaved changes. Create new file anyway?"):
                return

        self.editor.delete(1.0, tk.END)
        self.current_file = None
        self.has_unsaved_changes = False
        self.content_modified = False
        self.unsaved_label.config(text="")
        self.is_edit_mode = True
        self.show_editor()
        self.update_title()
        self.update_word_count()

    def open_file(self):
        """Open a file dialog"""
        filename = filedialog.askopenfilename(
            title="Open Markdown File",
            filetypes=[("Markdown files", "*.md"), ("All files", "*.*")],
            initialdir=self.file_manager.folder_path
        )

        if filename:
            self.load_file(filename)

    def open_selected_file(self):
        """Open the selected file from the list"""
        selection = self.file_listbox.curselection()
        if not selection:
            return

        filename = self.file_listbox.get(selection[0])[2:]  # Remove emoji prefix
        file_path = self.file_manager.get_file_path(filename)

        if file_path.exists():
            self.load_file(str(file_path))

    def load_file(self, file_path):
        """Load a file"""
        if self.has_unsaved_changes:
            if not messagebox.askyesno("Unsaved Changes",
                                        "You have unsaved changes. Open another file anyway?"):
                return

        try:
            with open(file_path, encoding='utf-8') as f:
                content = f.read()

            self.editor.delete(1.0, tk.END)
            self.editor.insert(1.0, content)

            self.current_file = os.path.basename(file_path)
            self.has_unsaved_changes = False
            self.content_modified = False
            self.unsaved_label.config(text="")

            # Default to view mode
            self.is_edit_mode = False
            self.show_preview()

            self.update_title()
            self.refresh_file_list()
            self.update_word_count()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to open file: {e}")

    def save_file(self):
        """Save the current file"""
        if self.current_file is None:
            return self.save_file_as()

        try:
            content = self.editor.get(1.0, tk.END).rstrip('\n')
            self.file_manager.write_file(self.current_file, content)

            self.has_unsaved_changes = False
            self.content_modified = False
            self.unsaved_label.config(text="")

            self.update_title()
            self.refresh_file_list()

            messagebox.showinfo("Saved", "File saved successfully!")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to save file: {e}")

    def save_file_as(self):
        """Save file with new name"""
        filename = filedialog.asksaveasfilename(
            title="Save Markdown File",
            defaultextension=".md",
            filetypes=[("Markdown files", "*.md"), ("All files", "*.*")],
            initialdir=self.file_manager.folder_path
        )

        if filename:
            try:
                content = self.editor.get(1.0, tk.END).rstrip('\n')

                # Get just the filename
                self.current_file = os.path.basename(filename)

                self.file_manager.write_file(self.current_file, content)

                self.has_unsaved_changes = False
                self.content_modified = False
                self.unsaved_label.config(text="")

                self.update_title()
                self.refresh_file_list()

                messagebox.showinfo("Saved", "File saved successfully!")

            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file: {e}")

    def delete_file(self):
        """Delete the selected file"""
        selection = self.file_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a file to delete")
            return

        filename = self.file_listbox.get(selection[0])[2:]

        if messagebox.askyesno("Confirm Delete", f"Delete '{filename}'?"):
            try:
                self.file_manager.delete_file(filename)
                self.refresh_file_list()

                # Clear editor if this was the current file
                if self.current_file == filename:
                    self.new_file()

            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete file: {e}")

    def change_folder(self):
        """Change the working folder"""
        folder = filedialog.askdirectory(title="Select Folder",
                                         initialdir=self.file_manager.folder_path)
        if folder:
            self.file_manager.set_folder(folder)
            self.update_folder_label()
            self.refresh_file_list()

    def open_folder(self):
        """Open the working folder in file explorer"""
        folder = self.file_manager.folder_path
        if os.path.exists(folder):
            os.startfile(folder)

    def toggle_mode(self):
        """Toggle between view and edit modes"""
        self.is_edit_mode = not self.is_edit_mode

        if self.is_edit_mode:
            self.show_editor()
        else:
            self.show_preview()

    def show_editor(self):
        """Show the editor"""
        self.preview_frame.pack_forget()
        self.editor_frame.pack(fill=tk.BOTH, expand=True)

        self.is_edit_mode = True
        self.editor.config(state=tk.NORMAL)

        # Update UI
        self.btn_toggle.config(text="🔄 Switch to View")
        self.toggle_btn.config(text="✏️ Edit Mode")
        self.mode_label.config(text="EDIT MODE", bg=self.colors['success'])
        self.status_mode.config(text="Edit Mode")

        # Focus on editor
        self.editor.focus()

    def show_preview(self):
        """Show the preview with markdown formatting"""
        self.editor_frame.pack_forget()
        self.preview_frame.pack(fill=tk.BOTH, expand=True)

        self.is_edit_mode = False

        # Get markdown content
        content = self.editor.get(1.0, tk.END)

        # Configure preview text widget
        self.preview.config(state=tk.NORMAL)
        self.preview.delete(1.0, tk.END)

        # Setup text tags for formatting
        self._setup_preview_tags()

        # Render markdown with formatting
        self._render_markdown(content)

        self.preview.config(state=tk.DISABLED)

        # Update UI
        self.btn_toggle.config(text="🔄 Switch to Edit")
        self.toggle_btn.config(text="👁 View Mode")
        self.mode_label.config(text="VIEW MODE", bg=self.colors['accent'])
        self.status_mode.config(text="View Mode")

    def _setup_preview_tags(self):
        """Setup text tags for markdown formatting"""
        # Use .get() with defaults for safe access
        heading_color = self.colors.get('heading_color', '#569CD6')
        link_color = self.colors.get('link_color', '#4EC9B0')
        code_color = self.colors.get('code_color', '#CE9178')
        bg_tertiary = self.colors.get('bg_tertiary', '#2D2D2D')
        text_secondary = self.colors.get('text_secondary', '#808080')
        accent = self.colors.get('accent', '#007ACC')
        border = self.colors.get('border', '#3C3C3C')

        # Configure tag styles
        self.preview.tag_configure('h1', font=('Segoe UI', 24, 'bold'), foreground=heading_color)
        self.preview.tag_configure('h2', font=('Segoe UI', 20, 'bold'), foreground=heading_color)
        self.preview.tag_configure('h3', font=('Segoe UI', 16, 'bold'), foreground=heading_color)
        self.preview.tag_configure('h4', font=('Segoe UI', 14, 'bold'), foreground=heading_color)
        self.preview.tag_configure('h5', font=('Segoe UI', 12, 'bold'), foreground=heading_color)
        self.preview.tag_configure('h6', font=('Segoe UI', 11, 'bold'), foreground=heading_color)
        self.preview.tag_configure('bold', font=('Segoe UI', 12, 'bold'))
        self.preview.tag_configure('italic', font=('Segoe UI', 12, 'italic'))
        self.preview.tag_configure('code', font=('Consolas', 12), background=bg_tertiary, foreground=code_color)
        self.preview.tag_configure('code_block', font=('Consolas', 11), background=bg_tertiary,
                                   foreground=code_color, relief=tk.FLAT, lmargin1=20, lmargin2=20)
        self.preview.tag_configure('link', foreground=link_color, underline=True)
        self.preview.tag_configure('blockquote', background=bg_tertiary, lmargin1=20, lmargin2=20, relief=tk.FLAT)
        self.preview.tag_configure('blockquote_text', foreground=text_secondary, font=('Segoe UI', 12, 'italic'))
        self.preview.tag_configure('list_bullet', foreground=accent)
        self.preview.tag_configure('hr', foreground=border)

    def _render_markdown(self, content):
        """Render markdown content with formatting"""
        import re

        lines = content.split('\n')

        # Track if we're in a code block
        in_code_block = False
        code_block_content = []
        code_block_start = 0

        for line in lines:
            # Check for code block start/end
            if line.strip().startswith('```'):
                if not in_code_block:
                    # Start of code block
                    in_code_block = True
                    code_block_start = self.preview.index(tk.INSERT)
                    code_block_content = [line[3:].strip()]  # Get language if specified
                    self.preview.insert(tk.END, '\n')
                else:
                    # End of code block
                    in_code_block = False
                    self.preview.insert(tk.END, '\n')
                    code_end = self.preview.index(tk.INSERT + ' -1c')
                    self.preview.tag_add('code_block', code_block_start, code_end)
                    code_block_content = []
                continue

            if in_code_block:
                code_block_content.append(line)
                self.preview.insert(tk.END, line + '\n')
                continue

            # Check for horizontal rule
            if re.match(r'^[-*_]{3,}$', line.strip()):
                self.preview.insert(tk.END, '─' * 50 + '\n', 'hr')
                continue

            # Check for headers
            header_match = re.match(r'^(#{1,6})\s+(.*)$', line)
            if header_match:
                level = len(header_match.group(1))
                text = header_match.group(2)
                tag = f'h{level}'
                self.preview.insert(tk.END, text + '\n', tag)
                continue

            # Check for blockquote
            if line.strip().startswith('>'):
                quote_text = line.lstrip('>').strip()
                self.preview.insert(tk.END, '│ ', 'blockquote')
                self.preview.insert(tk.END, quote_text + '\n', 'blockquote_text')
                continue

            # Check for list items
            list_match = re.match(r'^(\s*)([-*+]|\d+\.)\s+(.*)$', line)
            if list_match:
                indent = len(list_match.group(1))
                text = list_match.group(3)
                self.preview.insert(tk.END, '  ' * (indent // 2) + '• ', 'list_bullet')
                self._format_inline_markdown(text)
                self.preview.insert(tk.END, '\n')
                continue

            # Regular paragraph - process inline formatting
            if line.strip():
                self._format_inline_markdown(line)
                self.preview.insert(tk.END, '\n')
            else:
                # Empty line
                self.preview.insert(tk.END, '\n')

    def _format_inline_markdown(self, text):
        """Format inline markdown elements"""
        import re

        # Pattern for inline code
        code_pattern = r'`([^`]+)`'

        # Pattern for bold (**text** or __text__)
        bold_pattern = r'\*\*([^*]+)\*\*|__([^_]+)__'

        # Pattern for italic (*text* or _text_)
        italic_pattern = r'(?<!\*)\*([^*]+)\*(?!\*)|(?<!_)_([^_]+)_(?!_)'

        # Pattern for links [text](url)
        link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'

        # Pattern for strikethrough ~~text~~
        strike_pattern = r'~~([^~]+)~~'

        # We'll process in order: code first, then links, then bold, italic
        # Use a single pattern to find all positions

        # First, handle code blocks specially
        code_positions = []
        for match in re.finditer(code_pattern, text):
            code_positions.append((match.start(), match.end(), 'code', match.group(1)))

        # Remove code from text temporarily for other processing
        temp_text = text
        offset = 0
        for start, end, _tag, _content in code_positions:
            placeholder = f'\x00CODE{offset}\x00'
            temp_text = temp_text[:start] + placeholder + temp_text[end:]
            offset += 1

        # Handle links
        link_positions = []
        for match in re.finditer(link_pattern, temp_text):
            link_positions.append((match.start(), match.end(), 'link', match.group(1)))

        # Handle bold
        bold_positions = []
        for match in re.finditer(bold_pattern, temp_text):
            content = match.group(1) or match.group(2)
            bold_positions.append((match.start(), match.end(), 'bold', content))

        # Handle italic
        italic_positions = []
        for match in re.finditer(italic_pattern, temp_text):
            content = match.group(1) or match.group(2)
            italic_positions.append((match.start(), match.end(), 'italic', content))

        # Handle strikethrough
        strike_positions = []
        for match in re.finditer(strike_pattern, temp_text):
            strike_positions.append((match.start(), match.end(), 'strike', match.group(1)))

        # Now build the result with proper formatting
        # Combine all positions and sort
        all_positions = []
        for pos in code_positions:
            all_positions.append((pos[0], pos[1], pos[2], pos[3], 'code_placeholder'))
        for pos in link_positions:
            all_positions.append((pos[0], pos[1], pos[2], pos[3], 'link'))
        for pos in bold_positions:
            all_positions.append((pos[0], pos[1], pos[2], pos[3], 'bold'))
        for pos in italic_positions:
            all_positions.append((pos[0], pos[1], pos[2], pos[3], 'italic'))
        for pos in strike_positions:
            all_positions.append((pos[0], pos[1], pos[2], pos[3], 'strike'))

        all_positions.sort(key=lambda x: x[0])

        # Build the formatted text
        result_parts = []
        last_end = 0

        # Note: type_ is from the pattern but not used in this loop
        for start, end, tag, content, _type in all_positions:
            # Add plain text before this match
            if start > last_end:
                result_parts.append((text[last_end:start], None))

            # Add the formatted content
            result_parts.append((content, tag))
            last_end = end

        # Add remaining plain text
        if last_end < len(text):
            result_parts.append((text[last_end:], None))

        # Now insert with tags
        for content, tag in result_parts:
            if tag:
                self.preview.insert(tk.END, content, tag)
            else:
                self.preview.insert(tk.END, content)

    def _strip_html_tags(self, html):
        """Strip HTML tags for display in Text widget"""
        import re
        # Remove HTML tags but keep some formatting
        text = re.sub(r'<br\s*/?>', '\n', html)
        text = re.sub(r'</p>', '\n\n', text)
        text = re.sub(r'</div>', '\n', text)
        text = re.sub(r'<[^>]+>', '', text)
        text = re.sub(r'&nbsp;', ' ', text)
        text = re.sub(r'<', '<', text)
        text = re.sub(r'>', '>', text)
        text = re.sub(r'&', '&', text)
        return text.strip()

    def preview_in_browser(self):
        """Open preview in web browser"""
        content = self.editor.get(1.0, tk.END)

        # Get title from first H1 or use filename
        title = self.current_file or "SparkDown Preview"

        html = self.renderer.render_to_html(content, title)

        # Save to temporary file and open in browser
        try:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.html',
                                           delete=False, encoding='utf-8') as tmp:
                tmp.write(html)
                tmp_path = tmp.name

            webbrowser.open(f'file://{tmp_path}')

        except Exception as e:
            messagebox.showerror("Error", f"Failed to open in browser: {e}")

    def export_file(self, format_name):
        """Export current file to specified format"""
        if self.current_file is None and not self.editor.get(1.0, tk.END).strip():
            messagebox.showwarning("No Content", "Nothing to export")
            return

        # Get export format info
        format_ext = f".{format_name}"

        # Build filename
        default_name = "export"
        if self.current_file:
            default_name = self.current_file.replace('.md', '')

        # Ask for save location
        filename = filedialog.asksaveasfilename(
            title=f"Export to {format_name.upper()}",
            defaultextension=format_ext,
            filetypes=[(f"{format_name.upper()} files", f"*{format_ext}"),
                      ("All files", "*.*")],
            initialdir=self.file_manager.folder_path,
            initialfile=f"{default_name}{format_ext}"
        )

        if not filename:
            return

        # Export in thread to avoid blocking UI
        def do_export():
            try:
                content = self.editor.get(1.0, tk.END)
                self.exporter.export(content, filename, format_name)

                # Show success in main thread
                self.root.after(0, lambda: messagebox.showinfo(
                    "Export Complete",
                    f"File exported successfully to:\n{filename}"
                ))

            except Exception as e:
                self.root.after(0, lambda err=e: messagebox.showerror(
                    "Export Error",
                    f"Failed to export: {err}"
                ))

        # Run export in background
        threading.Thread(target=do_export, daemon=True).start()

    def find(self):
        """Find text in editor"""
        # Simple find dialog
        find_dialog = tk.Toplevel(self.root)
        find_dialog.title("Find")
        find_dialog.geometry("300x100")
        find_dialog.transient(self.root)

        tk.Label(find_dialog, text="Find:").pack(pady=5)

        search_var = tk.StringVar()
        search_entry = tk.Entry(find_dialog, textvariable=search_var, width=30)
        search_entry.pack(pady=5)

        def do_find():
            search_text = search_var.get()
            if search_text:
                start = self.editor.search(search_text, "1.0", stopindex=tk.END)
                if start:
                    end = f"{start}+{len(search_text)}c"
                    self.editor.tag_remove("sel", "1.0", tk.END)
                    self.editor.tag_add("sel", start, end)
                    self.editor.mark_set("insert", start)
                    self.editor.see(start)
                    self.editor.focus()

        tk.Button(find_dialog, text="Find", command=do_find).pack(pady=5)

        search_entry.bind('<Return>', lambda e: do_find())
        find_dialog.bind('<Escape>', lambda e: find_dialog.destroy())

        search_entry.focus()

    def undo(self):
        """Undo last edit"""
        try:
            self.editor.edit_undo()
        except tk.TclError:
            pass

    def redo(self):
        """Redo last edit"""
        try:
            self.editor.edit_redo()
        except tk.TclError:
            pass

    def cut(self):
        """Cut selected text"""
        self.editor.event_generate('<<Cut>>')

    def copy(self):
        """Copy selected text"""
        self.editor.event_generate('<<Copy>>')

    def paste(self):
        """Paste text"""
        self.editor.event_generate('<<Paste>>')

    def show_about(self):
        """Show about dialog"""
        messagebox.showinfo(
            "About SparkDown",
            "SparkDown - Markdown Editor\n\n"
            "Version 1.0\n\n"
            "A powerful markdown editor with:\n"
            "• File management\n"
            "• View/Edit modes\n"
            "• Live preview\n"
            "• Multiple export formats\n\n"
            "Built with Python and Tkinter"
        )

    def quit_app(self):
        """Quit the application"""
        if self.has_unsaved_changes:
            if not messagebox.askyesno("Unsaved Changes",
                                        "You have unsaved changes. Quit anyway?"):
                return

        self.root.quit()
        self.root.destroy()


def main():
    """Main entry point"""
    root = tk.Tk()
    _app = SparkDownApp(root)  # Store reference to prevent garbage collection
    root.mainloop()


if __name__ == "__main__":
    main()
