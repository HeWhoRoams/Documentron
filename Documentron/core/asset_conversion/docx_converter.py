"""
DOCX Converter

Converts Microsoft Word documents (.docx) to normalized content.

Notes:
- Avoids python-docx/lxml to prevent native crashes on some Windows setups.
- Parses the underlying OOXML with defusedxml for safety and stability.
"""

import hashlib
import zipfile
from pathlib import Path
from typing import Dict, Any
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

def extract_docx_content(file_path: Path, max_size: int) -> Dict[str, Any]:
    """
    Extract content from a DOCX file.

    Args:
        file_path: Path to the DOCX file
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

    # Open as zip and parse core document XML
    try:
        with zipfile.ZipFile(file_path, 'r') as zf:
            try:
                doc_xml = zf.read('word/document.xml')
            except KeyError:
                # Minimal/empty docx or corrupted
                raise MalformedFileError("Missing word/document.xml in DOCX")
    except RuntimeError as e:
        # Bad zip or encrypted container
        msg = str(e).lower()
        if "encrypted" in msg or "password" in msg:
            raise EncryptedFileError(f"File appears to be encrypted: {e}")
        raise MalformedFileError(f"Cannot open DOCX as zip: {e}")
    except zipfile.BadZipFile as e:
        raise MalformedFileError(f"Invalid DOCX (bad zip): {e}")

    try:
        root = ET.fromstring(doc_xml)
    except Exception as e:
        raise MalformedFileError(f"Cannot parse DOCX XML: {e}")

    # Namespaces used in WordprocessingML
    ns = {
        'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
    }

    content = {
        "title": "",
        "text_content": [],
        "tables": [],
        "metadata": {}
    }

    # Helper to extract all text from a paragraph or cell
    def _collect_text(elem) -> str:
        parts = []
        for t in elem.findall('.//w:t', ns):
            # t.text may be None
            parts.append(t.text or '')
        return ''.join(parts).strip()

    # Paragraphs
    paragraphs = root.findall('.//w:p', ns)
    for p in paragraphs:
        text = _collect_text(p)
        if not text:
            continue
        # Determine style name if present
        style = "Normal"
        ppr = p.find('w:pPr', ns)
        if ppr is not None:
            pstyle = ppr.find('w:pStyle', ns)
            if pstyle is not None:
                val = pstyle.attrib.get(f'{{{ns["w"]}}}val')
                if val:
                    style = val
        content["text_content"].append({
            "text": text,
            "style": style
        })

    # Title: first heading paragraph if present
    for item in content["text_content"]:
        st = item.get("style") or ""
        if st.startswith("Heading"):
            content["title"] = item["text"]
            break

    # Tables (rows/cells)
    tables = root.findall('.//w:tbl', ns)
    for tbl in tables:
        table_data = []
        for tr in tbl.findall('w:tr', ns):
            row = []
            for tc in tr.findall('w:tc', ns):
                row.append(_collect_text(tc))
            # Include row if non-empty
            if any(c for c in row):
                table_data.append(row)
        if table_data:
            content["tables"].append(table_data)

    # Basic metadata
    word_count = sum(len(item["text"].split()) for item in content["text_content"]) if content["text_content"] else 0
    content["metadata"] = {
        "word_count": word_count,
        "paragraph_count": len(content["text_content"]),
        "table_count": len(content["tables"]) if isinstance(content.get("tables"), list) else 0
    }

    return content

def convert_docx_file(file_path: Path, output_dir: Path, max_size: int) -> Path:
    """
    Convert a single DOCX file to JSON artifact.

    Args:
        file_path: Path to the DOCX file
        output_dir: Output directory for artifacts
        max_size: Maximum file size

    Returns:
        Path to the created JSON artifact
    """
    try:
        file_hash = calculate_file_hash(file_path)
        content = extract_docx_content(file_path, max_size)

        provenance = {
            "converter_version": "1.0.0",
            "library_versions": get_library_versions()
        }

        from .writer import write_asset_artifact
        return write_asset_artifact(
            output_dir=output_dir,
            original_path=file_path,
            file_hash=file_hash,
            file_type="docx",
            content=content,
            provenance=provenance
        )

    except (FileTooLargeError, EncryptedFileError, MalformedFileError) as e:
        report_skipped_file(file_path, type(e).__name__.replace('Error', '').lower(), str(e))
        raise
