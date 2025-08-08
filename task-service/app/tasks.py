import time
import random
from typing import Any, Dict

import httpx

from .metrics import tasks_executed_total, task_duration_seconds, tasks_running


def _run_wrapped(task_name: str, func, *args, **kwargs) -> Dict[str, Any]:
    start_time_seconds = time.time()
    tasks_running.inc()
    status = "success"
    try:
        result = func(*args, **kwargs)
        return result
    except Exception as exc:  # noqa: BLE001
        status = "error"
        raise exc
    finally:
        duration_seconds = time.time() - start_time_seconds
        task_duration_seconds.labels(task_name=task_name).observe(duration_seconds)
        tasks_executed_total.labels(task_name=task_name, status=status).inc()
        tasks_running.dec()


def heartbeat() -> Dict[str, Any]:
    def inner():
        time.sleep(0.1)
        return {"ok": True, "ts": time.time()}

    return _run_wrapped("heartbeat", inner)


def web_check(url: str = "https://example.com") -> Dict[str, Any]:
    def inner():
        with httpx.Client(timeout=10) as client:
            response = client.get(url)
            response.raise_for_status()
            return {"status_code": response.status_code, "url": url}

    return _run_wrapped("web_check", inner)


def cpu_burn(seconds: int = 2) -> Dict[str, Any]:
    def inner():
        end_time = time.time() + seconds
        x = 0.0001
        while time.time() < end_time:
            x = x * x + random.random()  # noqa: PLW2901
        return {"done": True, "seconds": seconds}

    return _run_wrapped("cpu_burn", inner)