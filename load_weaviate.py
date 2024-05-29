import weaviate
import weaviate.classes as wvc
import os
import pandas as pd

client = weaviate.connect_to_wcs(
    cluster_url="news-db-h6x724lk.weaviate.network",
    skip_init_checks=True,
    auth_credentials=weaviate.auth.AuthApiKey(os.getenv("WCS_API_KEY")),
    headers={
        "X-OpenAI-Api-Key": os.environ["OPENAI_API_KEY"]
    }
)

def load_to_weaviate():
    df = pd.read_csv("../data/articles.csv")

    if client.collections.exists("Articles"):
        client.collections.delete("Articles")  # Replace with your collection name

    client.collections.create(
        name="Articles",
        vectorizer_config=wvc.config.Configure.Vectorizer.text2vec_openai(),  
        generative_config=wvc.config.Configure.Generative.openai()
    )

    articles_objs = list()
    for i, d in df.iterrows():
        articles_objs.append({
            "title": d["title"],
            "summary": d["summary"],
            "content": d["content"],
            "published_at": d["published_at"]
        })

    articles = client.collections.get("Articles")
    articles.data.insert_many(articles_objs)

if __name__ == "__main__":
    try:
        load_to_weaviate()
    except Exception as e:
        print("Unable to upload to Weaviate", e)
    finally:
        client.close()
