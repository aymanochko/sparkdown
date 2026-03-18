"""
Unit tests for the FileManager module
"""

import unittest
import tempfile
import shutil
from pathlib import Path
import sys
import os

# Add parent directory and src to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src'))

from file_manager import FileManager


class TestFileManager(unittest.TestCase):
    """Test cases for FileManager class"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Create a temporary directory for testing
        self.temp_dir = tempfile.mkdtemp()
        self.file_manager = FileManager(self.temp_dir)
    
    def tearDown(self):
        """Clean up test fixtures"""
        # Remove the temporary directory
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_default_folder_path(self):
        """Test that default folder path is set correctly"""
        fm = FileManager()
        self.assertIn('SparkDown', fm.folder_path)
    
    def test_custom_folder_path(self):
        """Test that custom folder path is set correctly"""
        fm = FileManager(self.temp_dir)
        self.assertEqual(fm.folder_path, self.temp_dir)
    
    def test_ensure_folder_exists(self):
        """Test that folder is created if it doesn't exist"""
        new_dir = os.path.join(self.temp_dir, 'new_folder')
        fm = FileManager(new_dir)
        self.assertTrue(os.path.exists(new_dir))
    
    def test_set_folder(self):
        """Test setting a new folder"""
        new_dir = os.path.join(self.temp_dir, 'new_folder')
        self.file_manager.set_folder(new_dir)
        self.assertEqual(self.file_manager.folder_path, new_dir)
        self.assertTrue(os.path.exists(new_dir))
    
    def test_list_files_empty_folder(self):
        """Test listing files in empty folder"""
        files = self.file_manager.list_files()
        self.assertEqual(files, [])
    
    def test_list_files_with_markdown_files(self):
        """Test listing markdown files"""
        # Create test files
        test_files = ['test1.md', 'test2.md', 'test3.txt']
        for filename in test_files:
            file_path = os.path.join(self.temp_dir, filename)
            with open(file_path, 'w') as f:
                f.write('# Test')
        
        files = self.file_manager.list_files()
        self.assertEqual(len(files), 2)
        self.assertIn('test1.md', files)
        self.assertIn('test2.md', files)
        self.assertNotIn('test3.txt', files)
    
    def test_get_file_path(self):
        """Test getting full file path"""
        file_path = self.file_manager.get_file_path('test.md')
        expected = os.path.join(self.temp_dir, 'test.md')
        self.assertEqual(str(file_path), expected)
    
    def test_file_exists(self):
        """Test checking if file exists"""
        # File doesn't exist
        self.assertFalse(self.file_manager.file_exists('nonexistent.md'))
        
        # Create file
        file_path = os.path.join(self.temp_dir, 'test.md')
        with open(file_path, 'w') as f:
            f.write('# Test')
        
        # File exists
        self.assertTrue(self.file_manager.file_exists('test.md'))
    
    def test_read_file(self):
        """Test reading file content"""
        # Create test file
        content = '# Hello World\nThis is a test.'
        file_path = os.path.join(self.temp_dir, 'test.md')
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # Read file
        read_content = self.file_manager.read_file('test.md')
        self.assertEqual(read_content, content)
    
    def test_read_nonexistent_file(self):
        """Test reading nonexistent file raises FileNotFoundError"""
        with self.assertRaises(FileNotFoundError):
            self.file_manager.read_file('nonexistent.md')
    
    def test_write_file(self):
        """Test writing content to file"""
        content = '# Test Content'
        filename = self.file_manager.write_file('test.md', content)
        
        self.assertEqual(filename, 'test.md')
        file_path = os.path.join(self.temp_dir, 'test.md')
        self.assertTrue(os.path.exists(file_path))
        
        with open(file_path, 'r') as f:
            self.assertEqual(f.read(), content)
    
    def test_write_file_adds_extension(self):
        """Test that .md extension is added if missing"""
        content = '# Test'
        filename = self.file_manager.write_file('test', content)
        
        self.assertEqual(filename, 'test.md')
        file_path = os.path.join(self.temp_dir, 'test.md')
        self.assertTrue(os.path.exists(file_path))
    
    def test_delete_file(self):
        """Test deleting a file"""
        # Create test file
        file_path = os.path.join(self.temp_dir, 'test.md')
        with open(file_path, 'w') as f:
            f.write('# Test')
        
        # Delete file
        result = self.file_manager.delete_file('test.md')
        self.assertTrue(result)
        self.assertFalse(os.path.exists(file_path))
    
    def test_delete_nonexistent_file(self):
        """Test deleting nonexistent file returns False"""
        result = self.file_manager.delete_file('nonexistent.md')
        self.assertFalse(result)
    
    def test_create_backup(self):
        """Test creating a backup of a file"""
        # Create test file
        content = '# Test Content'
        file_path = os.path.join(self.temp_dir, 'test.md')
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # Create backup
        backup_name = self.file_manager.create_backup('test.md')
        self.assertIsNotNone(backup_name)
        self.assertIn('test_backup_', backup_name)
        self.assertTrue(backup_name.endswith('.md'))
        
        # Check backup file exists
        backup_path = os.path.join(self.temp_dir, backup_name)
        self.assertTrue(os.path.exists(backup_path))
    
    def test_create_backup_nonexistent_file(self):
        """Test creating backup of nonexistent file returns None"""
        backup_name = self.file_manager.create_backup('nonexistent.md')
        self.assertIsNone(backup_name)
    
    def test_get_file_info(self):
        """Test getting file information"""
        # Create test file
        content = '# Test Content'
        file_path = os.path.join(self.temp_dir, 'test.md')
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # Get file info
        info = self.file_manager.get_file_info('test.md')
        
        self.assertEqual(info['name'], 'test.md')
        self.assertIn('path', info)
        self.assertGreater(info['size'], 0)
        self.assertIn('modified', info)
        self.assertIn('created', info)
    
    def test_get_file_info_nonexistent(self):
        """Test getting info for nonexistent file returns empty dict"""
        info = self.file_manager.get_file_info('nonexistent.md')
        self.assertEqual(info, {})
    
    def test_rename_file(self):
        """Test renaming a file"""
        # Create test file
        file_path = os.path.join(self.temp_dir, 'test.md')
        with open(file_path, 'w') as f:
            f.write('# Test')
        
        # Rename file
        result = self.file_manager.rename_file('test.md', 'new_test.md')
        
        self.assertTrue(result)
        self.assertTrue(os.path.exists(os.path.join(self.temp_dir, 'new_test.md')))
        self.assertFalse(os.path.exists(file_path))
    
    def test_rename_file_adds_extension(self):
        """Test that .md extension is added if missing when renaming"""
        # Create test file
        file_path = os.path.join(self.temp_dir, 'test.md')
        with open(file_path, 'w') as f:
            f.write('# Test')
        
        # Rename file
        result = self.file_manager.rename_file('test.md', 'new_test')
        
        self.assertTrue(result)
        self.assertTrue(os.path.exists(os.path.join(self.temp_dir, 'new_test.md')))
    
    def test_rename_nonexistent_file(self):
        """Test renaming nonexistent file returns False"""
        result = self.file_manager.rename_file('nonexistent.md', 'new_name.md')
        self.assertFalse(result)
    
    def test_rename_to_existing_file(self):
        """Test renaming to an existing file returns False"""
        # Create two test files
        file1 = os.path.join(self.temp_dir, 'test1.md')
        file2 = os.path.join(self.temp_dir, 'test2.md')
        with open(file1, 'w') as f:
            f.write('# Test 1')
        with open(file2, 'w') as f:
            f.write('# Test 2')
        
        # Try to rename to existing file
        result = self.file_manager.rename_file('test1.md', 'test2.md')
        
        self.assertFalse(result)


