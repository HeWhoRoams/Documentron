"""
Hallucination and uncertainty flagging logic.
"""

from typing import Dict, Any, List

class HallucinationDetector:
    """Detects potential hallucinations in generated content."""

    UNCERTAIN_TERMS = ['may', 'might', 'possibly', 'uncertain', 'unknown', 'phantom']

    def __init__(self):
        pass

    def flag_hallucinations(self, content: str, citations: List[Dict[str, Any]]) -> str:
        """Flag potential hallucinations in content."""
        flagged_content = content

        # Flag uncertain terms
        for term in self.UNCERTAIN_TERMS:
            if term in content.lower():
                flagged_content = flagged_content.replace(term, f"**{term}** (potential hallucination)")

        # Check for uncited claims
        # Simple heuristic: sentences without citations
        sentences = content.split('.')
        for sentence in sentences:
            if sentence.strip() and not self._has_citation(sentence, citations):
                flagged_content = flagged_content.replace(sentence, f"{sentence} **[UNCITED]**")

        return flagged_content

    def _has_citation(self, sentence: str, citations: List[Dict[str, Any]]) -> bool:
        """Check if sentence has supporting citation."""
        # Simple check - in real implementation, more sophisticated
        for citation in citations:
            if citation['file'] in sentence:
                return True
        return False