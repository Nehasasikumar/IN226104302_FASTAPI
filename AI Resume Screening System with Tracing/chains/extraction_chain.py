import json
import re
from typing import Dict, Any

from langchain import LLMChain
from langchain.prompts import PromptTemplate

from ..prompts.extraction_prompt import EXTRACTION_PROMPT


def _fallback_extract(resume: str) -> Dict[str, Any]:
    # Simple rule-based extractor for offline use
    common_skills = [
        "Python",
        "SQL",  
        "pandas",
        "numpy",
        "scikit-learn",
        "TensorFlow",
        "PyTorch",
        "Docker",
        "AWS",
        "Excel",
    ]
    skills = []
    tools = []
    for s in common_skills:
        if re.search(r"\b" + re.escape(s) + r"\b", resume, re.IGNORECASE):
            if s.lower() in ["aws", "docker", "tensorflow", "pytorch"]:
                tools.append(s)
            else:
                skills.append(s)

    # experience summary: try to pick years of experience
    m = re.search(r"(\d+)\+?\s+years? of", resume, re.IGNORECASE)
    years = f"{m.group(1)} years experience" if m else "Experience not clearly stated"
    return {"skills": skills, "experience_summary": years, "tools": tools}


def extract_profile(llm=None, resume: str = "") -> Dict[str, Any]:
    """Try using an LLM chain to extract structured profile; fall back to rule-based extractor if unavailable."""
    if llm is None:
        return _fallback_extract(resume)

    prompt = PromptTemplate(input_variables=["resume"], template=EXTRACTION_PROMPT)
    chain = LLMChain(llm=llm, prompt=prompt)
    # prefer .invoke() if available, else .run()
    try:
        out = chain.invoke({"resume": resume})
    except Exception:
        try:
            out = chain.run(resume)
        except Exception:
            return _fallback_extract(resume)

    # parse JSON from the LLM output robustly
    try:
        parsed = json.loads(out)
    except Exception:
        # try to extract JSON substring
        m = re.search(r"\{.*\}", out, re.DOTALL)
        if m:
            try:
                parsed = json.loads(m.group(0))
            except Exception:
                return _fallback_extract(resume)
        else:
            return _fallback_extract(resume)

    # Ensure keys exist
    return {
        "skills": parsed.get("skills", []),
        "experience_summary": parsed.get("experience_summary", ""),
        "tools": parsed.get("tools", []),
    }
