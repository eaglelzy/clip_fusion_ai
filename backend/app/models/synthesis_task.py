"""语音/多媒体生成任务表。"""

from __future__ import annotations

import enum
import uuid
from typing import Any

from sqlalchemy import Enum, ForeignKey, String
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin


class TaskStatus(str, enum.Enum):
    """异步任务状态。"""

    QUEUED = "queued"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class SynthesisTask(TimestampMixin, Base):
    """存储 TTS/多媒体生成的任务及结果路径。"""

    __tablename__ = "synthesis_tasks"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        comment="任务 ID",
    )
    project_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="所属项目",
    )
    shot_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("shots.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
        comment="关联镜头，可选",
    )
    voice_preset_id: Mapped[str | None] = mapped_column(
        String(64),
        nullable=True,
        comment="使用的音色预设 ID",
    )
    payload: Mapped[dict[str, Any]] = mapped_column(
        JSONB,
        nullable=False,
        default=dict,
        comment="任务参数快照，方便重跑",
    )
    status: Mapped[TaskStatus] = mapped_column(
        Enum(TaskStatus, name="synthesis_task_status"),
        nullable=False,
        default=TaskStatus.QUEUED,
        comment="任务状态",
    )
    result_path: Mapped[str | None] = mapped_column(
        String(512),
        nullable=True,
        comment="生成文件在本地的路径",
    )
    error_message: Mapped[str | None] = mapped_column(
        String(512),
        nullable=True,
        comment="失败原因，最多 512 字符",
    )
    extra_metadata: Mapped[dict[str, Any] | None] = mapped_column(
        "metadata",
        JSONB,
        nullable=True,
        comment="运行日志、用时等信息",
    )

    project = relationship("Project", back_populates="synthesis_tasks")
    shot = relationship("Shot", back_populates="synthesis_tasks")

    def __repr__(self) -> str:  # pragma: no cover
        return f"SynthesisTask(id={self.id!s}, status={self.status})"
