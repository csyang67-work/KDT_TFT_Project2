"""
프로젝트 전체에서 사용하는 설정값을 관리합니다. ex1008 config.py 형식을 참고함
"""
from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

# CSV 파일 경로
PLANT_CATALOG_CSV = Path(__file__).resolve().parent / "data" / "plants_catalog_R1.csv"

# ChromaDB 저장 폴더와 컬렉션 이름
CHROMA_PATH = str(Path(__file__).resolve().parent / "vector_db" / "chroma")
COLLECTION_NAME = "plant_catalog"

# 임베딩 모델: 학원 ex1019/ex1102 방식처럼 OllamaEmbeddings로 직접 생성
EMBEDDING_MODEL = "bge-m3"
OLLAMA_BASE_URL = "http://localhost:11434"

# Chroma 유사도 검색 결과 개수
TOP_K = 5

# 현재 사용할 Claude 모델 (학원 ex1008 config.py 예시 기준)
CLAUDE_MODEL = os.getenv("LLM_MODEL_C")

# 로컬 Qwen3로 전환할 때 사용할 모델
QWEN_MODEL = os.getenv("LLM_MODEL_Q")

# CSV에서 만든 실제 식물 도감 자료
COLLECTION_NAME = "plant_catalog"

# 사용자가 키우는 식물의 관찰·돌봄 기록을 검색하기 위한 컬렉션
USER_PLANT_COLLECTION_NAME = "user_plant_records"