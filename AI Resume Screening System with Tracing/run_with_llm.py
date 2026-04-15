"""Run pipeline using an LLM (OpenAI) and LangSmith tracer if API keys are set.
Saves output to `results_llm.json`.
"""
import os
import json
from pathlib import Path

from main import get_llm, run_pipeline


def run_with_llm():
    base = Path(__file__).parent
    data = base / "data"
    job = (data / "job_description.txt").read_text(encoding="utf-8")

    resumes = [
        ("strong", (data / "resume_strong.txt").read_text(encoding="utf-8")),
        ("average", (data / "resume_average.txt").read_text(encoding="utf-8")),
        ("weak", (data / "resume_weak.txt").read_text(encoding="utf-8")),
    ]

    llm = get_llm()
    if llm is None:
        print("No LLM available. Ensure OPENAI_API_KEY is set and langchain OpenAI LLM is available.")
        return

    results = {}
    for name, text in resumes:
        print(f"Running with LLM for: {name}")
        res = run_pipeline(job, text, llm=llm)
        results[name] = res

    out_file = base / "results_llm.json"
    out_file.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"Wrote LLM-run results to {out_file}")


if __name__ == "__main__":
    run_with_llm()
