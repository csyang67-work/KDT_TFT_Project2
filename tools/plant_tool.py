from datetime import datetime

from langchain_community.retrievers import TavilySearchAPIRetriever
from langchain_core.documents import Document
from langchain_core.tools import tool

from services.plant_catalog_service import search_plant_catalog_documents
from services.plant_event_service import search_plant_events
from services.plant_game_service import (
    change_plant_environment,
    get_plant_status,
    set_game_time,
    water_plant_for_user,
)

@tool
def get_plant_status_tool(user_id: str, plant_id: str) -> str:
    """사용자가 키우는 가상 식물의 현재 상태를 조회합니다."""
    return str(get_plant_status(user_id, plant_id))


@tool
def water_plant_tool(
    user_id: str,
    plant_id: str,
    amount: int,
) -> str:
    """가상 식물에 물을 주고 게임 상태를 갱신합니다."""
    status = water_plant_for_user(user_id, plant_id, amount)
    return (
        f"물 주기 완료. 현재 수분 상태는 "
        f"{status['water_level']}입니다."
    )


@tool
def change_environment_tool(
    user_id: str,
    plant_id: str,
    temperature: float,
    humidity: float,
    light_level: float,
) -> str:
    """가상 정원의 온도·습도·빛 환경을 변경합니다."""
    status = change_plant_environment(
        user_id,
        plant_id,
        temperature,
        humidity,
        light_level,
    )
    return f"환경 변경 완료: {status['environment']}"


@tool
def set_game_time_tool(
    user_id: str,
    plant_id: str,
    new_game_time: str,
) -> str:
    """가상 식물의 게임 시간을 ISO 형식으로 변경합니다."""
    game_time = datetime.fromisoformat(new_game_time)
    status = set_game_time(user_id, plant_id, game_time)
    return f"게임 시간 변경 완료. 키운 지 {status['days_growing']}일입니다."


@tool
def search_plant_catalog(query: str) -> list[Document]:
    """CSV를 색인한 식물 도감에서 실제 식물 정보를 검색합니다."""
    documents = search_plant_catalog_documents(query)

    if documents:
        return documents

    return [Document(page_content="식물 도감에서 관련 정보를 찾지 못했습니다.")]


@tool
def search_user_plant_records(
    user_id: str,
    plant_id: str,
    query: str,
) -> list[Document]:
    """특정 사용자의 특정 식물에 대한 과거 돌봄·환경 기록을 검색합니다."""
    documents = search_plant_events(user_id, plant_id, query)

    if documents:
        return documents

    return [Document(page_content="이 식물의 관련 기록을 찾지 못했습니다.")]


@tool
def search_web_tavily(query: str) -> list[Document]:
    """도감에 정보가 없거나 최신 식물 정보가 필요할 때 웹을 검색합니다."""
    if not query.strip():
        return [Document(page_content="검색어를 입력해 주세요.")]

    retriever = TavilySearchAPIRetriever(k=5)
    documents = retriever.invoke(query)

    if documents:
        return documents

    return [Document(page_content="관련 웹 검색 결과를 찾지 못했습니다.")]


plant_tools = [
    get_plant_status_tool,
    water_plant_tool,
    change_environment_tool,
    set_game_time_tool,
    search_plant_catalog,
    search_user_plant_records,
    search_web_tavily,
]