from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class DocumentRecord:
    id: int
    filename: str
    content: bytes
    content_type: Optional[str]
    created_at: datetime
