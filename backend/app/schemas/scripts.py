"""脚本相关 Schema。"""

from __future__ import annotations

from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field

from app.models.script import ScriptLanguage
from app.schemas.common import IDMixin, ORMBaseModel, TimestampMixin


class ScriptBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255, description="脚本标题")
    language: ScriptLanguage = Field(default=ScriptLanguage.ZH, description="脚本语言")
    content: dict = Field(default_factory=dict, description="脚本文本/结构化内容")
    is_locked: bool = Field(default=False, description="是否锁定编辑")
    version_snapshot: Optional[dict] = Field(None, description="版本快照")


class ScriptCreate(ScriptBase):
    version: Optional[int] = Field(None, ge=1, description="可显式指定版本号")


class ScriptUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    language: Optional[ScriptLanguage] = None
    content: Optional[dict] = None
    is_locked: Optional[bool] = None
    version_snapshot: Optional[dict] = None


class ScriptRead(ORMBaseModel, IDMixin, TimestampMixin):
    project_id: UUID
    version: int
    title: str
    language: ScriptLanguage
    content: dict
    is_locked: bool
    version_snapshot: Optional[dict]
