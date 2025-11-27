from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from rag.embedder import EmbedderModel
from langchain.schema import Document

from core.config import get_settings

settings = get_settings()

class VectorStore:
    def __init__(self, index_name: str = 'docu-chat-index'):

        self.index_name = index_name
        self.embedder = EmbedderModel.get_embedder()

        self.pc = Pinecone(
            api_key = settings.PINECONE_API_KEY
        )

    # --- Create index ---
    def build_index(self):
        '''Creates index if not present'''

        try :
            existing_index = [idx['name'] for idx in self.pc.list_indexes()]

            if self.index_name not in existing_index:
                self.pc.create_index(
                    name = self.index_name,
                    dimension = 768,
                    metric = "cosine",
                    spec = ServerlessSpec(
                        cloud = 'aws',
                        region = 'us-east-1'
                    )

                )

        except Exception as e:
            raise RuntimeError(f"Failed to create Pinecone index: {e}")




    # --- Build vectorstore instance ---

    def build_vector_store(self, chunks: list[Document]) -> PineconeVectorStore:
        '''
        Accepts a list of documents, embeds & stores chunks,
        and returns a vector store instance.
        '''

       

        try :
            vectorstore = PineconeVectorStore.from_documents(
                documents= chunks,
                embedding= self.embedder,
                index_name= self.index_name
            )

            return vectorstore

        except Exception as e:
            raise RuntimeError(f"Failed to build vector store from chunks: {e}")

        


        