import concurrent.futures
import utils
from rag.query_expansion import QueryExpansion
from rag.query_meta_extractor import QueryMetaExtractor
from rag.qa_context import QAContext
from weaviate.classes.query import Filter, MetadataQuery
import logger_utils

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

logger = logger_utils.get_logger(__name__)


class DataRetriever:
    """
    Class for performing RAG with query expansion and filtering.
    """

    def __init__(self, weaviate_client, query: str):
        self.weaviate_client = weaviate_client
        self.query = query
        self._query_expander = QueryExpansion()
        self._metadata_extractor = QueryMetaExtractor()
        self._qa_extractor = QAContext()

    def _search_single_query(
        self, generated_query: str, currency: str, date: str, k: int
    ):
        
        articles = self.weaviate_client.collections.get("Articles")
        response = None

        try:
            if date != "":
                logger.info(f"Searching for date {date}")
                response = articles.query.near_text(
                    query=generated_query,
                    limit=k,
                    filters=Filter.by_property("published_at").equal(date),
                    return_metadata=MetadataQuery(distance=True)
                )
            else:
                logger.info(f"Searching without date")
                response = articles.query.near_text(
                    query=generated_query,
                    limit=k,
                    return_metadata=MetadataQuery(distance=True)
                )
        except Exception as e:
            logger.error(f"Search failed {e}")
            raise e

        return [{**item.properties, "uuid": str(item.uuid), "distance": item.metadata.distance} for item in response.objects]

    def retrieve_top_k(self, k: int, to_expand_to_n_queries: int) -> list:
        generated_queries = self._query_expander.generate_response(
            self.query, to_expand_to_n=to_expand_to_n_queries
        )
        logger.info(
            "Successfully generated queries for search.",
            num_queries=len(generated_queries),
        )

        currency = ""
        date = ""

        try:
            metadata = self._metadata_extractor.generate_response(self.query)
            currency = metadata.get("currency", "")
            date = metadata.get("date", "")
            logger.info(f"Extracted currency from query {currency}")
            logger.info(f"Extracted date from query {date}")
        except Exception as e:
            logger.info("Unable to extract metadata")

        with concurrent.futures.ThreadPoolExecutor() as executor:
            search_tasks = [
                executor.submit(self._search_single_query, query, currency, date, k)
                for query in generated_queries
            ]

            hits = [
                task.result() for task in concurrent.futures.as_completed(search_tasks)
            ]
            hits = utils.flatten(hits)
            hits = utils.remove_duplicates(hits)
            hits = utils.sort_by_distance(hits)

            # Extract top k
            hits = hits[:k]

        logger.info("All documents retrieved successfully.", num_documents=len(hits))
        context = "/n".join([hit["content"] for hit in hits])
        result = self._qa_extractor.rag_query(self.query, context)
        return result, hits
