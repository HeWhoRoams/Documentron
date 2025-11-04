import pytest
from pathlib import Path
import sys
import os

from Documentron.core.synthesis.artifact_loader import ArtifactLoader
from Documentron.core.synthesis.provenance import ProvenanceManager
from Documentron.core.synthesis.hallucination_detector import HallucinationDetector
from Documentron.core.synthesis.api_coverage import APICoverageReporter

import pytest
from pathlib import Path
import sys
import os
import json
from unittest.mock import patch

from Documentron.core.synthesis.artifact_loader import ArtifactLoader
from Documentron.core.synthesis.provenance import ProvenanceManager
from Documentron.core.synthesis.hallucination_detector import HallucinationDetector
from Documentron.core.synthesis.api_coverage import APICoverageReporter

def test_artifact_loader_loads_required_artifacts(tmp_path):
    """Test that artifact loader loads required artifacts."""
    # Create required artifact files
    (tmp_path / 'build.info.json').write_text(json.dumps({'name': 'test_project', 'version': '1.0'}))
    (tmp_path / 'symbol.graph.json').write_text(json.dumps({'nodes': [{'id': '1', 'name': 'TestClass'}]}))
    (tmp_path / 'api.surface.json').write_text(json.dumps({'apis': [{'name': 'TestAPI', 'type': 'method'}]}))
    (tmp_path / 'deps.map.json').write_text(json.dumps({'dependencies': {'lib1': '1.0'}}))
    (tmp_path / 'quality.report.json').write_text(json.dumps({
        'placeholder': True,
        'metrics': {'symbol_resolution_rate': 0.95, 'project_discovery_rate': 1.0, 'ms_per_kloc': 25},
        'note': 'Metrics are placeholders until real computation is implemented'
    }))
    
    loader = ArtifactLoader(tmp_path)
    artifacts = loader.load_artifacts()
    
    # Assert load succeeded and contains expected keys
    assert 'build.info.json' in artifacts
    assert 'symbol.graph.json' in artifacts
    assert 'api.surface.json' in artifacts
    assert 'deps.map.json' in artifacts
    assert 'quality.report.json' in artifacts
    
    # Assert specific content
    assert artifacts['build.info.json']['name'] == 'test_project'
    assert len(artifacts['symbol.graph.json']['nodes']) == 1
    assert artifacts['symbol.graph.json']['nodes'][0]['name'] == 'TestClass'
    assert len(artifacts['api.surface.json']['apis']) == 1
    assert artifacts['api.surface.json']['apis'][0]['name'] == 'TestAPI'
    assert artifacts['deps.map.json']['dependencies']['lib1'] == '1.0'
    assert artifacts['quality.report.json']['placeholder'] == True
    assert artifacts['quality.report.json']['metrics']['symbol_resolution_rate'] == 0.95
    assert artifacts['quality.report.json']['metrics']['project_discovery_rate'] == 1.0
    assert artifacts['quality.report.json']['metrics']['ms_per_kloc'] == 25
    
    # Assert validation passes
    assert loader.validate_artifacts(artifacts)

def test_artifact_loader_missing_required_artifact(tmp_path):
    """Test that missing required artifact raises FileNotFoundError."""
    # Create only some files, missing build.info.json
    (tmp_path / 'symbol.graph.json').write_text(json.dumps({'nodes': []}))
    (tmp_path / 'api.surface.json').write_text(json.dumps({'apis': []}))
    (tmp_path / 'deps.map.json').write_text(json.dumps({'dependencies': {}}))
    (tmp_path / 'quality.report.json').write_text(json.dumps({'metrics': {}}))
    
    loader = ArtifactLoader(tmp_path)
    with pytest.raises(FileNotFoundError, match="Required artifact missing"):
        loader.load_artifacts()

def test_artifact_loader_malformed_json(tmp_path):
    """Test that malformed JSON raises ValueError."""
    # Create files with invalid JSON
    (tmp_path / 'build.info.json').write_text('{"name": "test"')  # Missing closing brace
    (tmp_path / 'symbol.graph.json').write_text(json.dumps({'nodes': []}))
    (tmp_path / 'api.surface.json').write_text(json.dumps({'apis': []}))
    (tmp_path / 'deps.map.json').write_text(json.dumps({'dependencies': {}}))
    (tmp_path / 'quality.report.json').write_text(json.dumps({'metrics': {}}))
    
    loader = ArtifactLoader(tmp_path)
    with pytest.raises(ValueError, match="Failed to parse JSON in"):
        loader.load_artifacts()

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
    assert coverage['threshold'] == 90.0  # Default threshold
    assert not coverage['meets_threshold']  # 50 < 90

