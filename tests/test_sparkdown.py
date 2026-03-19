"""
Unit tests for the SparkDown main application
"""

import os
import shutil
import sys
import tempfile
import tkinter as tk
import unittest
from unittest.mock import Mock, patch

# Add parent directory and src to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src'))


class TestSparkDownApp(unittest.TestCase):
    """Test cases for SparkDownApp class"""

    def setUp(self):
        """Set up test fixtures"""
        # Create a mock root window
        self.mock_root = Mock()
        self.mock_root.title = Mock()
        self.mock_root.geometry = Mock()
        self.mock_root.minsize = Mock()
        self.mock_root.configure = Mock()
        self.mock_root.bind = Mock()
        self.mock_root.protocol = Mock()

        # Mock the Tkinter widgets that are created in __init__
        with patch('tkinter.ttk.Style'):
            with patch('tkinter.ttk.PanedWindow'):
                with patch('tkinter.Menu'):
                    with patch('tkinter.Frame'):
                        with patch('tkinter.Text'):
                            with patch('tkinter.Scrollbar'):
                                with patch('tkinter.Label'):
                                    with patch('tkinter.Button'):
                                        # Import after mocking
                                        from exporter import Exporter
                                        from file_manager import FileManager
                                        from renderer import MarkdownRenderer
                                        from sparkdown import SparkDownApp

                                        self.app = SparkDownApp.__new__(SparkDownApp)
                                        self.app.root = self.mock_root

                                        # Initialize required components for tests
                                        self.app.file_manager = FileManager()
                                        self.app.renderer = MarkdownRenderer()
                                        self.app.exporter = Exporter(self.app.renderer)

    def test_app_initialization(self):
        """Test that app initializes with default values"""
        # Test that the app has the expected attributes
        self.assertIsNotNone(self.app.root)
        self.assertIsNone(self.app.current_file)
        self.assertFalse(self.app.has_unsaved_changes)
        self.assertFalse(self.app.content_modified)

    def test_default_folder_path(self):
        """Test that default folder path is set"""
        self.assertIn('SparkDown', self.app.file_manager.folder_path)

    def test_renderer_initialized(self):
        """Test that renderer is initialized"""
        self.assertIsNotNone(self.app.renderer)

    def test_exporter_initialized(self):
        """Test that exporter is initialized"""
        self.assertIsNotNone(self.app.exporter)

    def test_file_manager_initialized(self):
        """Test that file manager is initialized"""
        self.assertIsNotNone(self.app.file_manager)


