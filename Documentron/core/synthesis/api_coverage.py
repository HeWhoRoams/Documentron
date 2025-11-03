"""
API coverage measurement and reporting.
"""

from typing import Dict, Any, List

class APICoverageReporter:
    """Measures and reports API coverage."""

    def __init__(self):
        pass

    def measure_coverage(self, api_surface: Dict[str, Any], api_reference_content: str) -> Dict[str, Any]:
        """Measure API coverage between surface and reference."""
        apis = api_surface.get('apis', [])
        total_apis = len(apis)
        documented = 0
        exclusions = []

        for api in apis:
            name = api.get('name', '')
            if name in api_reference_content:
                documented += 1
            elif api.get('exclusion_reason'):
                exclusions.append({'name': name, 'reason': api['exclusion_reason']})

        coverage_pct = (documented / total_apis) * 100 if total_apis > 0 else 0

        return {
            'total_apis': total_apis,
            'documented': documented,
            'coverage_percentage': coverage_pct,
            'exclusions': exclusions,
            'meets_threshold': coverage_pct >= 90
        }

    def generate_report(self, coverage: Dict[str, Any]) -> str:
        """Generate human-readable coverage report."""
        report = "# API Coverage Report\n\n"
        report += f"Total APIs: {coverage['total_apis']}\n"
        report += f"Documented: {coverage['documented']}\n"
        report += f"Coverage: {coverage['coverage_percentage']:.1f}%\n"
        report += f"Meets 90% threshold: {'Yes' if coverage['meets_threshold'] else 'No'}\n\n"

        if coverage['exclusions']:
            report += "## Exclusions\n\n"
            for excl in coverage['exclusions']:
                report += f"- {excl['name']}: {excl['reason']}\n"

        return report