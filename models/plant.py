from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Float, Integer, String

from database import Base


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class Plant(Base):
    """사용자가 키우는 가상 식물의 현재 상태."""

    __tablename__ = "plants"

    plant_id = Column(String, primary_key=True, index=True)
    user_id = Column(String, index=True, nullable=False)
    plant_name = Column(String, nullable=False)

    growth_stage = Column(String, default="새싹")
    health = Column(Integer, default=100)
    water_level = Column(Integer, default=50)

    temperature = Column(Float, default=22.0)
    humidity = Column(Float, default=50.0)
    light_level = Column(Float, default=50.0)

    started_at = Column(DateTime(timezone=True), nullable=False)
    game_time = Column(DateTime(timezone=True), nullable=False)
    recorded_at = Column(
        DateTime(timezone=True),
        default=utc_now,
        nullable=False,
    )