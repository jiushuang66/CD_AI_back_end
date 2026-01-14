from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from app.core.dependencies import get_current_user
from app.services.oss import upload_file_to_oss

router = APIRouter()


def admin_only(user=Depends(get_current_user)):
    if user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="仅管理员可访问")
    return user


@router.post("/templates")
async def upload_template(file: UploadFile = File(...), user=Depends(admin_only)):
    content = await file.read()
    key = upload_file_to_oss(file.filename, content)
    # TODO: persist template ID and metadata
    return {"template_id": "tpl_1", "oss_key": key}


@router.get("/dashboard/stats")
def dashboard_stats(user=Depends(admin_only)):
    # TODO: 聚合 DB，按学院分组统计
    return {"total_papers": 123, "by_college": []}


@router.get("/audit/logs")
def audit_logs(user=Depends(admin_only), page: int = 1, page_size: int = 50):
    # TODO: 查询操作日志表并返回分页结果
    return {"items": [], "page": page, "page_size": page_size}
