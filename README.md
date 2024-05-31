# Weaviate Challenge: Cryptocurrency news RAG

In this challenge I developed an application that enables users to perform retrieval augmented generation on a set of the latest cryptocurrency news. The user simply enters a text about cryptocurrencies into the search input and gets an answer to their query together with the context that was used to generate that answer.

The data is scrapped from cryptocurrency news articles, postprocessed  and uploaded to a Managed Weaviate cluster. 

Along with the data extraction scripts, the repo also provides a simple demo frontend application that communicates with a REST API to access the Weaviate client.

The part 2.2 of the challenge can be found in a kaggle notebook here:

https://www.kaggle.com/code/camiloramirezf/job-postings-challenge

## Requirements:

For running this demo you need to have **node** installed in your system for running the frontend and **poetry** for managing the python dependencies and running the backend REST API service. Also, you need an OPENAI_KEY and a weaviate cluster running. The following environemnt variables must be set:


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
poetry run python backfill.py
```

This script will save a the [data/articles.csv](/data/articles.csv) file replacing the existing one.

## Loading data to weaviate

Use the [load_weaviate.py](/load_weaviate.py) script for loading the data (articles.csv) from the steps before.
This script will create the Articles collection in Weaviate and insert the documents:

```
poetry run python data_extraction.py
```

## Running the demo

The demo consist of a simple frontend application in **Next.js** and a backend application that uses **FastAPI**. 
Having uploaded the documents to weaviate in the previous steps, you are ready to run the demo.

Run the frontend:

```
make run-frontend
```

in a new terminal run the backend:

```
make run-backend
```

Note that everything is running in development mode. 

## RAG description

The RAG consists of the following steps:

1. From the given initial query, extract metadata. In this case, I extract the date from the query if any and the cryptocurrency mentioned. This information will be used for filtering the search results. The extraction of metadata is achieved using OpenAI function calling.

2. Given the user query, generate 5 additional queries to make the search more extensive.

3. Send each of the queries generated above to Weaviate using the filters and a near text search. Merge all the resulting hits from each query, remove duplicates, order by distance and select the top 5 only.

5. Prompt OpenAI to answer the user query providing the context found above.

See [this notebook for reference](/notebooks/rag.ipynb)

## Possible enhancements

- Dockerize everything
- Add more news sources as right now the dataset is limited to a few hundred articles.
- Add a NER module to extract entities from the articles. This would enable filtering by different kind of tags during search.
- Add endpoint to compute the sentiment of the market based on the news.
- I used a prompting for query expansion, parameter extraction and RAG. Using DSPy could optimize my prompts to produce better answers.
- The data is extracted manually by executing a script and batching the results to weaviate. For real time, it would be more beneficial to have a streaming pipeline of news. I am developing such approach [in this repository](https://github.com/cancamilo).



