"""
Tests for Provenance and Stable ID Generation
"""

import pytest
from pathlib import Path
from Documentron.core.asset_conversion.provenance import generate_stable_asset_id, get_library_versions

def test_generate_stable_asset_id():
    """Test that stable asset IDs are generated consistently."""
    path = Path("/test/file.docx")
    hash_value = "abc123"

    # Same inputs should produce same ID
    id1 = generate_stable_asset_id(path, hash_value)
    id2 = generate_stable_asset_id(path, hash_value)
    assert id1 == id2

    # Different path should produce different ID
    different_path = Path("/test/file2.docx")
    id3 = generate_stable_asset_id(different_path, hash_value)
    assert id1 != id3

    # Different hash should produce different ID
    id4 = generate_stable_asset_id(path, "def456")
    assert id1 != id4

    # ID should be a valid UUID string
    import uuid
    uuid.UUID(id1)  # Should not raise

def test_get_library_versions():
    """Test that library versions are returned as a dict."""
    versions = get_library_versions()
    assert isinstance(versions, dict)
    assert "python-docx" in versions
    assert "openpyxl" in versions
    assert "defusedxml" in versions
    assert "jsonschema" in versions