class TestSparkDownAppMethods(unittest.TestCase):
    """Test cases for SparkDownApp methods"""

    def setUp(self):
        """Set up test fixtures"""
        # Create a temporary directory for testing
        self.temp_dir = tempfile.mkdtemp()

        # Mock the root
        self.mock_root = Mock()

        # Patch all tkinter components
        self.patches = [
            patch('tkinter.ttk.Style'),
            patch('tkinter.ttk.PanedWindow'),
            patch('tkinter.Menu'),
            patch('tkinter.Frame'),
            patch('tkinter.Text'),
            patch('tkinter.Scrollbar'),
            patch('tkinter.Label'),
            patch('tkinter.Button'),
            patch('tkinter.scrolledtext.ScrolledText'),
        ]

        for p in self.patches:
            p.start()

        # Create app with mocked components
        from sparkdown import SparkDownApp
        self.app = SparkDownApp.__new__(SparkDownApp)
        self.app.root = self.mock_root
        self.app.temp_dir = self.temp_dir

        # Create real components
        from exporter import Exporter
        from file_manager import FileManager
        from renderer import MarkdownRenderer

        self.app.file_manager = FileManager(self.temp_dir)
        self.app.renderer = MarkdownRenderer()
        self.app.exporter = Exporter(self.app.renderer)

        # Initialize state
        self.app.current_file = None
        self.app.has_unsaved_changes = False
        self.app.content_modified = False
        self.app.is_edit_mode = True

        # Mock the editor and preview widgets
        self.mock_editor = Mock()
        self.mock_editor.get = Mock(return_value="# Test\n\nHello world")
        self.mock_editor.insert = Mock()
        self.mock_editor.delete = Mock()
        self.mock_editor.edit_modified = Mock(return_value=False)
        self.mock_editor.pack = Mock()
        self.mock_editor.config = Mock()
        self.mock_editor.focus = Mock()
        self.mock_editor.yview = Mock()

        self.mock_preview = Mock()
        self.mock_preview.get = Mock()
        self.mock_preview.insert = Mock()
        self.mock_preview.delete = Mock()
        self.mock_preview.config = Mock()
        self.mock_preview.pack = Mock()
        self.mock_preview.pack_forget = Mock()
        self.mock_preview.tag_configure = Mock()
        self.mock_preview.tag_add = Mock()

        # Mock frames
        self.mock_editor_frame = Mock()
        self.mock_editor_frame.pack = Mock()
        self.mock_editor_frame.pack_forget = Mock()

        self.mock_preview_frame = Mock()
        self.mock_preview_frame.pack = Mock()
        self.mock_preview_frame.pack_forget = Mock()

        # Assign mocks to app
        self.app.editor = self.mock_editor
        self.app.preview = self.mock_preview
        self.app.editor_frame = self.mock_editor_frame
        self.app.preview_frame = self.mock_preview_frame

        # Mock buttons and labels
        self.app.btn_toggle = Mock()
        self.app.toggle_btn = Mock()
        self.app.mode_label = Mock()
        self.app.status_mode = Mock()
        self.app.unsaved_label = Mock()

        # Mock colors
        self.app.colors = {
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

    def tearDown(self):
        """Clean up test fixtures"""
        for p in self.patches:
            p.stop()

        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def test_show_welcome(self):
        """Test showing welcome content"""
        # Mock necessary components
        self.app.editor = Mock()
        self.app.editor.insert = Mock()
        self.app.editor.delete = Mock()

        self.app.root = Mock()
        self.app.root.title = Mock()

        self.app.file_manager = Mock()

        # Create mock frames
        self.app.editor_frame = Mock()
        self.app.editor_frame.pack = Mock()

        self.app.preview_frame = Mock()
        self.app.preview_frame.pack_forget = Mock()

        # Call show_welcome
        self.app.show_welcome()

        # Verify editor was cleared and populated
        self.app.editor.delete.assert_called()
        self.app.editor.insert.assert_called()

    def test_update_title_no_file(self):
        """Test updating title when no file is open"""
        self.app.current_file = None
        self.app.has_unsaved_changes = False

        self.app.root = Mock()
        self.app.root.title = Mock()

        self.app.update_title()

        self.app.root.title.assert_called_with("SparkDown")

    def test_update_title_with_file(self):
        """Test updating title with a file open"""
        self.app.current_file = "test.md"
        self.app.has_unsaved_changes = False

        self.app.root = Mock()
        self.app.root.title = Mock()

        self.app.update_title()

        self.app.root.title.assert_called_with("test.md - SparkDown")

    def test_update_title_unsaved_changes(self):
        """Test updating title with unsaved changes"""
        self.app.current_file = "test.md"
        self.app.has_unsaved_changes = True

        self.app.root = Mock()
        self.app.root.title = Mock()

        self.app.update_title()

        self.app.root.title.assert_called_with("● test.md - SparkDown")

    def test_update_word_count(self):
        """Test updating word count"""
        self.app.editor = Mock()
        self.app.editor.get = Mock(return_value="Hello world test")

        # Mock status_words label
        self.app.status_words = Mock()
        self.app.status_words.config = Mock()

        self.app.update_word_count()

        # Verify config was called
        self.app.status_words.config.assert_called()

    def test_refresh_file_list(self):
        """Test refreshing the file list"""
        # Create test file
        test_file = os.path.join(self.temp_dir, 'test.md')
        with open(test_file, 'w') as f:
            f.write("# Test")

        # Mock file_listbox
        self.app.file_listbox = Mock()
        self.app.file_listbox.delete = Mock()
        self.app.file_listbox.insert = Mock()

        # Create real file manager
        from file_manager import FileManager
        self.app.file_manager = FileManager(self.temp_dir)

        self.app.refresh_file_list()

        # Verify file list was updated
        self.app.file_listbox.delete.assert_called_with(0, tk.END)
        self.app.file_listbox.insert.assert_called()


class TestSparkDownPreview(unittest.TestCase):
    """Test cases for preview functionality"""

    def setUp(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()

        # Mock root
        self.mock_root = Mock()

        # Patch tkinter
        self.patches = [
            patch('tkinter.ttk.Style'),
            patch('tkinter.ttk.PanedWindow'),
            patch('tkinter.Menu'),
            patch('tkinter.Frame'),
            patch('tkinter.Text'),
            patch('tkinter.Scrollbar'),
            patch('tkinter.Label'),
            patch('tkinter.Button'),
        ]

        for p in self.patches:
            p.start()

        from sparkdown import SparkDownApp
        self.app = SparkDownApp.__new__(SparkDownApp)

        # Setup mocks
        self.mock_editor = Mock()
        self.mock_editor.get = Mock(return_value="# Header\n\nSome **bold** text")

        self.mock_preview = Mock()
        self.mock_preview.config = Mock()
        self.mock_preview.delete = Mock()
        self.mock_preview.insert = Mock()
        self.mock_preview.tag_configure = Mock()
        self.mock_preview.tag_add = Mock()
        self.mock_preview.index = Mock(return_value="1.0")

        self.mock_editor_frame = Mock()
        self.mock_editor_frame.pack_forget = Mock()
        self.mock_editor_frame.pack = Mock()

        self.mock_preview_frame = Mock()
        self.mock_preview_frame.pack = Mock()

        self.app.editor = self.mock_editor
        self.app.preview = self.mock_preview
        self.app.editor_frame = self.mock_editor_frame
        self.app.preview_frame = self.mock_preview_frame

        # Mock buttons and labels
        self.app.btn_toggle = Mock()
        self.app.btn_toggle.config = Mock()
        self.app.toggle_btn = Mock()
        self.app.toggle_btn.config = Mock()
        self.app.mode_label = Mock()
        self.app.mode_label.config = Mock()
        self.app.status_mode = Mock()
        self.app.status_mode.config = Mock()

        self.app.colors = {
            'bg_primary': '#1E1E1E',
            'bg_secondary': '#252526',
            'bg_tertiary': '#2D2D2D',
            'accent': '#007ACC',
            'success': '#4EC9B0',
            'heading_color': '#569CD6',
            'link_color': '#4EC9B0',
            'code_color': '#CE9178',
            'text_secondary': '#808080',
            'border': '#3C3C3C'
        }

        self.app.is_edit_mode = True
        self.app.current_file = None

    def tearDown(self):
        """Clean up test fixtures"""
        for p in self.patches:
            p.stop()

        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def test_show_preview_switches_to_view_mode(self):
        """Test that show_preview switches to view mode"""
        self.app.show_preview()

        self.assertFalse(self.app.is_edit_mode)

    def test_show_preview_gets_content(self):
        """Test that show_preview gets content from editor"""
        self.app.show_preview()

        self.mock_editor.get.assert_called()

    def test_show_preview_configures_preview(self):
        """Test that show_preview configures the preview widget"""
        self.app.show_preview()

        # Verify preview was configured
        self.mock_preview.config.assert_called()

    def test_setup_preview_tags(self):
        """Test that preview tags are configured"""
        self.app._setup_preview_tags()

        # Verify tag_configure was called multiple times
        self.mock_preview.tag_configure.assert_called()

    def test_render_markdown(self):
        """Test markdown rendering"""
        content = "# Test\n\nHello world"
        self.app._render_markdown(content)

        # Verify preview was populated
        self.mock_preview.insert.assert_called()


class TestSparkDownFileOperations(unittest.TestCase):
    """Test cases for file operations"""

    def setUp(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()

        # Patch tkinter
        self.patches = [
            patch('tkinter.ttk.Style'),
            patch('tkinter.ttk.PanedWindow'),
            patch('tkinter.Menu'),
            patch('tkinter.Frame'),
            patch('tkinter.Text'),
            patch('tkinter.Scrollbar'),
            patch('tkinter.Label'),
            patch('tkinter.Button'),
        ]

        for p in self.patches:
            p.start()

        from sparkdown import SparkDownApp
        self.app = SparkDownApp.__new__(SparkDownApp)

        # Setup file manager with temp directory
        from file_manager import FileManager
        self.app.file_manager = FileManager(self.temp_dir)

        # Setup mocks
        self.mock_editor = Mock()
        self.mock_editor.delete = Mock()
        self.mock_editor.insert = Mock()
        self.mock_editor.edit_modified = Mock(return_value=False)
        self.mock_editor.get = Mock(return_value="")

        self.mock_root = Mock()
        self.mock_root.title = Mock()

        self.mock_unsaved_label = Mock()
        self.mock_unsaved_label.config = Mock()

        self.mock_preview_frame = Mock()
        self.mock_preview_frame.pack_forget = Mock()

        self.mock_editor_frame = Mock()
        self.mock_editor_frame.pack = Mock()

        self.mock_btn_toggle = Mock()
        self.mock_btn_toggle.config = Mock()

        self.mock_toggle_btn = Mock()
        self.mock_toggle_btn.config = Mock()

        self.mock_mode_label = Mock()
        self.mock_mode_label.config = Mock()

        self.mock_status_mode = Mock()
        self.mock_status_mode.config = Mock()

        self.mock_status_words = Mock()
        self.mock_status_words.config = Mock()

        # Setup renderer mock
        from renderer import MarkdownRenderer
        self.app.renderer = MarkdownRenderer()

        self.app.editor = self.mock_editor
        self.app.root = self.mock_root
        self.app.unsaved_label = self.mock_unsaved_label
        self.app.preview_frame = self.mock_preview_frame
        self.app.editor_frame = self.mock_editor_frame
        self.app.btn_toggle = self.mock_btn_toggle
        self.app.toggle_btn = self.mock_toggle_btn
        self.app.mode_label = self.mock_mode_label
        self.app.status_mode = self.mock_status_mode
        self.app.status_words = self.mock_status_words
        self.app.current_file = None
        self.app.has_unsaved_changes = False
        self.app.colors = {'success': '#4EC9B0'}

    def tearDown(self):
        """Clean up test fixtures"""
        for p in self.patches:
            p.stop()

        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def test_new_file(self):
        """Test creating a new file"""
        self.app.new_file()

        # Verify editor was cleared
        self.mock_editor.delete.assert_called()

        # Verify state was reset
        self.assertIsNone(self.app.current_file)
        self.assertFalse(self.app.has_unsaved_changes)

    def test_write_and_read_file(self):
        """Test writing and reading a file"""
        # Mock the editor to return content
        self.mock_editor.get = Mock(return_value="# Test Content")

        filename = self.app.file_manager.write_file('test.md', '# Test Content')

        self.assertEqual(filename, 'test.md')

        content = self.app.file_manager.read_file('test.md')
        self.assertEqual(content, '# Test Content')


if __name__ == '__main__':
    unittest.main()
