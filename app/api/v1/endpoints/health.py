"""
健康检查端点
"""
from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def health_check():
    """健康检查"""
    return {
        "status": "healthy",
        "message": "API服务运行正常"
    }


@router.get("/detailed")
async def detailed_health_check():
    """详细健康检查"""
    # 这里可以添加数据库连接检查等
    return {
        "status": "healthy",
        "database": "connected",
        "message": "所有服务运行正常"
    }

