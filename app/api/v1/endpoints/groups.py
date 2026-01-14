from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from app.core.dependencies import get_current_user

router = APIRouter()


@router.post("/import")
async def import_groups(file: UploadFile = File(...), current_user=Depends(get_current_user)):
    # 这里只做接收并返回模拟结果；实际应解析 Excel 并写入 db
    if not file.filename.lower().endswith(('.xlsx', '.xls')):
        raise HTTPException(status_code=400, detail="请上传 Excel 文件（.xlsx/.xls）")
    content = await file.read()
    # TODO: parse excel, create osupervisions records
    return {"imported": 42}
