"""
Artifact Writer for Normalized JSON Output

Writes converted asset data to JSON files in the artifacts directory.
"""

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any

from .validation import validate_asset_json

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

def write_asset_artifact(
    output_dir: Path,
    original_path: Path,
    file_hash: str,
    file_type: str,
    content: Dict[str, Any],
    provenance: Dict[str, Any]
) -> Path:
    """
    Write a normalized asset artifact to JSON.

    Args:
        output_dir: Directory to write artifacts
        original_path: Original file path
        file_hash: SHA256 hash of the file
        file_type: Type of file (docx, xlsx, vdx)
        content: Extracted content
        provenance: Provenance information

    Returns:
        Path to the written JSON file
    """
    asset_id = generate_stable_asset_id(original_path, file_hash)

    artifact_data = {
        "asset_id": asset_id,
        "original_path": str(original_path),
        "file_hash": file_hash,
        "conversion_timestamp": datetime.now(timezone.utc).isoformat(),
        "file_type": file_type,
        "content": content,
        "provenance": provenance
    }

    # Validate before writing
    error = validate_asset_json(artifact_data)
    if error:
        raise ValueError(f"Invalid artifact data: {error}")

    # Create output filename: asset_id.json
    output_file = output_dir / f"{asset_id}.json"

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(artifact_data, f, indent=2, ensure_ascii=False)

    return output_file