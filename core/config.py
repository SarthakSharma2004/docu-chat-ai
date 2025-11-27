from pydantic_settings import BaseSettings , SettingsConfigDict
from pydantic import Field
from functools import lru_cache

class Settings(BaseSettings):
    '''
    Defines a centralized configuration class that loads and validates environment variables (like API keys etc. )
    '''

    GOOGLE_API_KEY: str = Field(..., description="Google API Key")


    GROQ_API_KEY: str = Field(..., description="Groq API Key")


    PINECONE_API_KEY: str = Field(..., description="Pinecone API Key")

    
    LANGCHAIN_API_KEY: str = Field(..., description="LangSmith/LangChain API Key")
    LANGCHAIN_TRACING_V2: bool = Field(default=True, description="Enable LangSmith tracing")
    LANGCHAIN_PROJECT: str = Field(..., description="LangSmith project name")


    HUGGINGFACE_EMBEDDING_MODEL: str = Field(default="sentence-transformers/all-mpnet-base-v2", description="HuggingFace Embedding model name")


    GEMINI_MODEL: str = Field(default="gemini-2.5-flash", description="GEMINI model name")
    GROQ_MODEL: str = Field(default="llama-3.3-70b-versatile", description="GROQ model name")


    REDIS_URL: str = Field(default="redis://localhost:6379/0", description="Redis URL")


    MAX_FILE_SIZE: int = Field(default=10 * 1024 * 1024, description="Max file size in bytes")


    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )



@lru_cache
def get_settings() -> Settings:
    return Settings()





