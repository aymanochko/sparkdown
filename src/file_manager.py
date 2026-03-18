"""
SparkDown - File Manager Module
Handles all file operations: create, read, write, delete, list
"""

import os
import shutil
from pathlib import Path
from datetime import datetime
from typing import List, Optional


class FileManager:
    """Manages file operations for markdown files"""
    
    def __init__(self, base_folder: Optional[str] = None):
        """Initialize file manager with base folder"""
        if base_folder is None:
            # Default to Documents/SparkDown
            self.base_folder = Path.home() / "Documents" / "SparkDown"
        else:
            self.base_folder = Path(base_folder)
        
        self.ensure_folder_exists()
    
    def ensure_folder_exists(self):
        """Create base folder if it doesn't exist"""
        if not self.base_folder.exists():
            self.base_folder.mkdir(parents=True, exist_ok=True)
    
    @property
    def folder_path(self) -> str:
        """Get the current folder path as string"""
        return str(self.base_folder)
    
    def set_folder(self, folder_path: str):
        """Set a new base folder"""
        self.base_folder = Path(folder_path)
        self.ensure_folder_exists()
    
    def list_files(self, pattern: str = "*.md") -> List[str]:
        """List all markdown files in the base folder"""
        if not self.base_folder.exists():
            return []
        
        files = []
        for f in sorted(self.base_folder.glob(pattern)):
            if f.is_file():
                files.append(f.name)
        return files
    
    def get_file_path(self, filename: str) -> Path:
        """Get full path for a filename"""
        return self.base_folder / filename
    
    def file_exists(self, filename: str) -> bool:
        """Check if file exists"""
        return self.get_file_path(filename).exists()
    
    def read_file(self, filename: str) -> str:
        """Read content from a markdown file"""
        file_path = self.get_file_path(filename)
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {filename}")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def write_file(self, filename: str, content: str) -> str:
        """Write content to a markdown file"""
        file_path = self.get_file_path(filename)
        
        # Ensure .md extension
        if not filename.endswith('.md'):
            filename = filename + '.md'
            file_path = self.base_folder / filename
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return filename
    
    def delete_file(self, filename: str) -> bool:
        """Delete a markdown file"""
        file_path = self.get_file_path(filename)
        
        if not file_path.exists():
            return False
        
        try:
            file_path.unlink()
            return True
        except Exception as e:
            raise IOError(f"Failed to delete file: {e}")
    
    def create_backup(self, filename: str) -> Optional[str]:
        """Create a backup of a file"""
        file_path = self.get_file_path(filename)
        
        if not file_path.exists():
            return None
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"{file_path.stem}_backup_{timestamp}{file_path.suffix}"
        backup_path = self.base_folder / backup_name
        
        shutil.copy2(file_path, backup_path)
        return backup_name
    
    def get_file_info(self, filename: str) -> dict:
        """Get file information"""
        file_path = self.get_file_path(filename)
        
        if not file_path.exists():
            return {}
        
        stat = file_path.stat()
        return {
            'name': filename,
            'path': str(file_path),
            'size': stat.st_size,
            'modified': datetime.fromtimestamp(stat.st_mtime),
            'created': datetime.fromtimestamp(stat.st_ctime)
        }
    
    def rename_file(self, old_name: str, new_name: str) -> bool:
        """Rename a file"""
        old_path = self.get_file_path(old_name)
        new_path = self.get_file_path(new_name)
        
        if not old_path.exists():
            return False
        
        # Ensure .md extension
        if not new_name.endswith('.md'):
            new_name = new_name + '.md'
            new_path = self.base_folder / new_name
        
        if new_path.exists():
            return False
        
        old_path.rename(new_path)
        return True
