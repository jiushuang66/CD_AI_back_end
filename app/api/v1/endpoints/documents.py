"""Document upload endpoint"""
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
import pymysql
from app.database import get_db
from app.services.document import DocumentService
from app.schemas.document import DocumentResponse

router = APIRouter()


@router.post("/upload", response_model=DocumentResponse)
async def upload_document(file: UploadFile = File(...), db: pymysql.connections.Connection = Depends(get_db)):
    """Upload a document and store it in the database."""
    try:
        content = await file.read()
    except Exception:
        raise HTTPException(status_code=400, detail="Failed to read uploaded file")

    service = DocumentService(db)
    doc = service.create(filename=file.filename, content=content, content_type=file.content_type)
    return doc
