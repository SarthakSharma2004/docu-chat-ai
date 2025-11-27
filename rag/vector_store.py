# rag/vector_store.py

from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone, ServerlessSpec
from langchain.schema import Document
from core.config import get_settings
from rag.embedder import Embedder

settings = get_settings()

# Load embedder once
embedder = Embedder.get_embedder()

# Pinecone client
pc = Pinecone(api_key=settings.PINECONE_API_KEY)


class VectorStore:
    """
    Handles creating Pinecone index and storing embedded chunks.
    """

    @staticmethod
    def build_vector_store(chunks: list[Document], index_name: str = "docu-chat-index"):
        """
        Splits → embeds → stores chunks into Pinecone.
        Returns the vectorstore object.
        """

        # 1) Create index if it doesn't exist
        existing_indexes = [i["name"] for i in pc.list_indexes()]

        if index_name not in existing_indexes:
            pc.create_index(
                name=index_name,
                dimension=768,              # embedding dimension
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
            index_name=index_name
        )

        return vectorstore







# from pinecone import Pinecone, ServerlessSpec
# from langchain_pinecone import PineconeVectorStore
# from rag.embedder import EmbedderModel
# from langchain_core.documents import Document


# from core.config import get_settings

# settings = get_settings()

# class VectorStore:
#     def __init__(self, index_name: str = 'docu-chat-index'):

#         self.index_name = index_name
#         self.embedder = EmbedderModel.get_embedder()

#         self.pc = Pinecone(
#             api_key = settings.PINECONE_API_KEY
#         )

#     # --- Create index ---
#     def build_index(self):
#         '''Creates index if not present'''

#         try :
#             existing_index = [idx['name'] for idx in self.pc.list_indexes()]

#             if self.index_name not in existing_index:
#                 self.pc.create_index(
#                     name = self.index_name,
#                     dimension = 768,
#                     metric = "cosine",
#                     spec = ServerlessSpec(
#                         cloud = 'aws',
#                         region = 'us-east-1'
#                     )

#                 )

#         except Exception as e:
#             raise RuntimeError(f"Failed to create Pinecone index: {e}")




#     # --- Build vectorstore instance ---

#     def build_vector_store(self, chunks: list[Document]) -> PineconeVectorStore:
#         '''
#         Accepts a list of documents, embeds & stores chunks,
#         and returns a vector store instance.
#         '''

       

#         try :
#             vectorstore = PineconeVectorStore.from_documents(
#                 documents= chunks,
#                 embedding= self.embedder,
#                 index_name= self.index_name
#             )

#             return vectorstore

#         except Exception as e:
#             raise RuntimeError(f"Failed to build vector store from chunks: {e}")

        


        