# Cryptocurrency news RAG

In this challenge I developed an application that enables users to perform retrieval augmented generation on a set of the latest cryptocurrency news.

The data is scrapped fromn cryptocurrency news articles, postprocessed  and uploaded to a Managed Weaviate cluster. 

Along with the data extraction scripts, the repo also provides a simple demo frontend application that communicates with a REST API to access the Weaviate client.

## Generating the Data

## RAG description

The RAG consists of the following steps:

1. From the given initial query, extract metadata. In this case, I extract the date from the query if any and the cryptocurrency mentioned. This information will be used for filtering the search results.

2. Given the user query, generate 5 additional queries to make the search more extensive.

3. Send the query to Weaviate using reranking of the results.

See [this notebook for reference](/notebooks/rag.ipynb)

## Starting the application

## Possible enhancements



