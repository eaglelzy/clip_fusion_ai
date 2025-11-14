"""Celery 任务占位，后续可注册具体任务。"""
from celery import Celery

from app.core.config import get_settings

settings = get_settings()
celery_app = Celery(
    "indextts",
    broker=settings.broker_url,
    backend=settings.result_backend,
)


@celery_app.task(name="synthesis.run")
def run_synthesis(task_payload: dict) -> dict:
    """执行合成任务的示例 Celery 任务。"""
    return {"status": "completed", "payload": task_payload}
