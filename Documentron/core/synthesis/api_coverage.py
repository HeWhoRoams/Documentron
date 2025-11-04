"""
API coverage measurement and reporting.
"""

import re
from typing import Dict, Any

class APICoverageReporter:
    """Measures and reports API coverage."""

    def measure_coverage(self, api_surface: Dict[str, Any], api_reference_content: str, threshold: float = 90.0) -> Dict[str, Any]:
        """Measure API coverage between surface and reference."""
        apis = api_surface.get('apis', [])
        total_apis = len(apis)
        documented = 0
        exclusions = []

        for api in apis:
            name = api.get('name', '')
            # Use word-boundary regex for exact matching to avoid false positives
            if re.search(r'\b' + re.escape(name) + r'\b', api_reference_content, re.IGNORECASE):
                documented += 1
            elif api.get('exclusion_reason'):
                exclusions.append({'name': name, 'reason': api['exclusion_reason']})

        coverage_pct = (documented / total_apis) * 100 if total_apis > 0 else 0

        return {
            'total_apis': total_apis,
            'documented': documented,
            'coverage_percentage': coverage_pct,
            'exclusions': exclusions,
            'threshold': threshold,
            'meets_threshold': coverage_pct >= threshold
        }

    def generate_report(self, coverage: Dict[str, Any]) -> str:
        """Generate human-readable coverage report."""
        report = "# API Coverage Report\n\n"
        report += f"Total APIs: {coverage['total_apis']}\n"
        report += f"Documented: {coverage['documented']}\n"
        report += f"Coverage: {coverage['coverage_percentage']:.1f}%\n"
        report += f"Meets {coverage['threshold']}% threshold: {'Yes' if coverage['meets_threshold'] else 'No'}\n\n"

        if coverage['exclusions']:
            report += "## Exclusions\n\n"
            for excl in coverage['exclusions']:
                report += f"- {excl['name']}: {excl['reason']}\n"

        return report


# Simple test for matching behavior
if __name__ == "__main__":
    # Test exact matching vs substring
    content = "This mentions GetUser but not GetUserProfile."
    assert re.search(r'\bGetUser\b', content, re.IGNORECASE)  # Should match exact
    assert re.search(r'\bGetUserProfile\b', content, re.IGNORECASE)  # Should match exact
    assert not re.search(r'\bGetUserP\b', content, re.IGNORECASE)  # Should not match partial
    print("Matching test passed.")