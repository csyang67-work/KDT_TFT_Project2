import os
from dotenv import load_dotenv

load_dotenv()

# 파일 및 DB 경로
CSV_PATH = "./data/plants_catalog_R1.csv"
STATE_FILE_PATH = "./data/plant_state.json"
CHROMA_PATH = "./chroma_db"
COLLECTION_NAME = "plant_db"

# LLM모델 및 RAG 검색 
LLM_MODEL = os.getenv(model_name=os.getenv("LLM_MODEL"))
EMBEDDING_MODEL = "bge-m3"
RERANK_MODEL = "BAAI/bge-reranker-v2-m3"

RETRIEVER_K = 5
RERANK_TOP_N = 2

# 게임 기본 설정(수분, 건강상태, 습도 등의 요소들의 최대, 최소값)
STAT_MIN = 0
STAT_MAX = 100

# 시간 경과에 따른 상태 변경 설정
DECAY_UNIT_SECONDS = 30 # 몇초 단위로 식물의 상태가 안좋아질건지
WATER_DECAY_PER_UNIT = 1.0 # 단위 시간당 수분 감소량
ENVIRONMENT_DECAY_PER_UNIT = 0.5 # 단위 시간당 환경요소 감소량
