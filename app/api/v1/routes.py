"""
API v1 路由汇总
"""
from fastapi import APIRouter
from app.api.v1.endpoints import health, documents, groups, papers, ai_review, annotations, admin

api_router = APIRouter()

# 注册各个端点路由
api_router.include_router(health.router, prefix="/health", tags=["健康检查"])
api_router.include_router(documents.router, prefix="/documents", tags=["documents"])
api_router.include_router(groups.router, prefix="/groups", tags=["groups"])
api_router.include_router(papers.router, prefix="/papers", tags=["papers"])
api_router.include_router(ai_review.router, prefix="/papers", tags=["ai"])
api_router.include_router(annotations.router, prefix="/annotations", tags=["annotations"])
api_router.include_router(admin.router, prefix="/admin", tags=["admin"])

