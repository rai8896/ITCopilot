# from functools import lru_cache
# from pathlib import Path
# from pydantic_settings import BaseSettings, SettingsConfigDict

# BASE_DIR = Path(__file__).resolve().parents[2]

# class Settings(BaseSettings):
#     app_name: str = "Enterprise IT Support Agentic RAG Copilot"
#     app_env: str = "development"
#     openai_api_key: str = ""
#     tavily_api_key: str = ""
#     pinecone_api_key: str = ""
#     pinecone_index_name: str = "fde-it-support-rag"
#     pinecone_namespace: str = "company-it-kb"
#     embedding_model: str = "text-embedding-3-small"
#     openai_model: str = "gpt-4o-mini"
#     top_k: int = 4
#     max_retries: int = 1
#     admin_api_key: str = "change-me"
#     audit_db_path: str = str(BASE_DIR / "data" / "audit.db")
#     upload_dir: str = str(BASE_DIR / "uploads")
#     sample_kb_dir: str = str(BASE_DIR / "data" / "sample_kb")

#     model_config = SettingsConfigDict(env_file=str(BASE_DIR / ".env"), extra="ignore")




# @lru_cache
# def get_settings() -> Settings:
#     return Settings()



from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    # Application
    app_name: str = "Enterprise IT Support Agentic RAG Copilot"
    app_env: str = "development"

    # LLM - Groq
    groq_api_key: str = ""
    groq_model: str = "llama-3.3-70b-versatile"

    # Optional OpenAI configuration
    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"

    # Web search
    tavily_api_key: str = ""

    # Pinecone vector database
    pinecone_api_key: str = ""
    pinecone_index_name: str = "fde-it-support-rag"
    pinecone_namespace: str = "company-it-kb"

    # Local Hugging Face embeddings
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"

    # RAG configuration
    top_k: int = 4
    max_retries: int = 1

    # Admin authentication
    admin_api_key: str = "change-me"

    # Application directories
    audit_db_path: str = str(BASE_DIR / "data" / "audit.db")
    upload_dir: str = str(BASE_DIR / "uploads")
    sample_kb_dir: str = str(BASE_DIR / "data" / "sample_kb")

    # Environment configuration
    model_config = SettingsConfigDict(
        env_file=str(BASE_DIR / ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
