"""
VDX Converter

Converts Microsoft Visio diagrams (.vdx) to normalized content.
.vdx files are XML-based, so we parse the XML structure.
"""

import hashlib
from pathlib import Path
from typing import Dict, Any, List
from defusedxml import ElementTree as ET

from .error_handling import MalformedFileError, EncryptedFileError, FileTooLargeError, report_skipped_file
from .provenance import get_library_versions

def calculate_file_hash(file_path: Path) -> str:
    """Calculate SHA256 hash of a file."""
    hash_sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_sha256.update(chunk)
    return hash_sha256.hexdigest()

def extract_vdx_content(file_path: Path, max_size: int) -> Dict[str, Any]:
    """
    Extract content from a VDX file.

    Args:
        file_path: Path to the VDX file
        max_size: Maximum file size in bytes

    Returns:
        Dictionary with extracted content

    Raises:
        FileTooLargeError: If file exceeds max_size
        EncryptedFileError: If file is password-protected
        MalformedFileError: If file cannot be parsed
    """
    if file_path.stat().st_size > max_size:
        raise FileTooLargeError(f"File size {file_path.stat().st_size} exceeds limit {max_size}")

    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
    except Exception as e:
        raise MalformedFileError(f"Cannot parse VDX file: {e}")

    content = {
        "pages": [],
        "shapes": [],
        "metadata": {}
    }

    # Visio XML namespace
    ns = {'v': 'http://schemas.microsoft.com/visio/2003/core'}

    # Extract pages
    pages = root.findall('.//v:Page', ns)
    for page in pages:
        page_data = {
            "name": page.get('Name', 'Unnamed Page'),
            "shapes": []
        }

        # Extract shapes in this page
        shapes = page.findall('.//v:Shape', ns)
        for shape in shapes:
            shape_data = {
                "id": shape.get('ID'),
                "type": shape.get('Type'),
                "text": ""
            }

            # Extract text
            text_elem = shape.find('.//v:Text', ns)
            if text_elem is not None:
                shape_data["text"] = ''.join(text_elem.itertext()).strip()

            page_data["shapes"].append(shape_data)
            content["shapes"].append(shape_data)

        content["pages"].append(page_data)

    # Extract basic metadata
    content["metadata"] = {
        "page_count": len(pages),
        "total_shapes": len(content["shapes"])
    }

    return content

def convert_vdx_file(file_path: Path, output_dir: Path, max_size: int) -> Path:
    """
    Convert a single VDX file to JSON artifact.

    Args:
        file_path: Path to the VDX file
        output_dir: Output directory for artifacts
        max_size: Maximum file size

    Returns:
        Path to the created JSON artifact
    """
    try:
        file_hash = calculate_file_hash(file_path)
        content = extract_vdx_content(file_path, max_size)

        provenance = {
            "converter_version": "1.0.0",
            "library_versions": get_library_versions()
        }

        from .writer import write_asset_artifact
        return write_asset_artifact(
            output_dir=output_dir,
            original_path=file_path,
            file_hash=file_hash,
            file_type="vdx",
            content=content,
            provenance=provenance
        )

    except (FileTooLargeError, EncryptedFileError, MalformedFileError) as e:
        report_skipped_file(file_path, type(e).__name__.replace('Error', '').lower(), str(e))
        raise