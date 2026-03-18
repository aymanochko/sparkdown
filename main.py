#!/usr/bin/env python3
"""
SparkDown - Main Entry Point
A feature-rich markdown editor with file management and export capabilities
"""

import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import and run the application
from sparkdown import main

if __name__ == "__main__":
    main()
