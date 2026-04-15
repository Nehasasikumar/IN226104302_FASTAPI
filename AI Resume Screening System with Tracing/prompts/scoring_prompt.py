SCORING_PROMPT = """
You are a scoring assistant. Given the job description, the candidate profile (skills, experience_summary, tools) and matching results (matched_skills, missing_skills), return a JSON object with:
- score: integer 0-100 (higher is better)
- breakdown: short one-line explanation of how the score was computed

Rules:
- Use matched skills coverage as primary factor, experience as secondary.
- Output must be valid JSON with keys `score` and `breakdown`.
Job description:
{job}

Candidate profile:
{profile}

Matching results:
{matching}
"""
