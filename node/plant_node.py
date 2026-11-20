from langchain_core.messages import HumanMessage, SystemMessage

# LLM 모델 불러와야 함
from KDT_TFT_Project2.state.plant_state_back1 import 

SYSTEM_PROMPT = """
너는 Oh! My Garden이라는 식물 관리 도우미다.
사용자가 등록한 식물의 정보와 관리 기록, 제공된 참고 자료를 바탕으로 한국어로 답변한다.

원칙:
1. 식물 상태를 보지 않고 병해충이나 물 부족을 확정하지 않는다.
2. 물 주기는 날짜만으로 단정하지 말고 흙 상태, 화분, 계절, 환경을 함께 고려한다.
3. 참고 자료가 없으면 공식 자료를 확인한 것처럼 말하지 않는다.
4. 사용자가 말하지 않은 식물 특성을 사실처럼 만들어내지 않는다.
5. 기록된 정보와 추정 정보를 구분한다.
6. 답변은 초보자도 이해하기 쉽게 단계별로 설명한다.
"""

def generate_plant_answer(state: PlantAgentState) -> dict[str, str]:
    """식물별 컨텍스트와 질문으로 답변을 생성하는 노드."""
    system_prompt = (
        f"{SYSTEM_PROMPT}\n\n"
        f"[현재 식물]\n{state['plant_name']} (plant_id: {state['plant_id']})\n\n"
        "[이 식물의 저장 정보, 최근 대화, 관리 기록 및 참고 지식]\n"
        f"{state['plant_context']}"
    )
    response = get_chat_model().invoke([
        SystemMessage(content=system_prompt),
        HumanMessage(content=state["question"]),
    ])

    content = response.content
    if isinstance(content, list):
        content = "\n".join(
            item.get("text", str(item)) if isinstance(item, dict) else str(item)
            for item in content
        )
    return {"generation": str(content)}
