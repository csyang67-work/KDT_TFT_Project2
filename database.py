from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from config import DATABASE_PATH, DATABASE_URL


# SQLite DB가 저장될 data 폴더가 없으면 만듭니다.
DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(
    autoflush=False,
    autocommit=False,
    bind=engine,
)

Base = declarative_base()


def create_tables() -> None:
    """Plant 모델을 등록한 뒤 DB 테이블을 만듭니다."""
    from models.plant import Plant

    Base.metadata.create_all(bind=engine)