EXPLANATION_PROMPT = """
You are an explainability assistant. Given the candidate profile (skills, experience_summary, tools), the matching results, and the assigned score, produce a short human-readable explanation (3-6 sentences) describing why the score was assigned and what are the candidate's strengths and key gaps.

Output must be plain text (not JSON).

Candidate profile:
{profile}

Matching results:
{matching}

Score:
{score}
"""
