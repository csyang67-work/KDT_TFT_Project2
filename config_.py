# OMG 프로젝트의 임베딩 및 Chroma 설정
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Ollama에서 사용할 임베딩 모델. 채팅용 Qwen 모델과 별도로 설정합니다.
    embedding_provider: str = "ollama"
    embedding_model: str = "bge-m3"
    embedding_base_url: str = "http://localhost:11434"

    # Chroma 저장 위치와 식물 도감 컬렉션 이름
    chroma_persist_directory: str = str(PROJECT_ROOT / "vector_db" / "chroma")
    chroma_collection: str = "plant_catalog"
    retrieval_top_k: int = 4

    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
