import os
from langchain_openai import ChatOpenAI
from llm_components.chain import GeneralChain
from llm_components.prompt_templates import QueryExpansionTemplate

class QueryExpansion:
    @staticmethod
    def generate_response(query: str, to_expand_to_n: int) -> list[str]:
        query_expansion_template = QueryExpansionTemplate()
        prompt_template = query_expansion_template.create_template(to_expand_to_n)
        model = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

        chain = GeneralChain().get_chain(
            llm=model, output_key="expanded_queries", template=prompt_template, verbose=False
        )

        response = chain.invoke({"question": query})
        result = response["expanded_queries"]

        queries = result.strip().split(query_expansion_template.separator)
        stripped_queries = [
            stripped_item for item in queries if (stripped_item := item.strip())
        ]

        return stripped_queries
