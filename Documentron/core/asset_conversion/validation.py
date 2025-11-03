"""
JSON Schema Validation Utilities

Provides validation for normalized asset JSON artifacts.
"""

import json
import sys
from pathlib import Path
from typing import Dict, Any, Optional
from jsonschema import validate, ValidationError

# Schema for normalized asset artifacts
ASSET_SCHEMA = {
    "type": "object",
    "properties": {
        "asset_id": {"type": "string"},
        "original_path": {"type": "string"},
        "file_hash": {"type": "string"},
        "conversion_timestamp": {"type": "string", "format": "date-time"},
        "file_type": {"type": "string", "enum": ["docx", "xlsx", "vdx"]},
        "content": {"type": "object"},  # Specific content schema per type
        "provenance": {
            "type": "object",
            "properties": {
                "converter_version": {"type": "string"},
                "library_versions": {"type": "object"}
            }
        }
    },
    "required": ["asset_id", "original_path", "file_hash", "conversion_timestamp", "file_type", "content"]
}

def validate_asset_json(json_data: Dict[str, Any]) -> Optional[str]:
    """
    Validate asset JSON against the schema.

    Args:
        json_data: The JSON data to validate

    Returns:
        None if valid, error message if invalid
    """
    try:
        validate(instance=json_data, schema=ASSET_SCHEMA)
        return None
    except ValidationError as e:
        return f"Validation error: {e.message}"

def load_and_validate_json(file_path: Path) -> Optional[Dict[str, Any]]:
    """
    Load and validate a JSON file.

    Args:
        file_path: Path to the JSON file

    Returns:
        Parsed JSON data if valid, None if invalid or error
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        error = validate_asset_json(data)
        if error:
            print(f"Invalid JSON in {file_path}: {error}", file=sys.stderr)
            return None
        return data
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error loading {file_path}: {e}", file=sys.stderr)
        return None