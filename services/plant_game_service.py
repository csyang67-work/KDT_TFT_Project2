from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy.orm import Session

from database import SessionLocal
from models.plant import Plant
from services.plant_event_service import add_plant_event


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def plant_to_dict(plant: Plant) -> dict:
    """Plant 객체를 그래프와 API에서 사용할 딕셔너리로 바꿉니다."""
    started_at = plant.started_at
    game_time = plant.game_time

    # SQLite에서 timezone 정보가 빠진 datetime을 반환하는 경우를 맞춥니다.
    if started_at.tzinfo is None:
        started_at = started_at.replace(tzinfo=timezone.utc)
    if game_time.tzinfo is None:
        game_time = game_time.replace(tzinfo=timezone.utc)

    days_growing = max(0, (game_time - started_at).days)

    return {
        "plant_id": plant.plant_id,
        "user_id": plant.user_id,
        "plant_name": plant.plant_name,
        "growth_stage": plant.growth_stage,
        "health": plant.health,
        "water_level": plant.water_level,
        "environment": {
            "temperature": plant.temperature,
            "humidity": plant.humidity,
            "light_level": plant.light_level,
        },
        "started_at": started_at.isoformat(),
        "game_time": game_time.isoformat(),
        "days_growing": days_growing,
        "recorded_at": plant.recorded_at.isoformat(),
    }


def find_user_plant(
    session: Session,
    user_id: str,
    plant_id: str,
) -> Plant:
    """사용자와 식물 ID가 모두 일치하는 식물을 찾습니다."""
    plant = (
        session.query(Plant)
        .filter(
            Plant.user_id == user_id,
            Plant.plant_id == plant_id,
        )
        .first()
    )

    if plant is None:
        raise ValueError("해당 사용자에게 등록된 식물이 없습니다.")

    return plant


def register_plant(user_id: str, plant_name: str) -> dict:
    """사용자에게 새 가상 식물을 등록합니다."""
    now = utc_now()

    plant = Plant(
        plant_id=str(uuid4()),
        user_id=user_id,
        plant_name=plant_name,
        growth_stage="새싹",
        health=100,
        water_level=50,
        temperature=22.0,
        humidity=50.0,
        light_level=50.0,
        started_at=now,
        game_time=now,
        recorded_at=now,
    )

    with SessionLocal() as session:
        session.add(plant)
        session.commit()
        session.refresh(plant)
        return plant_to_dict(plant)


def get_plant_status(user_id: str, plant_id: str) -> dict:
    """식물의 현재 게임 상태를 조회합니다."""
    with SessionLocal() as session:
        plant = find_user_plant(session, user_id, plant_id)
        return plant_to_dict(plant)


def water_plant_for_user(
    user_id: str,
    plant_id: str,
    amount: int,
) -> dict:
    """물 주기 수치와 돌봄 기록을 갱신합니다."""
    if amount < 1 or amount > 100:
        raise ValueError("물 주기 양은 1부터 100까지 입력해 주세요.")

    with SessionLocal() as session:
        plant = find_user_plant(session, user_id, plant_id)
        plant.water_level = min(100, plant.water_level + amount)
        plant.recorded_at = utc_now()

        session.commit()
        session.refresh(plant)
        result = plant_to_dict(plant)

    add_plant_event(
        user_id=user_id,
        plant_id=plant_id,
        event_id=str(uuid4()),
        event_type="watering",
        content=(
            f"{result['plant_name']}에 물을 주었습니다. "
            f"현재 게임 수분 상태는 {result['water_level']}입니다."
        ),
        game_time=result["game_time"],
    )

    return result


def change_plant_environment(
    user_id: str,
    plant_id: str,
    temperature: float,
    humidity: float,
    light_level: float,
) -> dict:
    """가상 식물의 환경값을 변경하고 기록합니다."""
    if not -20 <= temperature <= 60:
        raise ValueError("온도는 -20도부터 60도 사이여야 합니다.")
    if not 0 <= humidity <= 100:
        raise ValueError("습도는 0부터 100 사이여야 합니다.")
    if not 0 <= light_level <= 100:
        raise ValueError("빛 수치는 0부터 100 사이여야 합니다.")

    with SessionLocal() as session:
        plant = find_user_plant(session, user_id, plant_id)
        plant.temperature = temperature
        plant.humidity = humidity
        plant.light_level = light_level
        plant.recorded_at = utc_now()

        session.commit()
        session.refresh(plant)
        result = plant_to_dict(plant)

    add_plant_event(
        user_id=user_id,
        plant_id=plant_id,
        event_id=str(uuid4()),
        event_type="environment_change",
        content=(
            f"{result['plant_name']} 환경을 변경했습니다. "
            f"온도 {temperature}, 습도 {humidity}, 빛 {light_level}."
        ),
        game_time=result["game_time"],
    )

    return result


def set_game_time(
    user_id: str,
    plant_id: str,
    new_game_time: datetime,
) -> dict:
    """게임 시간만 바꾸고 실제 기록 시각은 별도로 보존합니다."""
    with SessionLocal() as session:
        plant = find_user_plant(session, user_id, plant_id)
        plant.game_time = new_game_time
        plant.recorded_at = utc_now()

        session.commit()
        session.refresh(plant)
        result = plant_to_dict(plant)

    add_plant_event(
        user_id=user_id,
        plant_id=plant_id,
        event_id=str(uuid4()),
        event_type="game_time_change",
        content=f"게임 시간을 {result['game_time']}으로 변경했습니다.",
        game_time=result["game_time"],
    )

    return result