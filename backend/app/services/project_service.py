"""项目相关业务逻辑。"""

from __future__ import annotations

from typing import Sequence
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.project import Project
from app.schemas.projects import ProjectCreate, ProjectUpdate
from app.services.exceptions import ConflictError, NotFoundError
from app.models.user import User


class ProjectService:
    """封装项目的增删改查，避免路由层直接操作 ORM。"""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_project(self, payload: ProjectCreate) -> Project:
        # 判断同名项目是否已存在可在此处添加
        user = await self.session.get(User, payload.owner_id)  
        if user is None:
            raise NotFoundError("创建者用户不存在")

        project = Project(**payload.model_dump())
        self.session.add(project)
        try:
            await self.session.commit()
        except IntegrityError as exc:
            await self.session.rollback()
            raise ConflictError("项目名称已存在") from exc
        await self.session.refresh(project)
        return project

    async def list_projects(self, *, skip: int, limit: int) -> Sequence[Project]:
        result = await self.session.execute(
            select(Project).order_by(Project.created_at.desc()).offset(skip).limit(limit)
        )
        return result.scalars().all()

    async def get_project(self, project_id: UUID) -> Project:
        project = await self.session.get(Project, project_id)
        if project is None:
            raise NotFoundError("项目不存在")
        return project

    async def update_project(self, project_id: UUID, payload: ProjectUpdate) -> Project:
        project = await self.get_project(project_id)
        data = payload.model_dump(exclude_unset=True)
        for field, value in data.items():
            setattr(project, field, value)
        try:
            await self.session.commit()
        except IntegrityError as exc:
            await self.session.rollback()
            raise ConflictError("项目名称已存在") from exc
        await self.session.refresh(project)
        return project

    async def delete_project(self, project_id: UUID) -> None:
        project = await self.get_project(project_id)
        await self.session.delete(project)
        await self.session.commit()
