import csv

from langchain_chroma import Chroma
from langchain_core.documents import Document

from config import CHROMA_PATH, COLLECTION_NAME, PLANT_CATALOG_CSV
from llm.embeddings import get_embeddings


# 프로젝트 data 폴더의 식물 도감 CSV 원본
CSV_PATH = PLANT_CATALOG_CSV


def load_plant_documents() -> list[Document]:
    """CSV의 각 행을 식물 한 종에 해당하는 Document로 변환합니다."""
    if not CSV_PATH.is_file():
        raise FileNotFoundError(f"식물 CSV 파일을 찾을 수 없습니다: {CSV_PATH}")

    documents = []
    with CSV_PATH.open("r", encoding="utf-8-sig", newline="") as csv_file:
        reader = csv.DictReader(csv_file)

        for row_number, row in enumerate(reader, start=1):
            content = "\n".join(
                f"{column}: {value.strip()}"
                for column, value in row.items()
                if value and value.strip()
            )
            if not content:
                continue

            documents.append(
                Document(
                    page_content=content,
                    metadata={
                        "source": CSV_PATH.name,
                        "row_number": row_number,
                        "plant_name": row.get("국명", "").strip(),
                        "scientific_name": row.get("학명", "").strip(),
                    },
                )
            )

    if not documents:
        raise ValueError("CSV에 색인할 식물 정보가 없습니다.")
    return documents


def rebuild_plant_catalog() -> int:
    """기존 식물 도감 컬렉션을 지우고 CSV 내용으로 다시 색인합니다."""
    embeddings = get_embeddings()

    # 이 컬렉션은 식물 도감 전용입니다. 실행하면 기존 도감 색인이 삭제됩니다.
    vectorstore = Chroma(
        collection_name=COLLECTION_NAME,
        persist_directory=CHROMA_PATH,
        embedding_function=embeddings,
    )
    vectorstore.delete_collection()

    documents = load_plant_documents()
    document_ids = [
        f"plant-catalog-row-{document.metadata['row_number']}"
        for document in documents
    ]

    Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        collection_name=COLLECTION_NAME,
        persist_directory=CHROMA_PATH,
        ids=document_ids,
    )
    return len(documents)


if __name__ == "__main__":
    count = rebuild_plant_catalog()
    print(f"식물 도감 갱신 완료: {count}개 문서")
