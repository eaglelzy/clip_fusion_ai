"""FastAPI 应用入口，聚合 API 及健康检查。"""
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.api_error import ApiError
from app.api.v1.routes import router as api_router
from app.core.config import get_settings
from app.core.exceptions import (
    api_error_handler,
    generic_error_handler,
    redis_error_handler,
    request_validation_error_handler,
    service_error_handler,
)
from app.core.logging import configure_logging
from app.core.redis import RedisBackendError
from app.services.exceptions import ServiceError

settings = get_settings()
configure_logging()

def create_app() -> FastAPI:
    """创建并配置 FastAPI 应用实例。"""
    app = FastAPI(
        title=settings.app_name,
        debug=settings.debug,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_allow_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(api_router, prefix=settings.api_prefix)

    app.add_exception_handler(ServiceError, service_error_handler)
    app.add_exception_handler(ApiError, api_error_handler)
    app.add_exception_handler(Exception, generic_error_handler)
    app.add_exception_handler(RequestValidationError, request_validation_error_handler)
    app.add_exception_handler(RedisBackendError, redis_error_handler)
    return app


app = create_app()
