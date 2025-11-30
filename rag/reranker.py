import cohere
from langchain.schema import Document
from core.config import get_settings

settings = get_settings()

class ReRanker:
    def __init__(self, model: str = "rerank-english-v3.0"):
        self.client = cohere.ClientV2(settings.COHERE_API_KEY)
        self.model = model

    def rerank(self, query: str, documents: list[Document], top_n: int = 5):
        if not documents:
            return []
        
        response = self.client.rerank(
            model= self.model , 
            query= query,
            documents= [doc.page_content for doc in documents],
            top_n= top_n
        )

        return [documents[r.index] for r in response.results]
    



    

# test

if __name__ == "__main__":
    try:
        rr = ReRanker()
        print("✅ Reranker initialized successfully!")

        # quick dummy test
        dummy_docs = [
            Document(page_content="New York is the capital of business."),
            Document(page_content="Washington, D.C. is the capital of the USA."),
            Document(page_content="Delhi is the capital of India.")
        ]

        results = rr.rerank("capital of the USA", dummy_docs, top_n=2)
        print("✅ Reranker test passed!")
        for r in results:
            print(r)
    except Exception as e:
        print("❌ Error:", e)
