"""项目相关 Pydantic 模型。"""

from __future__ import annotations

from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field

from app.models.project import ProjectStatus
from app.schemas.common import IDMixin, ORMBaseModel, TimestampMixin


class ProjectBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200, description="项目名称")
    description: Optional[str] = Field(None, max_length=2000, description="项目简介")
    language: str = Field(default="zh-CN", max_length=32, description="项目语言")
    target_platform: str = Field(default="generic", max_length=64, description="目标平台")
    tags: list[str] = Field(default_factory=list, description="标签列表")


class ProjectCreate(ProjectBase):
    owner_id: UUID = Field(..., description="创建者用户 ID")
    status: ProjectStatus = Field(default=ProjectStatus.DRAFT, description="初始状态")


class ProjectUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=2000)
    language: Optional[str] = Field(None, max_length=32)
    target_platform: Optional[str] = Field(None, max_length=64)
    status: Optional[ProjectStatus] = None
    tags: Optional[list[str]] = None


class ProjectRead(ORMBaseModel, IDMixin, TimestampMixin):
    owner_id: UUID = Field(description="拥有者用户 ID")
    name: str
    description: Optional[str]
    language: str
    target_platform: str
    status: ProjectStatus
    tags: list[str]
