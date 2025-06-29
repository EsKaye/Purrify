#!/usr/bin/env python3
"""
Purrify - AI-Driven System Optimization Utility
Setup script for building and packaging the application.
"""

import os
import sys
import platform
from setuptools import setup, find_packages
from setuptools.command.install import install
from setuptools.command.develop import develop

# Read the README file for long description
def read_readme():
    """Read README.md file for long description."""
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Read requirements from requirements.txt
def read_requirements():
    """Read requirements from requirements.txt file."""
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        install.run(self)
        self._post_install()

class PostDevelopCommand(develop):
    """Post-installation for development mode."""
    def run(self):
        develop.run(self)
        self._post_install()

    def _post_install(self):
        """Post-installation tasks."""
        print("🐱 Purrify installation completed!")
        print("📝 Run 'purrify --help' to see available commands")
        print("🎮 Run 'purrify gui' to launch the graphical interface")

# Package configuration
setup(
    name="purrify",
    version="1.0.0",
    author="Purrify Team",
    author_email="team@purrify.app",
    description="AI-Driven System Optimization Utility for macOS and Windows",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/your-username/purrify",
    project_urls={
        "Bug Tracker": "https://github.com/your-username/purrify/issues",
        "Documentation": "https://github.com/your-username/purrify/wiki",
        "Source Code": "https://github.com/your-username/purrify",
    },
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Topic :: System :: Systems Administration",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-asyncio>=0.21.1",
            "pytest-cov>=4.1.0",
            "black>=23.7.0",
            "flake8>=6.0.0",
            "mypy>=1.5.1",
            "pre-commit>=3.3.3",
        ],
        "gui": [
            "customtkinter>=5.2.0",
            "pillow>=10.0.0",
        ],
        "ai": [
            "tensorflow>=2.13.0",
            "torch>=2.0.1",
            "transformers>=4.31.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "purrify=purrify.main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "purrify": [
            "config/*.yaml",
            "resources/*",
            "models/*.pkl",
            "models/*.h5",
        ],
    },
    cmdclass={
        "install": PostInstallCommand,
        "develop": PostDevelopCommand,
    },
    keywords=[
        "system optimization",
        "cache cleaning",
        "performance",
        "macos",
        "windows",
        "ai",
        "machine learning",
        "utility",
    ],
    platforms=["Windows", "macOS"],
    zip_safe=False,
) 