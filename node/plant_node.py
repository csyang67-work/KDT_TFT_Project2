from langchain_core.messages import AIMessage, SystemMessage
from langgraph.graph import END, START, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition

from llm.llm import llm_with_tools
from state.plant_state import PlantAgentState
from tools.plant_tool import plant_tools


SYSTEM_PROMPT = """
너는 OMG 가상 정원의 식물 도우미다.

가상 식물의 현재 상태와 실제 식물 정보를 구분해서 답변한다.
현재 게임 상태를 바꾸거나 조회할 때는 알맞은 도구를 사용한다.
실제 식물 관리 정보가 필요하면 식물 도감 검색을 사용한다.
도감에 정보가 부족하거나 최신 정보가 필요하면 웹 검색을 사용한다.
물 주기, 환경 변경, 게임 시간 변경 후에는 도구 결과를 기준으로 설명한다.
"""


def call_model(state: PlantAgentState) -> dict:
    """질문과 식물 상태를 전달해 답변 또는 도구 호출을 받습니다."""
    system_message = SystemMessage(
        content=(
            f"{SYSTEM_PROMPT}\n\n"
            f"[가상 식물]\n"
            f"이름: {state['plant_name']}\n"
            f"성장 단계: {state['growth_stage']}\n"
            f"건강도: {state['health']}\n"
            f"수분: {state['water_level']}\n"
            f"게임 시간: {state['game_time']}\n"
            f"환경: {state['environment']}\n\n"
            f"[참고 문맥]\n{state['plant_context']}"
        )
    )

    response = llm_with_tools.invoke(
        [system_message] + state["messages"]
    )

    return {"messages": [response]}


def save_final_answer(state: PlantAgentState) -> dict[str, str]:
    """마지막 AI 응답을 generation 필드에 저장합니다."""
    last_message = state["messages"][-1]

    if isinstance(last_message, AIMessage):
        return {"generation": str(last_message.content)}

    return {"generation": ""}


builder = StateGraph(PlantAgentState)

builder.add_node("agent", call_model)
builder.add_node("tools", ToolNode(plant_tools))
builder.add_node("save_answer", save_final_answer)

builder.add_edge(START, "agent")

builder.add_conditional_edges(
    "agent",
    tools_condition,
    {
        "tools": "tools",
        END: "save_answer",
    },
)

builder.add_edge("tools", "agent")
builder.add_edge("save_answer", END)

plant_graph = builder.compile()