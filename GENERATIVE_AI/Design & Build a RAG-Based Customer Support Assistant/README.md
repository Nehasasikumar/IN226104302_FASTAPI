# RAG-Based Customer Support Assistant — Prototype

Quick start (Windows PowerShell):

1) Create a Python venv and install deps

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2) Run the API

```powershell
uvicorn src.app:app --reload --port 8000
```

3) Ingest a PDF (curl / Postman)

```powershell
curl -X POST "http://localhost:8000/ingest" -F "file=@path\to\manual.pdf"
```

4) Query

```powershell
curl -X POST "http://localhost:8000/query" -H "Content-Type: application/json" -d '{"query":"How do I reset my device?","user_id":"demo"}'
```

HITL demo:
- If a query triggers escalation, the API returns a `hitl_task_id`. Use `/hitl/approve` to supply a human response.

Recording a demo video:
- Start the server, ingest a sample PDF, run sample queries (auto and escalate), then demonstrate approving a HITL task.
- Use OBS Studio or built-in screen recorder. Show terminal and a browser call with `curl` or Postman.
