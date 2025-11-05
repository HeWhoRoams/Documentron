"""
Smoke test for asset conversion end-to-end.

Creates minimal sample assets in a temp repo directory, runs the
conversion entry point, and asserts JSON artifacts are produced in the
configured output directory.
"""

import json
import os
from pathlib import Path
import tempfile
import importlib

from Documentron.core.asset_conversion.main import main as convert_main
import pytest


def _write_minimal_vdx(path: Path) -> None:
    # Minimal Visio 2003 XML with one page and one shape with text
    content = (
        """
<?xml version="1.0" encoding="UTF-8"?>
<VisioDocument xmlns="http://schemas.microsoft.com/visio/2003/core">
  <Pages>
    <Page Name="Page-1">
      <Shapes>
        <Shape ID="1" Type="Rectangle">
          <Text>Hello</Text>
        </Shape>
      </Shapes>
    </Page>
  </Pages>
</VisioDocument>
""".strip()
    )
    path.write_text(content, encoding="utf-8")


def test_smoke_conversion_produces_artifacts():
    # Require defusedxml for VDX conversion; skip if not available in env
    try:
        import defusedxml  # type: ignore
    except Exception:
        pytest.skip("defusedxml not installed; skipping VDX smoke test")
    with tempfile.TemporaryDirectory() as tmp:
        repo = Path(tmp) / "repo"
        repo.mkdir(parents=True, exist_ok=True)

        # Prepare output under Generated Documentation/assets
        out_dir = Path(tmp) / "Generated Documentation" / "assets"

        # Create a minimal VDX file (no external deps)
        vdx_path = repo / "diagram.vdx"
        _write_minimal_vdx(vdx_path)

        # Keep test dependency-free: rely only on VDX conversion (no external libs)

        # Run conversion
        # Simulate CLI: repo path + --output-dir
        import sys
        argv_backup = sys.argv
        try:
            sys.argv = ["asset-convert", str(repo), "--output-dir", str(out_dir)]
            convert_main()
        finally:
            sys.argv = argv_backup

        # Assert output JSON artifacts exist for at least the VDX file
        assert out_dir.exists(), "Output directory not created"
        json_files = list(out_dir.glob("*.json"))
        assert len(json_files) >= 1, "No artifacts were produced"

        # Optionally, basic schema sanity on first artifact
        with open(json_files[0], "r", encoding="utf-8") as f:
            data = json.load(f)
        assert "asset_id" in data and data["asset_id"], "Missing asset_id"
        assert data.get("original_path"), "Missing original_path"
        assert data.get("file_hash"), "Missing file_hash"
        assert data.get("content") is not None, "Missing content"
        assert data.get("provenance") is not None, "Missing provenance"
