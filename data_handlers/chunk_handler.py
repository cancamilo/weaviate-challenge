import hashlib
from models.chunk import ArticleChunkModel
from utils.chunking import chunk_text

class ChunkingHandler:
    @staticmethod
    def handle_article(article_id, article):
        
        chunks_list = []
        chunks = chunk_text(article.content)

        for chunk in chunks:
            try:
                model = ArticleChunkModel(
                    article_id=article_id,
                    title=article.title,
                    chunk_id=hashlib.md5(chunk.encode()).hexdigest(),
                    chunk_content=chunk,
                    published_at=article.published_at
                )
            except Exception as e:
                print(e.errors())
                raise e
            
            chunks_list.append(model)

        return chunks_list
