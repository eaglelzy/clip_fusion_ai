"""项目相关 ORM 定义。"""

from __future__ import annotations

import enum
import uuid
from typing import Any

from sqlalchemy import Enum, ForeignKey, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin


class ProjectStatus(str, enum.Enum):
    """项目生命周期状态。"""

    DRAFT = "draft"
    ACTIVE = "active"
    ARCHIVED = "archived"


class Project(TimestampMixin, Base):
    """顶层项目实体，承载脚本/分镜/素材等资源。"""

    __tablename__ = "projects"
    __table_args__ = (
        UniqueConstraint("owner_id", "name", name="uq_project_owner_name"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        comment="项目 ID",
    )
    owner_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        comment="项目拥有者用户 ID",
    )
    name: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
        comment="项目名称",
    )
    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        comment="项目描述/简介",
    )
    language: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
        default="zh-CN",
        comment="主要语言，如 zh-CN/en-US",
    )
    target_platform: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
        default="generic",
        comment="面向的发布平台",
    )
    status: Mapped[ProjectStatus] = mapped_column(
        Enum(ProjectStatus, name="project_status"),
        nullable=False,
        default=ProjectStatus.DRAFT,
        comment="项目状态",
    )
    tags: Mapped[list[str]] = mapped_column(
        JSONB,
        nullable=False,
        default=list,
        comment="用户自定义标签数组",
    )
    extra: Mapped[dict[str, Any] | None] = mapped_column(
        JSONB,
        nullable=True,
        comment="额外元数据，可扩展字段",
    )

    owner = relationship("User", back_populates="projects")
    scripts = relationship(
        "Script",
        back_populates="project",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    shots = relationship(
        "Shot",
        back_populates="project",
        cascade="all, delete-orphan",
        passive_deletes=True,
        order_by="Shot.sequence",
    )
    assets = relationship(
        "Asset",
        back_populates="project",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    synthesis_tasks = relationship(
        "SynthesisTask",
        back_populates="project",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    exports = relationship(
        "ExportRecord",
        back_populates="project",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    def __repr__(self) -> str:  # pragma: no cover
        return f"Project(id={self.id!s}, name={self.name!r})"
