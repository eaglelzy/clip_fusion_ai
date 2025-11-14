"""v1 API 路由汇总。"""
from fastapi import APIRouter

from app.api.v1.views import projects, scripts, shots

router = APIRouter()

router.include_router(projects.router, prefix="/projects", tags=["projects"])
router.include_router(scripts.router, prefix="/projects/{project_id}/scripts", tags=["scripts"])
router.include_router(shots.router, prefix="/projects/{project_id}/shots", tags=["shots"])
