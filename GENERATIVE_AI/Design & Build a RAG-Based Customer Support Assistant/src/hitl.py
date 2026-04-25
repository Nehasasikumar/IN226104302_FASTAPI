import uuid
from typing import Dict

class HitlManager:
    def __init__(self):
        self.tasks: Dict[str, dict] = {}

    def create_task(self, query, draft, context):
        tid = str(uuid.uuid4())
        self.tasks[tid] = {"query": query, "draft": draft, "context": context, "status": "pending", "response": None}
        return tid

    def approve(self, task_id: str, human_response: str):
        t = self.tasks.get(task_id)
        if not t:
            return None
        t["status"] = "approved"
        t["response"] = human_response
        return t

    def get_task(self, task_id: str):
        return self.tasks.get(task_id)
