from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain_core.language_models import BaseChatModel
from langchain_core.retrievers import BaseRetriever
from langchain_pinecone import PineconeVectorStore
from langchain_groq import ChatGroq
class Retriever:
    '''
    Builds similarity retriever + MultiQuery retriever on top.
    '''

    def __init__(self, llm: BaseChatModel = ChatGroq(model='llama-3.1-8b-instant')):
        self.llm = llm
    
    
    def get_retriever(self, vector_store: PineconeVectorStore , k : int = 6) -> BaseRetriever :
        '''
        Convert vectorstore → retriever → multi-query retriever.
        '''

        try :
            retriever = vector_store.as_retriever(
                search_kwargs={"k": k}
            )

            multi_query_retriever = MultiQueryRetriever.from_llm(
                llm = self.llm,
                retriever = retriever
            )

            return multi_query_retriever

        except Exception as e :
            raise RuntimeError(f"Failed to build retriever: {e}")
        