MATCHING_PROMPT = """
You are a concise matcher. Given the job description and the candidate's extracted profile (skills, experience_summary, tools), produce JSON only with:
- matched_skills: list of skills that appear in both the job description and resume
- missing_skills: list of job-required skills not found in resume
- match_notes: 1-2 short sentences about fit for technical skills

Rules:
- Output valid JSON only with the keys above.
- Do NOT invent skills present in the resume.
Job description:
{job}

Candidate profile (JSON):
{profile}
"""
