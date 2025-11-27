from core.config import get_settings
from langchain_huggingface import HuggingFaceEmbeddings

settings = get_settings()

class EmbedderModel:
    ''' 
    Loads and provides embedding model for vector store.
    '''

    def __init__(self):
        self.embedder = HuggingFaceEmbeddings(model_name = settings.HUGGINGFACE_EMBEDDING_MODEL)


    def get_embedder(self):
        '''Returns embedding model'''

        return self.embedder