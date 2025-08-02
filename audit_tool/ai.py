"""Optional offline AI helpers.

This module is intentionally lightweight.  If an offline model such as
`llama.cpp` is available, the functions below can call into it to provide
classification suggestions or remediation advice.
"""
from typing import Optional


def suggest_classification(description: str) -> Optional[str]:
    """Return a naive classification suggestion based on keywords."""
    description = description.lower()
    if 'sql' in description:
        return 'Injection'
    if 'xss' in description:
        return 'Cross Site Scripting'
    return None
