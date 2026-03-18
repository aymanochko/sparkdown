"""
SparkDown - Setup Configuration
"""

from setuptools import setup, find_packages

setup(
    name="sparkdown",
    version="1.0.0",
    description="A feature-rich markdown editor with file management and export capabilities",
    author="SparkDown Team",
    packages=find_packages(),
    install_requires=[
        "markdown>=3.5",
        "Pygments>=2.17",
    ],
    extras_require={
        "full": [
            "weasyprint>=60.0",
            "pypandoc>=1.13",
            "markdown-it-py>=0.9.0",
            "mdit-py-plugins>=0.4.0",
        ]
    },
    entry_points={
        "console_scripts": [
            "sparkdown=sparkdown:main",
        ],
    },
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
