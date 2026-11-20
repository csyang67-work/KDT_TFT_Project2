from datetime import datetime, timezone

from langchain_chroma import Chroma
from langchain_core.documents import Document

from config import CHROMA_PATH, USER_PLANT_COLLECTION_NAME
from llm.embeddings import embeddings_model


def add_plant_event(
    user_id: str,
    plant_id: str,
    event_id: str,
    event_type: str,
    content: str,
    game_time: str,
) -> None:
    """돌봄·환경 변경 기록을 Chroma에 저장합니다."""

    plant_records = Chroma(
        collection_name=USER_PLANT_COLLECTION_NAME,
        persist_directory=CHROMA_PATH,
        embedding_function=embeddings_model,
    )

    document = Document(
        page_content=content,
        metadata={
            "user_id": user_id,
            "plant_id": plant_id,
            "event_id": event_id,
            "event_type": event_type,
            "game_time": game_time,
            "recorded_at": datetime.now(timezone.utc).isoformat(),
        },
    )

    plant_records.add_documents(
        documents=[document],
        ids=[event_id],
    )


def search_plant_events(
    user_id: str,
    plant_id: str,
    query: str,
) -> list[Document]:
    """특정 사용자의 특정 식물 기록을 검색합니다."""

    plant_records = Chroma(
        collection_name=USER_PLANT_COLLECTION_NAME,
        persist_directory=CHROMA_PATH,
        embedding_function=embeddings_model,
    )

    return plant_records.similarity_search(
        query=query,
        k=5,
        filter={
            "user_id": user_id,
            "plant_id": plant_id,
        },
    )