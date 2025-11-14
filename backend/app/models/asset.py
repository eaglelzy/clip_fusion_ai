"""素材资产 ORM 定义。"""

from __future__ import annotations

import enum
import uuid
from typing import Any

from sqlalchemy import Enum, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin


class AssetType(str, enum.Enum):
    """资产类型枚举。"""

    VIDEO = "video"
    AUDIO = "audio"
    IMAGE = "image"
    TEXT = "text"
    SCRIPT = "script"


class AssetStatus(str, enum.Enum):
    """资产制作状态。"""

    DRAFT = "draft"
    APPROVED = "approved"
    NEEDS_REVISION = "needs_revision"


class Asset(TimestampMixin, Base):
    """项目/镜头下的具体素材文件记录。"""

    __tablename__ = "assets"
    __table_args__ = (
        UniqueConstraint("storage_path", name="uq_asset_storage_path"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        comment="资产 ID",
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
        ForeignKey("shots.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
        comment="关联镜头，可为空",
    )
    type: Mapped[AssetType] = mapped_column(
        Enum(AssetType, name="asset_type"),
        nullable=False,
        comment="资产类型",
    )
    status: Mapped[AssetStatus] = mapped_column(
        Enum(AssetStatus, name="asset_status"),
        nullable=False,
        default=AssetStatus.DRAFT,
        comment="当前状态",
    )
    storage_path: Mapped[str] = mapped_column(
        String(512),
        nullable=False,
        comment="素材在本地挂载中的路径",
    )
    format: Mapped[str | None] = mapped_column(
        String(32),
        nullable=True,
        comment="编码/格式，如 mp4/wav/png",
    )
    duration_ms: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
        comment="时长，毫秒",
    )
    resolution: Mapped[str | None] = mapped_column(
        String(32),
        nullable=True,
        comment="分辨率，如 1920x1080",
    )
    sample_rate: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
        comment="音频采样率",
    )
    extra_metadata: Mapped[dict[str, Any] | None] = mapped_column(
        "metadata",
        JSONB,
        nullable=True,
        comment="生成参数、字幕等附加数据",
    )

    project = relationship("Project", back_populates="assets")
    shot = relationship("Shot", back_populates="assets")

    def __repr__(self) -> str:  # pragma: no cover
        return f"Asset(id={self.id!s}, type={self.type})"
