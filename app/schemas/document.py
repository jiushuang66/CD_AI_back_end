from pydantic import BaseModel
from typing import Optional


class PaperCreate(BaseModel):
    title: str


class PaperOut(BaseModel):
    id: int
    owner_id: int
    latest_version: str
    oss_key: Optional[str]


class VersionOut(BaseModel):
    version: str
    size: int
    created_at: str
    status: str
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class DocumentResponse(BaseModel):
    id: int
    filename: str
    content_type: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True
