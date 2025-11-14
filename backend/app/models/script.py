"""脚本版本表定义。"""

from __future__ import annotations

import uuid
from enum import Enum
from typing import Any

from sqlalchemy import Boolean, Enum as SQLEnum, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin


class ScriptLanguage(str, Enum):
    """脚本语言枚举，方便后续扩展。"""

    ZH = "zh-CN"
    EN = "en-US"


class Script(TimestampMixin, Base):
    """项目脚本的版本快照。"""

    __tablename__ = "scripts"
    __table_args__ = (
        UniqueConstraint("project_id", "version", name="uq_script_project_version"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        comment="脚本版本 ID",
    )
    project_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="所属项目 ID",
    )
    version: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=1,
        comment="脚本版本号，从 1 递增",
    )
    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        comment="脚本标题或章节名",
    )
    language: Mapped[ScriptLanguage] = mapped_column(
        SQLEnum(ScriptLanguage, name="script_language"),
        nullable=False,
        default=ScriptLanguage.ZH,
        comment="脚本使用的语言",
    )
    content: Mapped[dict[str, Any]] = mapped_column(
        JSONB,
        nullable=False,
        default=dict,
        comment="结构化脚本内容（场景、对白等）",
    )
    version_snapshot: Mapped[dict[str, Any] | None] = mapped_column(
        JSONB,
        nullable=True,
        comment="可选的全文快照，预留回滚用",
    )
    is_locked: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        comment="是否锁定编辑，以防误改",
    )

    project = relationship("Project", back_populates="scripts")
    shots = relationship(
        "Shot",
        back_populates="script",
        passive_deletes=True,
    )

    def __repr__(self) -> str:  # pragma: no cover
        return f"Script(id={self.id!s}, project_id={self.project_id!s}, version={self.version})"
