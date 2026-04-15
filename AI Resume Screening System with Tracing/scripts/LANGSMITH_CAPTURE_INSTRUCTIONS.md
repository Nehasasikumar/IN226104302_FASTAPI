LangSmith capture instructions
----------------------------

Manual steps to capture useful screenshots for submission:

1. Ensure `LANGCHAIN_TRACING_V2=true` and `LANGSMITH_API_KEY` are set in your environment.
2. Run the LLM pipeline:

```powershell
python run_with_llm.py
```

3. Open https://app.langchain.com (LangSmith) and navigate to Traces → your recent run.
4. Capture these screenshots:
  - Full pipeline trace showing all nodes (extraction, matching, scoring, explanation).
  - One expanded extraction node showing prompt and LLM response.
  - Score object and explanation node.
5. Save screenshots into `docs/langsmith_screenshots/` and commit them to the repo for submission.

Optional automated approach (advanced): use Playwright or Puppeteer with a headless browser to log in and screenshot, but this requires credentials and 2FA handling — I can add this automation if you want.
