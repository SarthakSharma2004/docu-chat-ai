from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone, ServerlessSpec
from langchain.schema import Document
from core.config import get_settings
from rag.embedder import EmbedderModel

settings = get_settings()


_pc_cache = None
def get_pinecone_client():
    global _pc_cache
    if _pc_cache is None:
        _pc_cache = Pinecone(api_key=settings.PINECONE_API_KEY)
    return _pc_cache



class VectorStore:
    """
    Handles creating Pinecone index and storing embedded chunks.
    """

    @staticmethod
    def build_vector_store(chunks: list[Document], namespace:str, index_name: str = "docu-chat-index-3072"):
        """
        Splits → embeds → stores chunks into Pinecone.
        Returns the vectorstore object.
        """

        try : 
            # Load embedder 
            embedder = EmbedderModel.get_embedder()

            # Pinecone client
            pc = get_pinecone_client()

            # 1) Create index if it doesn't exist
            existing_indexes = [i["name"] for i in pc.list_indexes()]

            if index_name not in existing_indexes:
                pc.create_index(
                    name=index_name,
                    dimension= 3072,              # embedding dimension
                    metric="cosine",
                    spec=ServerlessSpec(
                        cloud="aws",
                        region="us-east-1"
                    )
                )

    

            # 2) Build Pinecone vector store
            vectorstore = PineconeVectorStore.from_documents(
                documents=chunks,
                embedding=embedder,
                index_name=index_name,
               
            )

            return vectorstore

        except Exception as e:
            raise RuntimeError(f"Failed to create Pinecone vector store: {e}")