class TestFileManagerIntegration(unittest.TestCase):
    """Integration tests for FileManager with file operations"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
        self.file_manager = FileManager(self.temp_dir)
    
    def tearDown(self):
        """Clean up test fixtures"""
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_write_and_read_file(self):
        """Test writing and then reading a file"""
        content = '# Hello World\n\nThis is a **test**.'
        
        filename = self.file_manager.write_file('hello.md', content)
        read_content = self.file_manager.read_file(filename)
        
        self.assertEqual(content, read_content)
    
    def test_multiple_files_operations(self):
        """Test operations on multiple files"""
        files_content = {
            'file1.md': '# File 1',
            'file2.md': '# File 2',
            'file3.md': '# File 3'
        }
        
        # Write multiple files
        for filename, content in files_content.items():
            self.file_manager.write_file(filename, content)
        
        # List files
        files = self.file_manager.list_files()
        self.assertEqual(len(files), 3)
        
        # Read each file
        for filename, expected_content in files_content.items():
            content = self.file_manager.read_file(filename)
            self.assertEqual(content, expected_content)
    
    def test_delete_and_list(self):
        """Test deleting files and verifying list"""
        # Create files
        self.file_manager.write_file('file1.md', '# File 1')
        self.file_manager.write_file('file2.md', '# File 2')
        
        # Verify files exist
        self.assertEqual(len(self.file_manager.list_files()), 2)
        
        # Delete one file
        self.file_manager.delete_file('file1.md')
        
        # Verify remaining file
        files = self.file_manager.list_files()
        self.assertEqual(len(files), 1)
        self.assertIn('file2.md', files)


if __name__ == '__main__':
    unittest.main()
