from typing import Optional
from pydantic import BaseModel

class ArticleChunkModel(BaseModel):
    article_id: int
    chunk_id: str
    title: str
    chunk_content: str
    published_at: Optional[str] = ""