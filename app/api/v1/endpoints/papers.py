from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, BackgroundTasks
from typing import List
import os
from app.core.dependencies import get_current_user
from app.schemas.document import PaperCreate, PaperOut, VersionOut
from app.services.oss import upload_file_to_oss

router = APIRouter()


@router.post("/upload", response_model=PaperOut)
async def upload_paper(
    file: UploadFile = File(...),
    current_user=Depends(get_current_user),
):
    # 验证文件扩展名
    if not file.filename.lower().endswith(".docx"):
        raise HTTPException(status_code=400, detail="仅支持 .docx 格式")
    contents = await file.read()
    size = len(contents)
    if size > 100 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="文件大小超过 100MB")

    # 简单 OSS 上传（返回一个 oss_key）
    oss_key = upload_file_to_oss(file.filename, contents)

    # TODO: persist to DB, create paper record and initial version v1.0
    paper_id = 1
    version = "v1.0"

    return PaperOut(id=paper_id, owner_id=current_user.get("sub", 0), latest_version=version, oss_key=oss_key)


@router.get("/{paper_id}/versions", response_model=List[VersionOut])
def list_versions(paper_id: int, current_user=Depends(get_current_user)):
    # TODO: query DB for versions
    return [VersionOut(version="v1.0", size=12345, created_at="2025-01-01T00:00:00Z", status="ok")]
