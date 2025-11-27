from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader
from langchain.schema import Document
from pathlib import Path
class DocumentLoader:
    '''
    Loads PDF/DOCX files and converts them into LangChain Document objects.
    '''

    @staticmethod
    def load(file_path: str) -> list[Document]:
        ext = Path(file_path).suffix.lower()

        if ext == ".pdf":
            return DocumentLoader.load_pdf(file_path)
        
        elif ext == ".docx":
            return DocumentLoader.load_docx(file_path)
        
        else:
            raise ValueError(f"Unsupported file type: {ext}")
        
    
    @staticmethod
    def load_pdf(file_path: str):
        loader = PyPDFLoader(file_path)
        return loader.load()
    
    @staticmethod
    def load_docx(file_path: str):
        loader = Docx2txtLoader(file_path)
        return loader.load()
    