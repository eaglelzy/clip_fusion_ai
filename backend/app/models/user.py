"""用户表定义。"""

from __future__ import annotations

import uuid

from sqlalchemy import DateTime, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin


class User(TimestampMixin, Base):
    """平台用户，用于项目归属与后续权限扩展。"""

    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        comment="用户主键，UUID",
    )
    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True,
        comment="登录邮箱，唯一",
    )
    display_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        comment="展示昵称",
    )
    hashed_password: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        comment="BCrypt 等方式加密后的密码",
    )
    bio: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        comment="个人简介，可选",
    )
    last_login_at: Mapped[DateTime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        comment="最近登录时间",
    )

    projects = relationship(
        "Project",
        back_populates="owner",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    def __repr__(self) -> str:  # pragma: no cover - 调试辅助
        return f"User(id={self.id!s}, email={self.email!r})"
