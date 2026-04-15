import math
from typing import Dict, Any

def compute_score(profile: Dict[str, Any], matching: Dict[str, Any]) -> Dict[str, Any]:
    # Basic scoring: percent of required skills present, weighted by experience
    matched = matching.get("matched_skills", [])
    missing = matching.get("missing_skills", [])
    total_req = max(1, len(matched) + len(missing))
    coverage = len(matched) / total_req

    # crude experience weight: +0.1 for each year if experience_summary contains a number
    exp_text = profile.get("experience_summary", "")
    years = 0
    try:
        import re

        m = re.search(r"(\d+)\+?", exp_text)
        if m:
            years = int(m.group(1))
    except Exception:
        years = 0

    exp_weight = min(0.3, 0.02 * years)  # caps at +0.3
    raw_score = coverage * (1 + exp_weight)
    score = int(max(0, min(100, math.floor(raw_score * 100))))

    breakdown = f"{len(matched)}/{total_req} required skills matched ({coverage:.0%}); experience factor {exp_weight:.2f}."
    return {"score": score, "breakdown": breakdown}
