# Asset Conversion Module

Converts non-code assets (docx, xlsx, vdx) to normalized JSON artifacts for LLM consumption.

## Usage

```bash
python -m Documentron.core.asset_conversion.main /path/to/repo
```

## Supported Formats

- **DOCX**: Microsoft Word documents → text content, tables, metadata
- **XLSX**: Microsoft Excel spreadsheets → sheet data, cell values
- **VDX**: Microsoft Visio diagrams → page/shapes XML structure

## Output

JSON artifacts are written to `Documentron/artifacts/assets/` with stable IDs and provenance.

## Requirements

- python-docx
- openpyxl
- defusedxml
- jsonschema
- pytest (for testing)