"""
Tests for Artifact Writer
"""

import json
import tempfile
import pytest
from pathlib import Path
from Documentron.core.asset_conversion.writer import write_asset_artifact
from Documentron.core.asset_conversion.validation import validate_asset_json

def test_write_asset_artifact():
    """Test writing a valid asset artifact."""
    with tempfile.TemporaryDirectory() as temp_dir:
        output_dir = Path(temp_dir)
        original_path = Path("/test/file.docx")
        file_hash = "test_hash"
        file_type = "docx"
        content = {"title": "Test Document", "text_content": []}
        provenance = {"converter_version": "1.0.0", "library_versions": {"test": "1.0"}}

        result_path = write_asset_artifact(
            output_dir=output_dir,
            original_path=original_path,
            file_hash=file_hash,
            file_type=file_type,
            content=content,
            provenance=provenance
        )

        # Check that file was created
        assert result_path.exists()
        assert result_path.name.endswith('.json')

        # Check content
        with open(result_path, 'r') as f:
            data = json.load(f)

        assert data["asset_id"]
        assert data["original_path"] == str(original_path)
        assert data["file_hash"] == file_hash
        assert data["file_type"] == file_type
        assert data["content"] == content
        assert data["provenance"] == provenance
        assert "conversion_timestamp" in data

        # Validate against schema
        assert validate_asset_json(data) is None