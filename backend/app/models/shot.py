"""分镜镜头 ORM 定义。"""

from __future__ import annotations

import enum
import uuid
from typing import Any

from sqlalchemy import Enum, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin


class ShotStatus(str, enum.Enum):
    """镜头制作状态。"""

    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"


class Shot(TimestampMixin, Base):
    """镜头行，绑定脚本片段与资产。"""

    __tablename__ = "shots"
    __table_args__ = (
        UniqueConstraint("project_id", "sequence", name="uq_shot_project_sequence"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        comment="镜头 ID",
    )
    project_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="所属项目",
    )
    script_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("scripts.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
        comment="来源脚本版本，可为空",
    )
    sequence: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        comment="镜头顺序，从 1 开始",
    )
    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        comment="镜头标题",
    )
    description: Mapped[str] = mapped_column(
        String(1024),
        nullable=False,
        comment="镜头描述/动作分解",
    )
    duration_seconds: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=5,
        comment="预计时长，秒",
    )
    status: Mapped[ShotStatus] = mapped_column(
        Enum(ShotStatus, name="shot_status"),
        nullable=False,
        default=ShotStatus.TODO,
        comment="镜头当前状态",
    )
    extra_metadata: Mapped[dict[str, Any] | None] = mapped_column(
        "metadata",
        JSONB,
        nullable=True,
        comment="额外信息，如景别、镜头类型等",
    )

    project = relationship("Project", back_populates="shots")
    script = relationship("Script", back_populates="shots")
    assets = relationship(
        "Asset",
        back_populates="shot",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    synthesis_tasks = relationship(
        "SynthesisTask",
        back_populates="shot",
        passive_deletes=True,
    )

    def __repr__(self) -> str:  # pragma: no cover
        return f"Shot(id={self.id!s}, seq={self.sequence})"
