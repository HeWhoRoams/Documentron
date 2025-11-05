"""
Provenance and Stable ID Generation

Handles generation of stable asset IDs and provenance tracking.
"""

import uuid
from pathlib import Path

def generate_stable_asset_id(original_path: Path, file_hash: str) -> str:
    """
    Generate a stable UUID for an asset based on its path and hash.

    Args:
        original_path: Original file path
        file_hash: SHA256 hash of the file

    Returns:
        Stable UUID string
    """
    # Use UUID5 with namespace based on path and hash for stability
    namespace = uuid.NAMESPACE_URL
    name = f"{original_path}:{file_hash}"
    return str(uuid.uuid5(namespace, name))

def get_library_versions() -> dict:
    """
    Get versions of libraries used for conversion.

    Returns:
        Dictionary of library names to versions
    """
    # TODO: Dynamically get versions
    return {
        "python-docx": "1.1.0",
        "openpyxl": "3.1.2",
        "defusedxml": "0.7.1",
        "jsonschema": "4.17.0"
    }