from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from io import BytesIO
from .ingest import ingest_pdf
from .graph import GraphWorkflow
from .hitl import HitlManager

app = FastAPI(title="RAG Support Assistant Prototype")
graph = GraphWorkflow()
hitl = graph.hitl

class QueryIn(BaseModel):
    query: str
    user_id: str = "demo"

@app.post("/ingest")
async def ingest_endpoint(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported in this demo")
    content = await file.read()
    bio = BytesIO(content)
    res = ingest_pdf(bio, doc_id=file.filename)
    return {"status": "ingested", "doc_id": res["doc_id"], "chunks": res["chunks"]}

@app.post("/query")
async def query_endpoint(q: QueryIn):
    res = graph.run(q.query, q.user_id)
    return res

class HitlIn(BaseModel):
    task_id: str
    human_response: str

@app.post("/hitl/approve")
async def hitl_approve(payload: HitlIn):
    t = hitl.approve(payload.task_id, payload.human_response)
    if not t:
        raise HTTPException(status_code=404, detail="task not found")
    return {"status": "approved", "task": t}
