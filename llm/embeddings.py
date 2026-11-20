"""
임베딩 모델을 생성하는 클래스입니다.
"""
from langchain_ollama import OllamaEmbeddings

from config import EMBEDDING_MODEL, OLLAMA_BASE_URL


# CSV 색인과 검색에서 공통으로 사용할 임베딩 모델
embeddings_model = OllamaEmbeddings(
    model=EMBEDDING_MODEL,
    base_url=OLLAMA_BASE_URL,
)