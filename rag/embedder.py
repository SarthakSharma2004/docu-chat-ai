from core.config import get_settings
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings

settings = get_settings()

_embedder_cache = None
class EmbedderModel:
    ''' 
    Loads and provides embedding model for vector store.
    '''

    @staticmethod
    def get_embedder():
        global _embedder_cache
        if _embedder_cache is None:
            _embedder_cache = HuggingFaceEmbeddings(model_name=settings.HUGGINGFACE_EMBEDDING_MODEL)
        return _embedder_cache