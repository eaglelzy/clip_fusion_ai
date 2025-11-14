"""全局配置与环境变量加载。"""
from functools import lru_cache
from typing import List

from pydantic import AnyUrl, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """集中管理应用配置，支持从 .env 与环境变量加载。"""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # 应用基础配置
    app_name: str = "ai video"
    environment: str = "development"
    debug: bool = False

    # API 相关
    api_prefix: str = "/api"
    api_v1_prefix: str = "/api/v1"
    cors_allow_origins: List[str] = Field(default_factory=lambda: ["*"])

    # 日志与监控
    log_level: str = "INFO"

    # 数据库
    database_url: str = "postgresql+asyncpg://lizy:Lzy142857@db:5432/clipfusion"
    database_pool_size: int = 5
    database_max_overflow: int = 10
    database_echo: bool = False

    # 消息队列 / 缓存
    redis_url: AnyUrl = "redis://localhost:6379/0"
    broker_url: AnyUrl = "redis://localhost:6379/0"
    result_backend: AnyUrl = "redis://localhost:6379/1"


@lru_cache
def get_settings() -> Settings:
    """返回缓存的配置实例，避免重复解析 .env。"""

    return Settings()


settings = get_settings()
