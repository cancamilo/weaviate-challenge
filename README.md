# Weaviate Challenge: Cryptocurrency news RAG

In this challenge I developed an application that enables users to perform retrieval augmented generation on a set of the latest cryptocurrency news. The user simply enters a text about cryptocurrencies into the search input and gets an answer to their query together with the context that was used to generate that answer.

The data is scrapped fromn cryptocurrency news articles, postprocessed  and uploaded to a Managed Weaviate cluster. 

Along with the data extraction scripts, the repo also provides a simple demo frontend application that communicates with a REST API to access the Weaviate client.

## Requirements:

For running this demo you need to have **node** installed in your system for running the frontend and **poetry** for managing the python dependencies. Also, you need an OPEN_AI_KEY and a weaviate cluster running. The following environemnt variables must be set:


```
#Weaviate Configs
WCS_CLUSTER_URL="YOUR CLUSTER URL"
WCS_API_KEY="YOUR CLUSTER KEY"

# Retrieval config
OPENAI_API_KEY="YOUR OPENAI API KEY"
```

## Generating the Data

You can either generate the data yourself by running the [backfill.py script](/backfill.py):

```
poetry run backfill.py
```

This script will save a the [data/articles.csv](/data/articles.csv) file replacing the existing one.

## Loading data to weaviate

Use the [load_weaviate.py](/load_weaviate.py) script for loading the data (articles.csv) from the steps before.
This script will create the Articles collection in Weaviate and insert the documents.

## Running the demo

The demo consist of a simple frontend application in **Next.js** and a backend application that uses **FastAPI**. 
Having uploaded the documents to weaviate in the previous steps, you are ready to run the demo.

Run the frontend:

```
make run-frontend
```

Backend:

```
make run-backend
```

## RAG description

The RAG consists of the following steps:

1. From the given initial query, extract metadata. In this case, I extract the date from the query if any and the cryptocurrency mentioned. This information will be used for filtering the search results.

2. Given the user query, generate 5 additional queries to make the search more extensive.

3. Send the query to Weaviate using reranking of the results.

See [this notebook for reference](/notebooks/rag.ipynb)

## Starting the application

## Possible enhancements



