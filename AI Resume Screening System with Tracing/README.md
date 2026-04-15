AI Resume Screening System with Tracing

Overview
- Minimal LangChain-based resume screening pipeline with tracing support (LangSmith).

Quick start
1. Create virtual environment and install:

```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

2. (Optional) Set API keys for better results and tracing:

```bash
set OPENAI_API_KEY=your_openai_key
set LANGSMITH_API_KEY=your_langsmith_key
set LANGCHAIN_TRACING_V2=true
```

3. Run locally without LLM (deterministic fallbacks):

```bash
python run_local.py
```

4. Run with LLM + LangSmith tracing (optional):

```powershell
setx OPENAI_API_KEY "your_openai_key"
setx LANGSMITH_API_KEY "your_langsmith_key"
setx LANGCHAIN_TRACING_V2 "true"
# open a new shell after setx then:
python main.py
```

What this repo includes
- `prompts/` - Prompt templates for each chain
- `chains/` - Extraction, matching, scoring, explanation logic
- `data/` - sample job description + 3 resumes (strong, average, weak)
- `main.py` - runner that executes the pipeline and a deliberate incorrect run for debugging

Notes
- If `OPENAI_API_KEY` is not set the pipeline falls back to deterministic extract/match/score logic so it remains runnable offline.
- To see traces in LangSmith set `LANGCHAIN_TRACING_V2=true` and provide a `LANGSMITH_API_KEY`.
