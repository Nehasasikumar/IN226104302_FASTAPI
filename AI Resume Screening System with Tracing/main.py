"""
AI Resume Screening System (minimal runnable pipeline)

Run instructions (local):
- create a virtualenv and `pip install -r requirements.txt`
- set `OPENAI_API_KEY` (optional) and `LANGSMITH_API_KEY` (optional)
- set `LANGCHAIN_TRACING_V2=true` to enable tracing to LangSmith
- run `python main.py`

The pipeline will fall back to a deterministic extractor/matcher/scorer if LLM keys are not provided.
"""

import os
import json
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.tracers import LangSmithTracer

from chains.extraction_chain import extract_profile
from chains.matching_chain import match_profile
from chains.scoring_chain import compute_score
from chains.explanation_chain import explain_profile


def get_llm():
    api_key = os.environ.get("OPENAI_API_KEY")
    # configure LangSmith tracer if configured
    tracer = None
    try:
        tracer = LangSmithTracer()
    except Exception:
        tracer = None

    if api_key:
        try:
            from langchain.llms import OpenAI
        except Exception:
            try:
                from langchain import OpenAI
            except Exception:
                return None

        if tracer:
            manager = CallbackManager([tracer])
            return OpenAI(temperature=0, openai_api_key=api_key, callback_manager=manager, verbose=False)
        else:
            return OpenAI(temperature=0, openai_api_key=api_key, verbose=False)
    return None


def load_text(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def run_pipeline(job_text: str, resume_text: str, llm=None):
    profile = extract_profile(llm=llm, resume=resume_text)
    matching = match_profile(job_text, profile, llm=llm)
    score_obj = compute_score(profile, matching)
    explanation = explain_profile(profile, matching, score_obj["score"], llm=llm)

    result = {
        "profile": profile,
        "matching": matching,
        "score": score_obj,
        "explanation": explanation,
    }
    return result


def main():
    print("Starting AI Resume Screening pipeline...")
    base = os.path.dirname(__file__)
    data_dir = os.path.join(base, "data")
    job = load_text(os.path.join(data_dir, "job_description.txt"))

    # three resumes: strong, average, weak
    resumes = [
        ("strong", load_text(os.path.join(data_dir, "resume_strong.txt"))),
        ("average", load_text(os.path.join(data_dir, "resume_average.txt"))),
        ("weak", load_text(os.path.join(data_dir, "resume_weak.txt"))),
    ]

    llm = get_llm()
    results = {}
    for name, text in resumes:
        print(f"\n--- Running pipeline for: {name} candidate ---")
        res = run_pipeline(job, text, llm=llm)
        print(json.dumps({"score": res["score"]["score"], "breakdown": res["score"]["breakdown"]}, indent=2))
        print("Explanation:\n", res["explanation"], "\n")
        results[name] = res

    # Deliberate incorrect output: show a debug case where resume missing a required skill
    print("Running deliberate incorrect output for debugging: removing all skills from average candidate and re-scoring")
    avg_profile = extract_profile(llm=llm, resume=resumes[1][1])
    avg_profile["skills"] = []  # introduce incorrect/missing extraction
    matching2 = match_profile(job, avg_profile, llm=llm)
    score2 = compute_score(avg_profile, matching2)
    explanation2 = explain_profile(avg_profile, matching2, score2["score"], llm=llm)
    print("Deliberate incorrect run result:")
    print(json.dumps({"score": score2["score"], "breakdown": score2["breakdown"]}, indent=2))
    print("Explanation:\n", explanation2)


if __name__ == "__main__":
    main()
