"""
식물 상담과 게임 흐름에서 노드들이 공유하는 데이터
"""
from typing import TypedDict, Annotated
from langchain_core.documents import Document
from langgraph.graph.message import add_messages

class PlantAgentState(TypedDict):
    user_id: str                    # 사용자 구분 ID
    plant_id: str                   # 사용자가 키우는 개별 식물 ID
    plant_name: str                 # 식물 이름

    growth_stage: str               # 씨앗, 새싹, 성장기 등
    health: int                     # 게임상 건강도
    water_level: int                # 게임상 수분 상태
    environment: dict[str, float]   # 게임상 환경 상태(온도, 습도, 빛 등)

    game_time: str                  # 게임에서 표시/편집하는 시간
    days_growing: int               # 게임 시간 기준 키운 날짜 수
    plant_state: str                # 식물 상태

    plant_context: str              # CSV 식물 정보, 관리 기록, 대화 문맥
    documents: list[Document]       # Chroma RAG 검색 노드가 찾은 식물 관련 문서 목록
    question: str                   # 사용자 질문
    generation: str                 # LLM 답변

    messages: Annotated[list, add_messages]