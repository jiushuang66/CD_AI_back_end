from fastapi import APIRouter, Depends, HTTPException
from app.core.dependencies import get_current_user
from app.schemas.annotation import AnnotationCreate, AnnotationOut

router = APIRouter()


@router.post("/", response_model=AnnotationOut)
def create_annotation(payload: AnnotationCreate, current_user=Depends(get_current_user)):
    # TODO: 权限与坐标校验，持久化到数据库
    return AnnotationOut(id=1, paper_id=payload.paper_id, author_id=current_user.get("sub", 0), content=payload.content)
