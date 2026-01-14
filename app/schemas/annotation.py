from pydantic import BaseModel


class AnnotationCreate(BaseModel):
    paper_id: int
    paragraph_id: str | None = None
    coordinates: dict | None = None
    content: str


class AnnotationOut(BaseModel):
    id: int
    paper_id: int
    author_id: int
    content: str
