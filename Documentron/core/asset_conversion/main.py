#!/usr/bin/env python3
"""
Asset Conversion CLI Entry Point

Converts non-code assets (docx, xlsx, vdx) to normalized JSON artifacts.
"""

import argparse
import os
import sys
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(
        description="Convert non-code assets to normalized JSON artifacts"
    )
    parser.add_argument(
        "repo_path",
        type=Path,
        help="Path to the repository to scan for assets"
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("Generated Documentation/assets"),
        help="Output directory for JSON artifacts (default: 'Generated Documentation/assets')"
    )
    parser.add_argument(
        "--max-size",
        type=int,
        default=50 * 1024 * 1024,  # 50MB
        help="Maximum file size in bytes (default: 50MB)"
    )

    args = parser.parse_args()

    if not args.repo_path.exists():
        print(f"Error: Repository path {args.repo_path} does not exist", file=sys.stderr)
        sys.exit(1)

    # TODO: Implement conversion logic
    print(f"Scanning {args.repo_path} for assets...")
    print(f"Output will be written to {args.output_dir}")
    # Ensure output directory exists for direct invocation scenarios (tests)
    try:
        args.output_dir.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        print(f"Error creating output directory {args.output_dir}: {e}", file=sys.stderr)
        sys.exit(1)

    # Allow disabling specific formats via environment variables to work around platform issues
    disable_docx = os.environ.get("DOCUMENTRON_DISABLE_DOCX") == "1"
    disable_xlsx = os.environ.get("DOCUMENTRON_DISABLE_XLSX") == "1"
    disable_vdx  = os.environ.get("DOCUMENTRON_DISABLE_VDX") == "1"
    if disable_docx:
        print("DOCX conversion disabled via DOCUMENTRON_DISABLE_DOCX=1")
    if disable_xlsx:
        print("XLSX conversion disabled via DOCUMENTRON_DISABLE_XLSX=1")
    if disable_vdx:
        print("VDX conversion disabled via DOCUMENTRON_DISABLE_VDX=1")

    from .file_discovery import discover_asset_files
    asset_files = discover_asset_files(args.repo_path)
    print(f"Found {len(asset_files)} asset files")

    converted_count = 0
    for file_path in asset_files:
        try:
            if file_path.suffix.lower() == '.docx':
                if disable_docx:
                    print(f"Skipping DOCX (disabled): {file_path}")
                    continue
                from .docx_converter import convert_docx_file
                convert_docx_file(file_path, args.output_dir, args.max_size)
            elif file_path.suffix.lower() == '.xlsx':
                if disable_xlsx:
                    print(f"Skipping XLSX (disabled): {file_path}")
                    continue
                from .xlsx_converter import convert_xlsx_file
                convert_xlsx_file(file_path, args.output_dir, args.max_size)
            elif file_path.suffix.lower() == '.vdx':
                if disable_vdx:
                    print(f"Skipping VDX (disabled): {file_path}")
                    continue
                from .vdx_converter import convert_vdx_file
                convert_vdx_file(file_path, args.output_dir, args.max_size)
            else:
                print(f"Unsupported file type: {file_path}", file=sys.stderr)
                continue
            converted_count += 1
        except Exception as e:
            print(f"Failed to convert {file_path}: {e}", file=sys.stderr)

    print(f"Successfully converted {converted_count} files")

if __name__ == "__main__":
    main()
