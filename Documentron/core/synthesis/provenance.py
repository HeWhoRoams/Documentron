"""
Provenance and confidence signal logic for doc synthesis.
"""

import hashlib
import json
from datetime import datetime
from typing import Dict, List, Any

class ProvenanceManager:
    """Manages provenance and confidence signals for generated docs."""

    def __init__(self):
        self.timestamp = datetime.now().isoformat()

    def generate_provenance(self, artifacts: Dict[str, Any]) -> Dict[str, Any]:
        """Generate provenance information for the synthesis run."""
        # Create hash of all artifacts for determinism check
        combined = json.dumps(artifacts, sort_keys=True)
        artifact_hash = hashlib.sha256(combined.encode()).hexdigest()

        return {
            'timestamp': self.timestamp,
            'artifact_hash': artifact_hash,
            'source': 'Documentron synthesis v1.0'
        }

    def add_confidence_signals(self, content: str, citations: List[Dict[str, Any]]) -> str:
        """Add confidence signals to content based on citations."""
        # Simple heuristic: more citations = higher confidence
        confidence_level = min(len(citations) * 0.1, 1.0)

        confidence_note = f"\n\n**Confidence Level**: {confidence_level:.1f}/1.0\n"
        return content + confidence_note

    def flag_uncertainty(self, content: str, uncertain_terms: List[str] = None) -> str:
        """Flag uncertain or uncited claims."""
        if uncertain_terms is None:
            uncertain_terms = ['may', 'might', 'possibly', 'uncertain', 'unknown']

        # Simple flagging - in real implementation, use LLM or analysis
        flagged_content = content
        for term in uncertain_terms:
            if term in content.lower():
                flagged_content = flagged_content.replace(term, f"**{term}** (uncertain)")

        return flagged_content