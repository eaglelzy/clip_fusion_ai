"""分镜 CRUD 接口。"""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.schemas.shots import ShotCreate, ShotRead, ShotUpdate
from app.services.shot_service import ShotService

router = APIRouter()


def get_shot_service(session: AsyncSession = Depends(get_session)) -> ShotService:
    return ShotService(session)


@router.post("", response_model=ShotRead, status_code=status.HTTP_201_CREATED)
async def create_shot(
    project_id: UUID,
    payload: ShotCreate,
    service: ShotService = Depends(get_shot_service),
) -> ShotRead:
    shot = await service.create_shot(project_id, payload)
    return ShotRead.model_validate(shot)


@router.get("", response_model=list[ShotRead])
async def list_shots(
    project_id: UUID,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    service: ShotService = Depends(get_shot_service),
) -> list[ShotRead]:
    shots = await service.list_shots(project_id, skip=skip, limit=limit)
    return [ShotRead.model_validate(item) for item in shots]


@router.get("/{shot_id}", response_model=ShotRead)
async def get_shot(
    project_id: UUID,
    shot_id: UUID,
    service: ShotService = Depends(get_shot_service),
) -> ShotRead:
    shot = await service.get_shot(project_id, shot_id)
    return ShotRead.model_validate(shot)


@router.patch("/{shot_id}", response_model=ShotRead)
async def update_shot(
    project_id: UUID,
    shot_id: UUID,
    payload: ShotUpdate,
    service: ShotService = Depends(get_shot_service),
) -> ShotRead:
    shot = await service.update_shot(project_id, shot_id, payload)
    return ShotRead.model_validate(shot)


@router.delete("/{shot_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_shot(
    project_id: UUID,
    shot_id: UUID,
    service: ShotService = Depends(get_shot_service),
) -> None:
    await service.delete_shot(project_id, shot_id)
