<div align="center">

![Python](https://img.shields.io/badge/Python-3.13-blue?logo=python)
![RAG](https://img.shields.io/badge/RAG-Conversational-orange)
![LangChain](https://img.shields.io/badge/LangChain-green)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?logo=docker)
![AWS EC2](https://img.shields.io/badge/AWS-EC2-orange?logo=amazonaws)
![Streamlit](https://img.shields.io/badge/Streamlit-UI-FF4B4B?logo=streamlit)
![Multi-Query Retriever](https://img.shields.io/badge/Retriever-Multi--Query-yellow)
![Cross Encoder](https://img.shields.io/badge/Re--Ranking-Cross%20Encoder-purple)
![Pinecone](https://img.shields.io/badge/Pinecone-Vector%20DB-0A1FFF)
![Redis](https://img.shields.io/badge/Redis-Chat%20Memory-DC382D?logo=redis)
![Gemini](https://img.shields.io/badge/Gemini-Embeddings-blueviolet)
![Cohere](https://img.shields.io/badge/Cohere-LLM%20%26%20Embeddings-FF6B00)
![LLaMA](https://img.shields.io/badge/LLaMA-LLM-8A2BE2)
![Groq](https://img.shields.io/badge/Groq-Ultra%20Fast%20Inference-black)
![LangSmith](https://img.shields.io/badge/LangSmith-Observability-green)

</div>

---

# 🧠📄 DocuChat - A Conversational RAG-Based Document Chat System



---



## 📄 Overview

- DocuChat is a conversational AI system that enables intelligent, multi-turn interactions over user-uploaded documents using an advanced Retrieval-Augmented Generation (RAG) architecture.

- The system combines multi-query semantic retrieval, cross-encoder–based re-ranking, and persistent conversational memory to deliver highly accurate, context-aware responses across long documents.

- Built with a FastAPI backend and Streamlit chat UI, DocuChat is fully containerized using Docker, monitored via LangSmith, and deployed on AWS for scalable, low-latency inference.



---



## 🧠 System Architecture


1. **Document Upload & Parsing**
   - Users upload PDFs or word documents via the Streamlit UI.
   - Documents are chunked and preprocessed using LangChain document loaders.

2. **Embedding & Vector Storage**
   - Text chunks are converted into dense vector embeddings using Gemini  embedding model (gemini-embedding-001).
   - Embeddings are stored in Pinecone for scalable and efficient similarity search.

3. **Multi-Query Retrieval**
   - User queries are expanded into multiple semantically diverse variants.
   - Each variant retrieves relevant chunks from the vector store, improving recall across complex documents.

4. **Cross-Encoder Re-Ranking**
   - Retrieved chunks are re-ranked using a transformer-based cross-encoder (from cohere).
   - This step prioritizes the most contextually relevant passages, significantly improving answer precision.

5. **Conversational Memory**
   - Chat history is stored in Redis Cloud to maintain session-based conversational context.
   - Enables coherent, multi-turn interactions with sub-millisecond retrieval latency.

6. **LLM Response Generation**
   - The top-ranked context is passed to LLaMA via Groq for ultra-fast inference.
   - Responses are generated with full awareness of prior conversation and document context.

7. **Observability & Monitoring**
   - End-to-end pipeline traces are logged using LangSmith for debugging, evaluation, and performance monitoring.



---



## ⚙️ Tech Stack

| Layer | Technologies |
|------|-------------|
| **Language** | Python 3.13 |
| **LLM & Inference** | LLaMA, Groq |
| **Embeddings** | Gemini Embedding Model |
| **RAG Framework** | LangChain |
| **Retrieval Strategy** | Multi-Query Retriever |
| **Re-Ranking** | Transformer-based Cross Encoder from Cohere|
| **Vector Database** | Pinecone |
| **Memory Store** | Redis Cloud |
| **Backend API** | FastAPI, Pydantic v2 |
| **Frontend UI** | Streamlit (Chat-style Interface) |
| **Observability** | LangSmith |
| **Containerization** | Docker |
| **Cloud Deployment** | AWS EC2 |



---



## 🚀 Key Features

- **Advanced Conversational RAG**
  - Enables natural, multi-turn conversations over uploaded documents with context retention across interactions.

- **Multi-Query Semantic Retrieval**
  - Expands user queries into multiple semantic variants to improve document coverage and retrieval recall.

- **Cross-Encoder–Based Re-Ranking**
  - Applies transformer-based re-ranking on retrieved chunks to prioritize the most contextually relevant passages, significantly improving response precision.

- **Persistent Conversational Memory**
  - Stores session-based chat history in Redis Cloud, enabling coherent conversations with ultra-low retrieval latency.

- **Scalable Vector Search**
  - Utilizes Pinecone for efficient and scalable similarity search across large document collections.

- **Ultra-Fast LLM Inference**
  - Leverages LLaMA models served via Groq for low-latency, high-throughput response generation.

- **Production-Ready Deployment**
  - Fully containerized using Docker, deployed on AWS EC2, and monitored end-to-end using LangSmith.

- **Interactive Chat UI**
  - Clean, chat-style Streamlit interface for seamless document upload and real-time interaction.



---



## 🛠️ Installation & Setup

### 📦 Clone the Repository

```bash
git clone https://github.com/SarthakSharma2004/docu-chat-ai.git
```

### 🔑 Environment Variables

```bash
Create a .env file in the root directory:

GOOGLE_API_KEY=
GROQ_API_KEY=
LANGCHAIN_API_KEY=
LANGCHAIN_TRACING_V2=
LANGCHAIN_PROJECT=
PINECONE_API_KEY=
REDIS_URL=
COHERE_API_KEY=
```

### 🎨 Run Locally (Without Docker)

```bash
pip install -r requirements.txt
uvicorn main:app --reload
streamlit run app.py
```


### 🐳 Run with Docker 

```bash
docker build -t docuchat .
docker run -p 8000:8000 -p 8501:8501 --env-file .env docuchat
```
