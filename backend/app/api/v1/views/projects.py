"""项目 CRUD 接口。"""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.schemas.projects import ProjectCreate, ProjectRead, ProjectUpdate
from app.services.project_service import ProjectService

router = APIRouter()


def get_project_service(session: AsyncSession = Depends(get_session)) -> ProjectService:
    """便于复用的 ProjectService 依赖。"""

    return ProjectService(session)


@router.post("", response_model=ProjectRead, status_code=status.HTTP_201_CREATED)
async def create_project(
    payload: ProjectCreate,
    service: ProjectService = Depends(get_project_service),
) -> ProjectRead:
    """创建项目并返回完整信息。"""

    project = await service.create_project(payload)
    return ProjectRead.model_validate(project)


@router.get("", response_model=list[ProjectRead])
async def list_projects(
    skip: int = Query(0, ge=0, description="起始偏移"),
    limit: int = Query(20, ge=1, le=100, description="返回条目数"),
    service: ProjectService = Depends(get_project_service),
) -> list[ProjectRead]:
    """分页列出项目。"""

    projects = await service.list_projects(skip=skip, limit=limit)
    return [ProjectRead.model_validate(item) for item in projects]


@router.get("/{project_id}", response_model=ProjectRead)
async def get_project(
    project_id: UUID,
    service: ProjectService = Depends(get_project_service),
) -> ProjectRead:
    """查询单个项目。"""

    project = await service.get_project(project_id)
    return ProjectRead.model_validate(project)


@router.patch("/{project_id}", response_model=ProjectRead)
async def update_project(
    project_id: UUID,
    payload: ProjectUpdate,
    service: ProjectService = Depends(get_project_service),
) -> ProjectRead:
    """局部更新项目。"""

    project = await service.update_project(project_id, payload)
    return ProjectRead.model_validate(project)


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(
    project_id: UUID,
    service: ProjectService = Depends(get_project_service),
) -> None:
    """删除项目。"""

    await service.delete_project(project_id)
