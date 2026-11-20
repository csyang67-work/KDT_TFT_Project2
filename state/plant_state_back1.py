from typing import TypedDict, List, Optional
from langchain_core.documents import Document
from langgraph.graph.message import add_messages


class PlantAgentState(TypedDict):
    """식물 상담 그래프의 입력과 노드 간 공유 데이터.
    ex1102의 state/law_state.py처럼 그래프가 읽고 쓸 필드를 한곳에 모읍니다.
    이 첫 단계에서는 검색 노드를 분리하기 전이므로, 기존 서비스가 준비한
    식물 정보·기억·관리 기록·대화 문맥을 plant_context로 전달합니다.
    """
    plant_id: int # 식물 고유 번호
    plant_name: str # 식물 이름
    plant_context: str # 식물 정보
    documents: List[Document] # 검색 결과 문서
    num_generations: int # 답변 생성 횟수(무한반복 방지에 활용)
    question: str # 사용자 질문
    generation: str # LLM 생성 답변

# 웹 검색에 대한 상태
class WebRagState(PlantAgentState):
    rewritten_query: str # 재작성된 질문
    extracted_info: Optional[ExtractedInformation] # 추출된 정보 조각들
    node_answer: Optional[str]

# 메인 그래프에 대한 상태
class ReasearchAgentState(TypedDict):
    question: str
    answers: Annotated[List[str], add_messages]
    datasources: List[str] # 도구명들이 저장되는 곳
    final_answer: str
    evalution_report: Optional[dict]
    user_desision: Optional[str]