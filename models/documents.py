from pydantic import BaseModel
from typing import Optional

class ArticleDocument(BaseModel):
    source: str
    title: str
    content: str
    summary: Optional[str] = None
    published_at: Optional[str] = ""
    
    class Settings:
        name = "articles"