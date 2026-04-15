from langchain import LLMChain
from langchain.prompts import PromptTemplate
import json

from ..prompts.explanation_prompt import EXPLANATION_PROMPT


def explain_profile(profile: dict, matching: dict, score: int, llm=None) -> str:
    # If LLM available, ask it to provide a human-friendly explanation.
    if llm is None:
        strengths = ", ".join(matching.get("matched_skills", [])[:5]) or "No clear strengths"
        gaps = ", ".join(matching.get("missing_skills", [])[:5]) or "No clear gaps"
        return (
            f"Score: {score}. Strengths: {strengths}. Key gaps: {gaps}. "
            "Consider screening for demonstrated project experience on missing skills."
        )

    prompt = PromptTemplate(
        input_variables=["profile", "matching", "score"], template=EXPLANATION_PROMPT
    )
    chain = LLMChain(llm=llm, prompt=prompt)
    try:
        out = chain.invoke({"profile": json.dumps(profile), "matching": json.dumps(matching), "score": str(score)})
    except Exception:
        out = chain.run(json.dumps(profile), json.dumps(matching), str(score))
    return out
