Contributing
------------

Thanks for contributing. Quick guide to run and test locally:

- Create and activate virtualenv, install deps:

```powershell
python -m venv .venv
.venv\Scripts\Activate
pip install -r requirements.txt
```

- Run deterministic pipeline (no LLM required):

```powershell
python run_local.py
```

- Run with LLM + LangSmith tracing (requires keys & `gh` login if pushing):

```powershell
setx OPENAI_API_KEY "your_openai_key"
setx LANGSMITH_API_KEY "your_langsmith_key"
setx LANGCHAIN_TRACING_V2 "true"
# restart shell, then:
python run_with_llm.py
```

- Tests:
```powershell
pip install pytest
pytest
```

If you want me to push the repo to GitHub, provide `gh` CLI auth or a GitHub token and I'll prepare the push script for you to run locally.
