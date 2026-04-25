from .retriever import retrieve
from .hitl import HitlManager
import os
import json

HITL_THRESHOLD = 0.5

class GraphWorkflow:
    def __init__(self):
        self.hitl = HitlManager()

    def _process_with_llm(self, query, contexts):
        # Simple LLM fallback: concatenate context and return a draft plus heuristic confidence.
        prompt = "\n\n".join([c["text"] for c in contexts])
        draft = f"Answer (draft) to: {query}\n\nContext:\n{prompt[:1500]}"
        # heuristic confidence based on number of contexts
        confidence = min(0.95, 0.4 + 0.15 * len(contexts))
        return {"answer": draft, "confidence": confidence}

    def run(self, query: str, user_id: str = "user"):
        # InputNode -> RetrieveNode
        retrieved = retrieve(query, top_k=5)

        # ProcessNode
        llm_out = self._process_with_llm(query, retrieved)

        # DecideNode
        if llm_out["confidence"] >= HITL_THRESHOLD:
            return {"action": "auto", "answer": llm_out["answer"], "confidence": llm_out["confidence"], "sources": retrieved}
        else:
            task_id = self.hitl.create_task(query, llm_out["answer"], retrieved)
            return {"action": "hitl_required", "hitl_task_id": task_id, "reason": "low_confidence", "confidence": llm_out["confidence"], "sources": retrieved}
