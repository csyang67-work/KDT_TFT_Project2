from datetime import datetime, timezone
from langchain_chroma import Chroma
from langchain_core.documents import Document

from config import CHROMA_PATH, USER_PLANT_COLLECTION_NAME
from llm.embeddings import embeddings_model

# 상태 변경 기록을 검색용 문서로 Chroma에 추가함
def add_plant_event(
    user_id: str,
    plant_id: str,
    event_id: str,
    event_type: str,
    content: str,
) -> None:
    """돌봄·상태 변경 기록을 검색용 문서로 Chroma에 추가함"""

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
            "event_type": event_type,
            "recorded_at": datetime.now(timezone.utc).isoformat(),
        },
    )

    # 새 돌봄·관찰 기록은 고유 event_id로 추가함
    plant_records.add_documents(
        documents=[document],
        ids=[event_id],
    )