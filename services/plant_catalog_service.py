import csv

from langchain_chroma import Chroma
from langchain_core.documents import Document

from config import CHROMA_PATH, COLLECTION_NAME, PLANT_CATALOG_CSV, TOP_K
from llm.embeddings import embeddings_model


def create_plant_catalog() -> int:
    """CSV 한 행을 식물 Document 하나로 만들어 Chroma에 저장합니다."""
    documents = []
    document_ids = []

    with PLANT_CATALOG_CSV.open(
        "r",
        encoding="utf-8-sig",
        newline="",
    ) as csv_file:
        rows = csv.DictReader(csv_file)

        for row_number, row in enumerate(rows, start=1):
            plant_info = {
                key: value.strip()
                for key, value in row.items()
                if value and value.strip()
            }

            if not plant_info:
                continue

            scientific_name = plant_info.get("학명")
            plant_name = plant_info.get("국명", "")

            page_content = "\n".join(
                f"{key}: {value}"
                for key, value in plant_info.items()
            )

            documents.append(
                Document(
                    page_content=page_content,
                    metadata={
                        "source": PLANT_CATALOG_CSV.name,
                        "row_number": row_number,
                        "plant_name": plant_name,
                        "scientific_name": scientific_name or "",
                    },
                )
            )

            # 학명이 없는 행은 국명과 행 번호를 이용해 구분합니다.
            document_ids.append(
                f"catalog:{scientific_name or plant_name}:{row_number}"
            )

    if not documents:
        raise ValueError("CSV에서 색인할 식물 정보를 찾지 못했습니다.")

    Chroma.from_documents(
        documents=documents,
        embedding=embeddings_model,
        collection_name=COLLECTION_NAME,
        persist_directory=CHROMA_PATH,
        ids=document_ids,
    )

    return len(documents)


def search_plant_catalog_documents(query: str) -> list[Document]:
    """식물 도감에서 질문과 관련된 문서를 찾습니다."""
    plant_catalog = Chroma(
        collection_name=COLLECTION_NAME,
        persist_directory=CHROMA_PATH,
        embedding_function=embeddings_model,
    )

    return plant_catalog.similarity_search(query, k=TOP_K)


if __name__ == "__main__":
    count = create_plant_catalog()
    print(f"식물 도감 {count}개를 Chroma에 저장했습니다.")