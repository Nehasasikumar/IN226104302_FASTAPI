import json
from typing import Dict, Any, List

from langchain import LLMChain
from langchain.prompts import PromptTemplate

from ..prompts.matching_prompt import MATCHING_PROMPT


def match_profile(job_description: str, profile: Dict[str, Any], llm=None) -> Dict[str, Any]:
    # If LLM provided, use it to generate a JSON match; else use deterministic matching
    if llm is None:
        jd = job_description.lower()
        matched = []
        missing = []
        for s in profile.get("skills", []):
            if s.lower() in jd:
                matched.append(s)
        # simple missing skills detection: look for common skill keywords in JD
        candidates = ["python", "sql", "pandas", "numpy", "machine learning", "tensorflow", "aws"]
        for c in candidates:
            if c in jd and c.capitalize() not in profile.get("skills", []):
                missing.append(c.capitalize())

        notes = "Technical skills fit is adequate." if len(matched) > 0 else "Limited technical match found."
        return {"matched_skills": matched, "missing_skills": missing, "match_notes": notes}

    prompt = PromptTemplate(input_variables=["job", "profile"], template=MATCHING_PROMPT)
    chain = LLMChain(llm=llm, prompt=prompt)
    try:
        out = chain.invoke({"job": job_description, "profile": json.dumps(profile)})
    except Exception:
        out = chain.run(job_description, json.dumps(profile))

    try:
        parsed = json.loads(out)
    except Exception:
        # fallback: simple deterministic behavior
        return match_profile(job_description, profile, llm=None)

    return {
        "matched_skills": parsed.get("matched_skills", []),
        "missing_skills": parsed.get("missing_skills", []),
        "match_notes": parsed.get("match_notes", ""),
    }
