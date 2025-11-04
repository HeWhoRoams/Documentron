"""
Artifact loader and validator for Documentron.
"""

import json
from pathlib import Path
from typing import Dict, Any

class ArtifactLoader:
    """Loads and validates artifacts from filesystem."""

    REQUIRED_ARTIFACTS = [
        'build.info.json',
        'symbol.graph.json',
        'api.surface.json',
        'deps.map.json',
        'quality.report.json'
    ]

    OPTIONAL_ARTIFACTS = [
        'assets/*.json'
    ]

    def __init__(self, artifacts_dir: Path):
        self.artifacts_dir = Path(artifacts_dir)

    def load_artifacts(self) -> Dict[str, Any]:
        """Load all artifacts into a dictionary."""
        artifacts = {}
        for artifact_file in self.REQUIRED_ARTIFACTS:
            path = self.artifacts_dir / artifact_file
            if not path.exists():
                raise FileNotFoundError(f"Required artifact missing: {path}")
            with open(path, 'r') as f:
                try:
                    artifacts[artifact_file] = json.load(f)
                except json.JSONDecodeError as e:
                    raise ValueError(f"Failed to parse JSON in {path}: {e}") from e

        # Load optional assets
        for pattern in self.OPTIONAL_ARTIFACTS:
            for path in self.artifacts_dir.glob(pattern):
                with open(path, 'r') as f:
                    try:
                        key = str(path.relative_to(self.artifacts_dir))
                        artifacts[key] = json.load(f)
                    except json.JSONDecodeError as e:
                        raise ValueError(f"Failed to parse JSON in {path}: {e}") from e

        return artifacts

    def validate_artifacts(self, artifacts: Dict[str, Any]) -> bool:
        """Basic validation of loaded artifacts."""
        # TODO: Implement schema validation
        for name, data in artifacts.items():
            if not isinstance(data, dict):
                raise ValueError(f"Artifact {name} is not a valid JSON object")
            # Check for adversarial content
            if self._is_adversarial(data):
                raise ValueError(f"Artifact {name} contains potentially adversarial content")
        return True

    def _is_adversarial(self, data: Dict[str, Any]) -> bool:
        """Check for potentially adversarial content in artifacts."""
        # Recursive traversal to check for 'phantom_api' in keys and string values
        def _contains_phantom(obj):
            if isinstance(obj, dict):
                for key, value in obj.items():
                    if isinstance(key, str) and 'phantom_api' in key.lower():
                        return True
                    if _contains_phantom(value):
                        return True
            elif isinstance(obj, list):
                for item in obj:
                    if _contains_phantom(item):
                        return True
            elif isinstance(obj, str):
                if 'phantom_api' in obj.lower():
                    return True
            return False
        
        return _contains_phantom(data)