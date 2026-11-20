from typing import TypedDict
from langchain_core.documents import Document


class PlantAgentState(TypedDict):
    plant_id: str # 식물 고유 번호
    plant_name: str # 식물 이름
    plant_state: str # 식물 상태
    plant_context: str # CSV 식물 정보, 관리 기록, 대화 문맥
    documents: list[Document] # Chroma RAG 검색 노드가 찾은 식물 관련 문서 목록
    num_generations: int # 검색 및 답변 생성 횟수, 무한반복 방지
    question: str # 사용자 질문
    generation: str # LLM 답변