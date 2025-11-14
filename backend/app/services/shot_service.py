"""分镜业务逻辑封装。"""

from __future__ import annotations

from typing import Sequence
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.project import Project
from app.models.script import Script
from app.models.shot import Shot
from app.schemas.shots import ShotCreate, ShotUpdate
from app.services.exceptions import ConflictError, NotFoundError


class ShotService:
    """镜头 CRUD 服务。"""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def _ensure_project(self, project_id: UUID) -> Project:
        project = await self.session.get(Project, project_id)
        if project is None:
            raise NotFoundError("项目不存在")
        return project

    async def _ensure_script_belongs(self, project_id: UUID, script_id: UUID | None) -> None:
        if script_id is None:
            return
        script = await self.session.get(Script, script_id)
        if script is None or script.project_id != project_id:
            raise NotFoundError("脚本不存在或不属于该项目")

    async def _get_shot(self, shot_id: UUID) -> Shot | None:
        return await self.session.get(Shot, shot_id)

    async def create_shot(self, project_id: UUID, payload: ShotCreate) -> Shot:
        await self._ensure_project(project_id)
        await self._ensure_script_belongs(project_id, payload.script_id)

        shot = Shot(project_id=project_id, **payload.model_dump())
        self.session.add(shot)
        try:
            await self.session.commit()
        except IntegrityError as exc:
            await self.session.rollback()
            raise ConflictError("镜头序号已存在") from exc
        await self.session.refresh(shot)
        return shot

    async def list_shots(self, project_id: UUID, *, skip: int, limit: int) -> Sequence[Shot]:
        await self._ensure_project(project_id)
        result = await self.session.execute(
            select(Shot)
            .where(Shot.project_id == project_id)
            .order_by(Shot.sequence)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def get_shot(self, project_id: UUID, shot_id: UUID) -> Shot:
        shot = await self._get_shot(shot_id)
        if shot is None or shot.project_id != project_id:
            raise NotFoundError("镜头不存在")
        return shot

    async def update_shot(self, project_id: UUID, shot_id: UUID, payload: ShotUpdate) -> Shot:
        shot = await self.get_shot(project_id, shot_id)
        data = payload.model_dump(exclude_unset=True)
        await self._ensure_script_belongs(project_id, data.get("script_id"))

        for field, value in data.items():
            setattr(shot, field, value)
        try:
            await self.session.commit()
        except IntegrityError as exc:
            await self.session.rollback()
            raise ConflictError("镜头序号已存在") from exc
        await self.session.refresh(shot)
        return shot

    async def delete_shot(self, project_id: UUID, shot_id: UUID) -> None:
        shot = await self.get_shot(project_id, shot_id)
        await self.session.delete(shot)
        await self.session.commit()
