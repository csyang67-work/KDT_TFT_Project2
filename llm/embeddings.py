# 프로젝트에서 공통으로 사용하는 임베딩 모델 생성 함수.

from functools import lru_cache

from langchain_core.embeddings import Embeddings

from config import settings


@lru_cache(maxsize=1)
def get_embeddings() -> Embeddings:
    """설정된 임베딩 제공자로부터 임베딩 객체를 생성합니다.

    현재 프로젝트는 Ollama 임베딩을 사용하며 기본 모델은 bge-m3입니다.
    CSV 색인과 검색에서 이 함수를 함께 사용해 같은 모델을 유지합니다.
    """
    provider = settings.embedding_provider.strip().lower()

    if provider == "ollama":
        from langchain_ollama import OllamaEmbeddings

        return OllamaEmbeddings(
            model=settings.embedding_model,
            base_url=settings.embedding_base_url,
        )

    raise ValueError(
        f"지원하지 않는 EMBEDDING_PROVIDER: {provider}. 현재는 ollama만 지원합니다."
    )
