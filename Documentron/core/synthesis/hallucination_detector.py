"""
Hallucination and uncertainty flagging logic.
"""

import re
from typing import Dict, Any, List

class HallucinationDetector:
    """Detects potential hallucinations in generated content."""

    UNCERTAIN_TERMS = ['may', 'might', 'possibly', 'uncertain', 'unknown', 'phantom']

    def flag_hallucinations(self, content: str, citations: List[Dict[str, Any]]) -> str:
        """Flag potential hallucinations in content."""
        # First, flag uncited sentences
        flagged_content = self._flag_uncited_sentences(content, citations)
        
        # Then, flag uncertain terms
        for term in self.UNCERTAIN_TERMS:
            pattern = re.compile(re.escape(term), re.IGNORECASE)
            flagged_content = pattern.sub(f"**{term}** (potential hallucination)", flagged_content)
        
        return flagged_content

    def _flag_uncited_sentences(self, content: str, citations: List[Dict[str, Any]]) -> str:
        """Flag sentences without citations."""
        # Use regex to find sentence spans
        sentence_pattern = r'[^.!?]*[.!?]+'
        result = []
        last_end = 0
        for match in re.finditer(sentence_pattern, content):
            # Append intervening text
            result.append(content[last_end:match.start()])
            sentence = match.group()
            if sentence.strip() and not self._has_citation(sentence, citations):
                result.append(sentence + " **[UNCITED]**")
            else:
                result.append(sentence)
            last_end = match.end()
        # Append remaining text
        result.append(content[last_end:])
        return ''.join(result)

    def _has_citation(self, sentence: str, citations: List[Dict[str, Any]]) -> bool:
        """Check if sentence has supporting citation."""
        # Simple check - in real implementation, more sophisticated
        for citation in citations:
            file_path = citation.get('file')
            if file_path and file_path in sentence:
                return True
        return False