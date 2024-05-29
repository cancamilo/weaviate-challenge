from abc import ABC, abstractmethod
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain.prompts import PromptTemplate, BasePromptTemplate, ChatPromptTemplate


class BaseTemplate(ABC, BaseModel):
    @abstractmethod
    def create_template(self) -> BasePromptTemplate:
        pass

class QueryExpansionTemplate(BaseTemplate):
    prompt: str = """You are an AI language model assistant. Your task is to generate {n_expansions}
    different versions of the given user question to retrieve relevant documents from a vector
    database. By generating multiple perspectives on the user question, your goal is to help
    the user overcome some of the limitations of the distance-based similarity search.
    Provide these alternative questions seperated by '{separator}'.
    Original question: {question}"""

    @property
    def separator(self) -> str:
        return "#next-question#"

    def create_template(self, n_expansions: int) -> BasePromptTemplate:
        return PromptTemplate(
            template=self.prompt,
            input_variables=["question"],
            partial_variables={
                "separator": self.separator,
                "n_expansions": n_expansions,
            },
        )
    
class QueryMetadata(BaseModel):
    """Information to extract from the user query. 
    Dates should be transformed to yyyy-mm-dd and be relative to the given current date"""

    currency: str = Field(description="The cryptocurrency mentioned in the query or empty string if not found.")
    date: str = Field(description="date from the text in the format yyyy-mm-dd or empty if no date found")

class QueryMetaTemplate(BaseTemplate):

    def create_template(self) -> BasePromptTemplate:
        return ChatPromptTemplate.from_messages([
            ("system", "Today´s date is {current_date}."),
            ("human", "{user_query}"),
        ])

class QATemplate(BaseTemplate):

    prompt: str = """You are an AI language model assistant whose job is to provide answers to cryptocurrency investors
    in order to make informed decisions based on news. If the user query is a question, provide answers based on the given context only if it is relevant.
    If the user query is not a question, just give a summary of the relevant content in the context related to the query. 
    USER_QUERY:
    ```{user_query}```
    CONTEXT:
    {context}"""

    def create_template(self) -> BasePromptTemplate:
        return PromptTemplate(
            template=self.prompt,
            input_variables=["user_query", "context"]
        )
