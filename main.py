import os
import weaviate
from fastapi import FastAPI
from pydantic import BaseModel
from rag.retriever import DataRetriever


class SearchQuery(BaseModel):
    query: str

app = FastAPI()

client = weaviate.connect_to_wcs(
    cluster_url=os.getenv("WCS_CLUSTER_URL"),
    skip_init_checks=True,
    auth_credentials=weaviate.auth.AuthApiKey(os.getenv("WCS_API_KEY")),
    headers={
        "X-OpenAI-Api-Key": os.environ["OPENAI_API_KEY"]
    }
)

@app.get("/")
def root():
    return "FastAPI Running OK!"

@app.post("/search")
def rag_search(search_query: SearchQuery):
    try:
        results = DataRetriever(weaviate_client=client, query=search_query.query).retrieve_top_k(k=10, to_expand_to_n_queries=3)
        return {"status": 200, "results": results}
    except Exception as e:
        return {"status": 500, "exception": str(e)}
    finally:
        client.close()
    