"""
Error Handling for Asset Conversion

Defines exceptions and error reporting for asset conversion issues.
"""

import sys
from pathlib import Path
from typing import Dict, Any, List

# Global list to store conversion errors
_conversion_errors: List[Dict[str, Any]] = []

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

class DependencyError(AssetConversionError):
    """Raised when a required dependency is missing."""
    pass

def add_conversion_error(file_path: Path, error_type: str, message: str) -> None:
    """
    Add a conversion error to the global error collection.

    Args:
        file_path: Path to the file that caused the error
        error_type: Type of error (e.g., "file_too_large", "encrypted", "malformed", "unsupported")
        message: Detailed error message
    """
    # Normalize path for cross-platform stable output
    safe_path = file_path.as_posix() if isinstance(file_path, Path) else str(file_path)
    error_entry = {
        "file_path": safe_path,
        "error_type": error_type,
        "message": message
    }
    _conversion_errors.append(error_entry)

def clear_conversion_errors() -> None:
    """
    Clear all collected conversion errors.
    Call this at the start of a new conversion run.
    """
    _conversion_errors.clear()

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
    # Return a copy of the errors to prevent external modification
    return _conversion_errors.copy()
