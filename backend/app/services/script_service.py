"""脚本业务逻辑封装。"""

from __future__ import annotations

from typing import Sequence
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.project import Project
from app.models.script import Script
from app.schemas.scripts import ScriptCreate, ScriptUpdate
from app.services.exceptions import ConflictError, NotFoundError


class ScriptService:
    """脚本 CRUD 操作。"""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def _ensure_project(self, project_id: UUID) -> Project:
        project = await self.session.get(Project, project_id)
        if project is None:
            raise NotFoundError("项目不存在")
        return project

    async def _get_script(self, script_id: UUID) -> Script | None:
        return await self.session.get(Script, script_id)

    async def create_script(self, project_id: UUID, payload: ScriptCreate) -> Script:
        await self._ensure_project(project_id)

        version = payload.version
        if version is None:
            result = await self.session.execute(
                select(func.max(Script.version)).where(Script.project_id == project_id)
            )
            max_version = result.scalar() or 0
            version = max_version + 1

        script = Script(project_id=project_id, version=version, **payload.model_dump(exclude={"version"}))
        self.session.add(script)
        try:
            await self.session.commit()
        except IntegrityError as exc:
            await self.session.rollback()
            raise ConflictError("脚本版本重复") from exc
        await self.session.refresh(script)
        return script

    async def list_scripts(self, project_id: UUID, *, skip: int, limit: int) -> Sequence[Script]:
        await self._ensure_project(project_id)
        result = await self.session.execute(
            select(Script)
            .where(Script.project_id == project_id)
            .order_by(Script.version.desc())
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def get_script(self, project_id: UUID, script_id: UUID) -> Script:
        script = await self._get_script(script_id)
        if script is None or script.project_id != project_id:
            raise NotFoundError("脚本不存在")
        return script

    async def update_script(self, project_id: UUID, script_id: UUID, payload: ScriptUpdate) -> Script:
        script = await self.get_script(project_id, script_id)
        data = payload.model_dump(exclude_unset=True)
        for field, value in data.items():
            setattr(script, field, value)
        await self.session.commit()
        await self.session.refresh(script)
        return script

    async def delete_script(self, project_id: UUID, script_id: UUID) -> None:
        script = await self.get_script(project_id, script_id)
        await self.session.delete(script)
        await self.session.commit()
