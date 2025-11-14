"""导出记录表定义。"""

from __future__ import annotations

import enum
import uuid
from typing import Any

from sqlalchemy import Enum, ForeignKey, String
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin


class ExportFormat(str, enum.Enum):
    """导出支持的格式。"""

    AE = "after_effects"
    PR = "premiere_pro"
    ZIP = "zip_bundle"


class ExportStatus(str, enum.Enum):
    """导出流程状态。"""

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class ExportRecord(TimestampMixin, Base):
    """记录用户触发导出的历史及产物。"""

    __tablename__ = "export_records"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        comment="导出记录 ID",
    )
    project_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="关联项目",
    )
    format: Mapped[ExportFormat] = mapped_column(
        Enum(ExportFormat, name="export_format"),
        nullable=False,
        comment="导出格式",
    )
    status: Mapped[ExportStatus] = mapped_column(
        Enum(ExportStatus, name="export_status"),
        nullable=False,
        default=ExportStatus.PENDING,
        comment="执行状态",
    )
    output_path: Mapped[str | None] = mapped_column(
        String(512),
        nullable=True,
        comment="生成文件在存储中的路径",
    )
    extra_metadata: Mapped[dict[str, Any] | None] = mapped_column(
        "metadata",
        JSONB,
        nullable=True,
        comment="导出配置、版本信息等",
    )

    project = relationship("Project", back_populates="exports")

    def __repr__(self) -> str:  # pragma: no cover
        return f"ExportRecord(id={self.id!s}, format={self.format})"
