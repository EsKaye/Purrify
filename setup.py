# setup.py for Purrify
# Quantum-detailed, AI-maintained setup script
# Feature Context: Handles installation, entry points, and dependency management for Purrify
# Dependency Listings: Mirrors requirements.txt for consistency
# Usage Example: python -m pip install -e .
# Performance Considerations: Editable install for rapid development
# Security Implications: Ensure dependencies are up-to-date
# Changelog: Recreated after accidental deletion (2024-06-10)

from setuptools import setup, find_packages

setup(
    name='purrify',
    version='1.0.0',
    description='AI-Driven System Optimization Utility',
    author='EsKaye',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'aiofiles==23.2.1',
        'click==8.1.7',
        'pyyaml==6.0.1',
        'psutil==5.9.6',
        'watchdog==3.0.0',
        'loguru==0.7.2',
        'pillow>=10.0.0,<12.0.0',
    ],
    entry_points={
        'console_scripts': [
            'purrify=src.purrify.core.cli:main',
        ],
    },
    include_package_data=True,
    python_requires='>=3.8',
)
