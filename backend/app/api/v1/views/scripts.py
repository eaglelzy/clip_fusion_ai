"""脚本 CRUD 接口。"""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.schemas.scripts import ScriptCreate, ScriptRead, ScriptUpdate
from app.services.script_service import ScriptService

router = APIRouter()


def get_script_service(session: AsyncSession = Depends(get_session)) -> ScriptService:
    return ScriptService(session)


@router.post("", response_model=ScriptRead, status_code=status.HTTP_201_CREATED)
async def create_script(
    project_id: UUID,
    payload: ScriptCreate,
    service: ScriptService = Depends(get_script_service),
) -> ScriptRead:
    script = await service.create_script(project_id, payload)
    return ScriptRead.model_validate(script)


@router.get("", response_model=list[ScriptRead])
async def list_scripts(
    project_id: UUID,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    service: ScriptService = Depends(get_script_service),
) -> list[ScriptRead]:
    scripts = await service.list_scripts(project_id, skip=skip, limit=limit)
    return [ScriptRead.model_validate(item) for item in scripts]


@router.get("/{script_id}", response_model=ScriptRead)
async def get_script(
    project_id: UUID,
    script_id: UUID,
    service: ScriptService = Depends(get_script_service),
) -> ScriptRead:
    script = await service.get_script(project_id, script_id)
    return ScriptRead.model_validate(script)


@router.patch("/{script_id}", response_model=ScriptRead)
async def update_script(
    project_id: UUID,
    script_id: UUID,
    payload: ScriptUpdate,
    service: ScriptService = Depends(get_script_service),
) -> ScriptRead:
    script = await service.update_script(project_id, script_id, payload)
    return ScriptRead.model_validate(script)


@router.delete("/{script_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_script(
    project_id: UUID,
    script_id: UUID,
    service: ScriptService = Depends(get_script_service),
) -> None:
    await service.delete_script(project_id, script_id)