def test_api_coverage_configurable_threshold():
    """Test that API coverage threshold is configurable."""
    reporter = APICoverageReporter()
    api_surface = {'apis': [{'name': 'API1'}, {'name': 'API2'}]}
    api_ref = "# API Reference\n\n## API1\n\nDescription."
    
    # Test with lower threshold (50% should meet 40%)
    coverage_low = reporter.measure_coverage(api_surface, api_ref, threshold=40.0)
    assert coverage_low['threshold'] == 40.0
    assert coverage_low['meets_threshold']  # 50 >= 40
    
    # Test with higher threshold (50% should not meet 60%)
    coverage_high = reporter.measure_coverage(api_surface, api_ref, threshold=60.0)
    assert coverage_high['threshold'] == 60.0
    assert not coverage_high['meets_threshold']  # 50 < 60

def test_provenance_manager_generate_provenance():
    """Test provenance generation."""
    manager = ProvenanceManager()
    artifacts = {'test': 'data'}
    provenance = manager.generate_provenance(artifacts)
    assert 'timestamp' in provenance
    assert 'artifact_hash' in provenance
    assert 'source' in provenance
    assert provenance['source'] == 'Documentron synthesis v1.0'

def test_hallucination_detector_flag_hallucinations():
    """Test hallucination detection."""
    detector = HallucinationDetector()
    content = "This is certain. This may be uncertain."
    citations = [{'file': 'test.md'}]
    flagged = detector.flag_hallucinations(content, citations)
    # Assert exact format
    assert isinstance(flagged, str)
    assert "This is certain." in flagged
    assert "**may** (potential hallucination)" in flagged
    assert "**uncertain** (potential hallucination)" in flagged  # "uncertain" is also in UNCERTAIN_TERMS
    # Assert uncited sentences are marked
    assert flagged.count("**[UNCITED]**") == 2

def test_hallucination_detector_no_uncertain_terms():
    """Test that content without uncertain terms is not flagged."""
    detector = HallucinationDetector()
    content = "This is certain. This is definite."
    citations = [{'file': 'test.md'}]
    flagged = detector.flag_hallucinations(content, citations)
    # Should only mark uncited sentences, no uncertain term flags
    assert "**certain**" not in flagged
    assert "**definite**" not in flagged
    assert flagged.count("**[UNCITED]**") == 2

def test_hallucination_detector_other_uncertain_phrases():
    """Test detection of other uncertain phrases."""
    detector = HallucinationDetector()
    content = "This might be true. This could be false. This possibly works."
    citations = []
    flagged = detector.flag_hallucinations(content, citations)
    assert "**might** (potential hallucination)" in flagged
    assert "**possibly** (potential hallucination)" in flagged
    # "could" is not in UNCERTAIN_TERMS, so not flagged
    assert "**could**" not in flagged
    # All sentences uncited
    assert flagged.count("**[UNCITED]**") == 3

def test_hallucination_detector_with_citations():
    """Test that cited sentences are not marked as uncited."""
    detector = HallucinationDetector()
    content = "This may be uncertain. This is certain from reference file."
    citations = [{'file': 'reference'}]
    flagged = detector.flag_hallucinations(content, citations)
    # First sentence has uncertain terms and is uncited
    assert "**may** (potential hallucination)" in flagged
    assert "**uncertain** (potential hallucination)" in flagged
    # Second sentence contains 'reference', so not marked uncited
    assert "This is certain from reference file." in flagged
    assert flagged.count("**[UNCITED]**") == 1  # Only the first sentence

def test_provenance_add_confidence_signals():
    """Test adding confidence signals."""
    manager = ProvenanceManager()
    content = "Some content"
    citations = [{'file': 'ref1'}, {'file': 'ref2'}]
    result = manager.add_confidence_signals(content, citations)
    assert "Confidence Level" in result
    assert "0.2/1.0" in result  # 2 citations * 0.1 = 0.2