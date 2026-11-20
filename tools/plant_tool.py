from langchain_core.tools import tool


@tool
def water_plant(plant_id: str, amount: int) -> str:
    """가상 식물에 물을 주고 게임 상태와 돌봄 기록을 갱신합니다."""
    # plant_game_service에 상태 갱신과 이벤트 기록을 맡깁니다.
    ...


@tool
def change_environment(
    plant_id: str,
    temperature: float,
    humidity: float,
    light_level: float,
) -> str:
    """가상 정원의 온도·습도·빛 조건을 변경합니다."""
    # 게임 상태를 갱신하고 환경 변경 기록을 남깁니다.
    ...


@tool
def search_plant_catalog(query: str) -> str:
    """CSV에서 색인한 Chroma 도감에서 실제 식물 정보를 찾습니다."""
    # 기존 tools/tool.py의 검색 기능을 사용합니다.
    ...