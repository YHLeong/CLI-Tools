#!/usr/bin/env python3
"""
Setup script for the CLI File Manager
"""

from setuptools import setup, find_packages

setup(
    name="advanced-file-manager",
    version="1.0.0",
    description="Advanced CLI File Manager with Rich interface",
    author="Portfolio Developer",
    py_modules=["filemanager"],
    install_requires=[
        "click>=8.0.0",
        "rich>=13.0.0",
    ],
    entry_points={
        "console_scripts": [
            "fm=filemanager:cli",
            "filemanager=filemanager:cli",
        ],
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
)