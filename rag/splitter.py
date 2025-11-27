from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document



class DocumentSplitter:
    '''
    Splits a list of documents into smaller chunks for embeddings. 
    '''
    def __init__(self, chunk_size: int = 800, chunk_overlap: int = 200):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size = chunk_size,
            chunk_overlap = chunk_overlap
        )
    
    def split(self, docs: list[Document]) -> list[Document]:
        return self.splitter.split_documents(docs)