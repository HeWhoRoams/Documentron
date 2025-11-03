import pytest
from pathlib import Path
import sys
import os

# Add synthesis module to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'core' / 'synthesis'))

from artifact_loader import ArtifactLoader
from provenance import ProvenanceManager
from hallucination_detector import HallucinationDetector
from api_coverage import APICoverageReporter

def test_artifact_loader_loads_required_artifacts():
    """Test that artifact loader loads required artifacts."""
    loader = ArtifactLoader(Path('dummy'))
    # Mock artifacts
    artifacts = {
        'build.info.json': {'name': 'test'},
        'symbol.graph.json': {'nodes': []},
        'api.surface.json': {'apis': []},
        'deps.map.json': {'dependencies': {}},
        'quality.report.json': {'metrics': {}}
    }
    assert loader.validate_artifacts(artifacts)

def test_provenance_manager_generates_hash():
    """Test that provenance manager generates consistent hashes."""
    manager = ProvenanceManager()
    artifacts = {'test': 'data'}
    prov1 = manager.generate_provenance(artifacts)
    prov2 = manager.generate_provenance(artifacts)
    assert prov1['artifact_hash'] == prov2['artifact_hash']

def test_hallucination_detector_flags_uncertain_terms():
    """Test that hallucination detector flags uncertain terms."""
    detector = HallucinationDetector()
    content = "This may be correct."
    citations = []
    flagged = detector.flag_hallucinations(content, citations)
    assert "potential hallucination" in flagged

def test_api_coverage_measures_correctly():
    """Test that API coverage reporter measures coverage."""
    reporter = APICoverageReporter()
    api_surface = {'apis': [{'name': 'API1'}, {'name': 'API2'}]}
    api_ref = "# API Reference\n\n## API1\n\nDescription."
    coverage = reporter.measure_coverage(api_surface, api_ref)
    assert coverage['total_apis'] == 2
    assert coverage['documented'] == 1
    assert coverage['coverage_percentage'] == 50.0

def test_synthesis_placeholder():
    """Placeholder test for synthesis module"""
    assert True