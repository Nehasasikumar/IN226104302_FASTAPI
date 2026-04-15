EXTRACTION_PROMPT = """
You are a precise extractor. Given a candidate resume text provided as input, extract the following fields in valid JSON only:
- skills: a list of skill keywords (e.g., Python, SQL, pandas)
- experience_summary: a 1-2 sentence summary of relevant experience (years, roles)
- tools: a list of tools, libraries or platforms mentioned (e.g., AWS, TensorFlow)

Rules:
- Output must be valid JSON with keys: skills, experience_summary, tools
- Do NOT assume or hallucinate skills not present in the resume
- Normalize skills/tools to short keyword form (Title case or common acronyms)
Input resume:
{resume}
"""
