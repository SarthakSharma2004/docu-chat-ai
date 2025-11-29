from parser.document_loader import DocumentLoader
from rag.retriever import Retriever
from rag.vector_store import VectorStore
from rag.splitter import DocumentSplitter
from prompts.rag_prompt import RagPrompt
from prompts.contextualize_prompt import ContextualizePrompt  
from memory.redis_memory import get_session_history

from langchain_core.language_models import BaseChatModel
from langchain_core.documents import Document

from langchain.chains import create_retrieval_chain, create_history_aware_retriever
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.runnables.history import RunnableWithMessageHistory




class RagPipeline:
    def __init__(self, llm: BaseChatModel, index_name: str = "docu-chat-index"):
        
        self.llm = llm
        self.index_name = index_name
        self.vectorstore = None
        self.retriever = None
        self.rag_chain = None
        self.conversational_rag_chain = None
  

    def build_index(self, file_path: str):
        '''Builds vectorstore + MQR retriever on top'''

        try : 
            loader = DocumentLoader()
            docs = loader.load(file_path)
            
            splitter = DocumentSplitter()
            chunks = splitter.split(docs)

            self.vectorstore = VectorStore.build_vector_store(chunks, self.index_name)

            self.retriever = Retriever.get_retriever(self.vectorstore, self.llm)

            return {
                "status": "success",
                "message": "Document ingested successfully, index built",
                "chunks": len(chunks)
            }   
        

        except Exception as e:
            raise RuntimeError(f"Error ingesting document: {e}")
        

    def build_rag_chain(self):
        if not self.retriever:
            raise RuntimeError("Retriever not initialized. Build index first.")
        
        try :
            # ------ history-aware retriever --------
            history_aware_retriever = create_history_aware_retriever(
                self.llm,
                self.retriever,
                ContextualizePrompt.get_contextualize_prompt()
            )

            # --------stuff documents chain ------------
            question_ans_chain = create_stuff_documents_chain(
                self.llm,
                RagPrompt.get_rag_prompt()
            )

            # --------Retrieval chain ----------------
            rag_chain = create_retrieval_chain(
                history_aware_retriever, 
                question_ans_chain
            )
            self.rag_chain = rag_chain
            return self.rag_chain

        except Exception as e:
            raise RuntimeError(f"Error creating RAG chain: {e}")
        

    # ---- RAG + MEMORY CHAIN (REDIS) ---------
    def build_rag_with_memory(self):
        if not self.rag_chain:
            self.build_rag_chain()
        
        conversational_rag_chain = RunnableWithMessageHistory(
            self.rag_chain,
            get_session_history,
            input_messages_key= "input",
            history_messages_key= "chat_history",
            output_messages_key= "answer"
        )
        self.conversational_rag_chain = conversational_rag_chain

        return self.conversational_rag_chain
    
    
    # ---- queries with history ------------
    
    def user_input(self, session_id: str, question: str):
        if not self.conversational_rag_chain:
            self.build_rag_with_memory()

        try:
            response = self.conversational_rag_chain.invoke(
                {"input": question},
                config= {"configurable": {"session_id": session_id}}
            )
            return response['answer']
        
        except Exception as e:
            raise RuntimeError(f"Error processing user input: {e}")
    
      

            

















# class RagPipeline:

#     def __init__(self, llm: BaseChatModel, chunk_size: int = 400, chunk_overlap: int = 80):

#         self.llm = llm
#         self.chunk_size = chunk_size
#         self.chunk_overlap = chunk_overlap
#         self.prompt = RagPrompt.get_rag_prompt()

#         self.splitter = RecursiveCharacterTextSplitter(
#             chunk_size=self.chunk_size,
#             chunk_overlap=self.chunk_overlap
#         )
#         self.retriever = None


#     def ingest_documents(self, file_path: str):

#         try:
#             docs = DocumentLoader.load(file_path)
#             chunks = self.splitter.split_documents(docs)

#             vectorstore = VectorStore.build_vector_store(chunks)

#             # FIXED — Correct retriever creation
#             self.retriever = Retriever.get_retriever(vectorstore, self.llm)

#             return {
#                 "status": "success",
#                 "message": "Document ingested successfully, index built",
#                 "chunks": len(chunks)
#             }

#         except Exception as e:
#             raise RuntimeError(f"Error ingesting document: {e}")


#     def ask_question(self, query: str, language: str = "English"):

#         try:
#             if self.retriever is None:
#                 raise RuntimeError("Index not built. Call ingest_documents() first.")
            
#             retrieved_docs = self.retriever.get_relevant_documents(query)

#             stuff_chain = create_stuff_documents_chain(
#                 llm=self.llm,
#                 prompt=self.prompt
#             )

#             retrieval_chain = create_retrieval_chain(
#                 self.retriever,
#                 stuff_chain
#             )

#             response = retrieval_chain.invoke(
#                 {"input": query, "language": language}
#             )

#             return response['answer'], retrieved_docs

#         except Exception as e:
#             raise RuntimeError(f"Error during question-answering: {e}")

        
 