"""Run pipeline programmatically without shell quoting issues.
This script loads the job and candidate files and runs the pipeline with no LLM (deterministic fallbacks).
It writes `results.json` in the project folder.
"""
import json
from pathlib import Path

from chains.extraction_chain import extract_profile
from chains.matching_chain import match_profile
from chains.scoring_chain import compute_score
from chains.explanation_chain import explain_profile


def load_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def run_all():
    base = Path(__file__).parent
    data = base / "data"
    job = load_text(data / "job_description.txt")

    resumes = [
        ("strong", load_text(data / "resume_strong.txt")),
        ("average", load_text(data / "resume_average.txt")),
        ("weak", load_text(data / "resume_weak.txt")),
    ]

    results = {}
    for name, text in resumes:
        profile = extract_profile(llm=None, resume=text)
        matching = match_profile(job, profile, llm=None)
        score = compute_score(profile, matching)
        explanation = explain_profile(profile, matching, score["score"], llm=None)
        results[name] = {"profile": profile, "matching": matching, "score": score, "explanation": explanation}

    # deliberate incorrect run
    avg_profile = results["average"]["profile"].copy()
    avg_profile["skills"] = []
    matching2 = match_profile(job, avg_profile, llm=None)
    score2 = compute_score(avg_profile, matching2)
    explanation2 = explain_profile(avg_profile, matching2, score2["score"], llm=None)
    results["average_deliberate_incorrect"] = {"profile": avg_profile, "matching": matching2, "score": score2, "explanation": explanation2}

    out_file = base / "results.json"
    out_file.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"Wrote results to {out_file}")


if __name__ == "__main__":
    run_all()
