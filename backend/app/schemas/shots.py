"""分镜 Schema 定义。"""

from __future__ import annotations

from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field

from app.models.shot import ShotStatus
from app.schemas.common import IDMixin, ORMBaseModel, TimestampMixin


class ShotBase(BaseModel):
    script_id: Optional[UUID] = Field(None, description="关联脚本版本 ID，可选")
    sequence: int = Field(..., ge=1, description="镜头序号，从 1 开始")
    title: str = Field(..., min_length=1, max_length=255, description="镜头标题")
    description: str = Field(..., min_length=1, max_length=1024, description="镜头描述")
    duration_seconds: int = Field(default=5, ge=1, le=600, description="时长，秒")
    status: ShotStatus = Field(default=ShotStatus.TODO, description="状态")
    metadata: Optional[dict] = Field(None, description="额外信息，如景别等")


class ShotCreate(ShotBase):
    pass


class ShotUpdate(BaseModel):
    script_id: Optional[UUID] = None
    sequence: Optional[int] = Field(None, ge=1)
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, min_length=1, max_length=1024)
    duration_seconds: Optional[int] = Field(None, ge=1, le=600)
    status: Optional[ShotStatus] = None
    metadata: Optional[dict] = None


class ShotRead(ORMBaseModel, IDMixin, TimestampMixin):
    project_id: UUID
    script_id: Optional[UUID]
    sequence: int
    title: str
    description: str
    duration_seconds: int
    status: ShotStatus
    metadata: Optional[dict]
