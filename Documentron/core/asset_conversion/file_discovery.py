"""
Batch File Discovery for Asset Conversion

Scans a repository for supported asset files (docx, xlsx, vdx).
"""

import os
from pathlib import Path
from typing import List

SUPPORTED_EXTENSIONS = {'.docx', '.xlsx', '.vdx'}
EXCLUDED_DIRS = {'.git', '.venv', '__pycache__', 'node_modules', '.specify'}

def discover_asset_files(repo_path: Path) -> List[Path]:
    """
    Discover all supported asset files in the repository.

    Args:
        repo_path: Root path of the repository to scan

    Returns:
        List of absolute paths to supported asset files
    """
    asset_files = []

    for root, dirs, files in os.walk(repo_path):
        # Skip excluded directories
        dirs[:] = [d for d in dirs if d not in EXCLUDED_DIRS]

        for file in files:
            file_path = Path(root) / file
            if file_path.suffix.lower() in SUPPORTED_EXTENSIONS:
                asset_files.append(file_path.resolve())

    return sorted(asset_files)