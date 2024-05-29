import os
import weaviate
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from rag.retriever import DataRetriever


class SearchQuery(BaseModel):
    query: str

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.on_event("startup")
async def startup_event():
    app.state.client = weaviate.connect_to_wcs(
        cluster_url=os.getenv("WCS_CLUSTER_URL"),
        skip_init_checks=True,
        auth_credentials=weaviate.auth.AuthApiKey(os.getenv("WCS_API_KEY")),
        headers={
            "X-OpenAI-Api-Key": os.environ["OPENAI_API_KEY"]
        }
    )

@app.on_event("shutdown")
async def shutdown_event():
    app.state.client.close()

@app.get("/")
def root():
    return "FastAPI Running OK!"

@app.post("/search")
def rag_search(search_query: SearchQuery):
    try:
        answer, hits = DataRetriever(weaviate_client=app.state.client, query=search_query.query).retrieve_top_k(k=10, to_expand_to_n_queries=2)
        return {
            "status": 200, 
            "result": {
                "answer": answer,
                "hits": hits
            }
        }
    except Exception as e:
        return {"status": 500, "exception": str(e)}
    