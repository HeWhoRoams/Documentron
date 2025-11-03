# Phase 0 Research Tasks: Asset Conversion

## Unknowns to Resolve

1. pyvisio support for .vdx (NEEDS CLARIFICATION)
2. Best practices for python-docx, openpyxl in batch conversion
3. Provenance and stable ID generation for assets
4. File size and error handling patterns for proprietary formats

## Research Tasks

- Research pyvisio or alternatives for Visio (.vdx) conversion
- Find best practices for python-docx in batch docx conversion
- Find best practices for openpyxl in batch xlsx conversion
- Research provenance and stable ID generation for converted assets
- Research robust error handling for encrypted, malformed, or oversized files

## Decision Log


Decision: Use python-docx and openpyxl for docx/xlsx; external tool or custom XML for .vdx; uuid5 for stable IDs; provenance includes file path, hash, timestamp; skip files >50MB or on error.
Rationale: Chosen approach maximizes reliability, leverages mature libraries, ensures traceability and robust error handling.
Alternatives considered: pyVisio (not suitable for .vdx), manual XML parsing, other batch libraries.

---

### 1. pyvisio support for .vdx (NEEDS CLARIFICATION)
Finding: pyVisio is a data visualization library, not a Visio file parser. No Python library currently supports direct .vdx (Visio XML) conversion. Alternatives: Use external tools (e.g., LibreOffice CLI, or custom XML parsing) for .vdx extraction.

### 2. Best practices for python-docx, openpyxl in batch conversion
Finding: Both libraries support batch processing by iterating over files and using their respective APIs. For python-docx, use `Document()` to load and extract text, tables, and metadata. For openpyxl, use `load_workbook()` and iterate over sheets/cells. Use defusedxml for security when processing untrusted files.

### 3. Provenance and stable ID generation for assets
Finding: Use Python's `uuid` module (uuid4 for random, uuid5 for deterministic based on file path/name) to generate stable asset IDs. Record original file path, hash, and conversion timestamp for provenance.

### 4. File size and error handling patterns for proprietary formats
Finding: For python-docx/openpyxl, catch exceptions for encrypted, malformed, or oversized files. Use try/except blocks and log actionable reasons (e.g., "encrypted", "parse_error", "oversized"). For .vdx, validate XML before parsing. Always skip files >50MB.
