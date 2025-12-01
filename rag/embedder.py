from core.config import get_settings

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
            _embedder_cache = GoogleGenerativeAIEmbeddings(model= settings.GEMINI_EMBEDDING_MODEL, google_api_key= settings.GOOGLE_API_KEY)
        return _embedder_cache