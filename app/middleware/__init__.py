"""
中间件模块
"""
from fastapi import FastAPI
from app.middleware.logging import LoggingMiddleware


def setup_middleware(app: FastAPI):
    """设置中间件"""
    app.add_middleware(LoggingMiddleware)

