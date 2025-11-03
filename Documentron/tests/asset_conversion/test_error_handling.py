"""
Tests for Error Handling
"""

import pytest
from pathlib import Path
from unittest.mock import patch
from Documentron.core.asset_conversion.error_handling import (
    FileTooLargeError, EncryptedFileError, MalformedFileError,
    UnsupportedFileError, report_skipped_file
)
from Documentron.core.asset_conversion.docx_converter import convert_docx_file
from Documentron.core.asset_conversion.xlsx_converter import convert_xlsx_file

def test_file_too_large_error():
    """Test that oversized files raise FileTooLargeError."""
    # Create a mock file path that reports large size
    with patch('pathlib.Path.stat') as mock_stat:
        mock_stat.return_value.st_size = 100 * 1024 * 1024  # 100MB

        with pytest.raises(FileTooLargeError):
            from Documentron.core.asset_conversion.docx_converter import extract_docx_content
            extract_docx_content(Path("/fake/file.docx"), 50 * 1024 * 1024)  # 50MB limit

def test_report_skipped_file(capsys):
    """Test that skipped files are reported to stderr."""
    test_path = Path("/test/file.docx")
    report_skipped_file(test_path, "encrypted", "password protected")

    captured = capsys.readouterr()
    assert "Skipped /test/file.docx: encrypted (password protected)" in captured.err

def test_unsupported_file_type():
    """Test that unsupported file types are skipped."""
    # This would be tested in main.py integration
    # For now, just check the logic exists
    from Documentron.core.asset_conversion.main import main
    # TODO: Add integration test when sample files are available
    pass