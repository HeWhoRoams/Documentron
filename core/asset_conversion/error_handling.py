"""
Error Handling for Asset Conversion

Defines exceptions and error reporting for asset conversion issues.
"""

import sys
from pathlib import Path
from typing import Dict, Any, List

class AssetConversionError(Exception):
    """Base exception for asset conversion errors."""
    pass

class FileTooLargeError(AssetConversionError):
    """Raised when a file exceeds the maximum allowed size."""
    pass

class EncryptedFileError(AssetConversionError):
    """Raised when a file is encrypted or password-protected."""
    pass

class MalformedFileError(AssetConversionError):
    """Raised when a file is malformed or cannot be parsed."""
    pass

class UnsupportedFileError(AssetConversionError):
    """Raised when a file type is not supported."""
    pass

def report_skipped_file(file_path: Path, reason: str, details: str = "") -> None:
    """
    Report a file that was skipped during conversion.

    Args:
        file_path: Path to the skipped file
        reason: Short reason code (e.g., "encrypted", "oversized")
        details: Additional details about why it was skipped
    """
    # Normalize path for cross-platform stable output (tests expect POSIX-style)
    safe_path = file_path.as_posix() if isinstance(file_path, Path) else str(file_path)
    message = f"Skipped {safe_path}: {reason}"
    if details:
        message += f" ({details})"
    print(message, file=sys.stderr)

def collect_conversion_errors() -> List[Dict[str, Any]]:
    """
    Collect and return a summary of conversion errors.

    Returns:
        List of error dictionaries with file_path, error_type, and message
    """
    # TODO: Implement error collection mechanism
    # For now, return empty list
    return []
