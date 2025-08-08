from typing import Any, Dict, List, Optional

from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI, HTTPException
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest

from . import tasks

app = FastAPI(title="Task Service", version="0.1.0")

scheduler = BackgroundScheduler(timezone="UTC")
scheduler.start()

# Schedule some default recurring tasks
scheduler.add_job(tasks.heartbeat, "interval", seconds=30, id="heartbeat", replace_existing=True)
scheduler.add_job(tasks.web_check, "interval", minutes=1, id="web_check", replace_existing=True)
scheduler.add_job(tasks.cpu_burn, "interval", minutes=10, id="cpu_burn", replace_existing=True)


class RunTaskRequest(BaseModel):
    name: str
    args: Optional[List[Any]] = None
    kwargs: Optional[Dict[str, Any]] = None


@app.get("/health")
def health() -> Dict[str, str]:
    return {"status": "ok"}


@app.get("/metrics")
def metrics() -> PlainTextResponse:
    return PlainTextResponse(generate_latest(), media_type=CONTENT_TYPE_LATEST)


@app.get("/tasks")
def list_tasks() -> List[Dict[str, Any]]:
    jobs = scheduler.get_jobs()
    return [
        {
            "id": job.id,
            "next_run_time": job.next_run_time.isoformat() if job.next_run_time else None,
            "trigger": str(job.trigger),
        }
        for job in jobs
    ]


@app.post("/tasks/run")
def run_task(req: RunTaskRequest) -> Dict[str, Any]:
    mapping = {
        "heartbeat": tasks.heartbeat,
        "web_check": tasks.web_check,
        "cpu_burn": tasks.cpu_burn,
    }
    func = mapping.get(req.name)
    if not func:
        raise HTTPException(status_code=404, detail="Task not found")

    args = req.args or []
    kwargs = req.kwargs or {}

    try:
        result = func(*args, **kwargs)
        return {"result": result}
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=str(exc)) from exc