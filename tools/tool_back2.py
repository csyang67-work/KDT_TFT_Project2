"""
도구들
"""
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_core.tools import tool

from config import (
    CHROMA_PATH,
    COLLECTION_NAME,
    PLANT_CATALOG_CSV,
    TOP_K,
)
from llm.embeddings import embeddings_model
import csv

# 식물 카테고리를 저장하는 함수
def create_plant_catalog() -> int:
    """식물 도감 CSV의 각 행을 Chroma에 저장합니다."""

    documents = []

    # CSV를 읽어 식물 한 종마다 Document 하나를 만듬
    with PLANT_CATALOG_CSV.open(
        "r",
        encoding="utf-8",
        newline="",
    ) as csv_file:
        rows = csv.reader(csv_file)
        columns = next(rows, None)

        if not columns:
            raise ValueError("CSV 헤더를 읽을 수 없습니다.")

        for row in rows:
            # 각 값을 CSV 컬럼명과 연결해 검색할 문서 내용으로 만듭니다.
            plant_info = {
                column: value.strip()
                for column, value in zip(columns, row)
                if value.strip()
            }

            if not plant_info:
                continue

            page_content = "\n".join(
                f"{key}: {value}"
                for key, value in plant_info.items()
            )

            documents.append(
                Document(
                    page_content=page_content,
                    metadata={
                        "source": PLANT_CATALOG_CSV.name,
                        "plant_name": plant_info.get("국명", ""),
                        "scientific_name": plant_info.get("학명", ""),
                    },
                )
            )

    if not documents:
        raise ValueError("CSV에서 색인할 식물 정보를 찾지 못했습니다.")

    # CSV 문서를 임베딩해 Chroma에 저장합니다.
    Chroma.from_documents(
        documents=documents,
        embedding=embeddings_model,
        collection_name=COLLECTION_NAME,
        persist_directory=CHROMA_PATH,
    )

    return len(documents)


@tool
def search_plant_catalog(query: str) -> list[Document]:
    """식물 도감 CSV에서 식물 특징과 관리 정보를 검색합니다."""

    if not query.strip():
        return [Document(page_content="검색어를 입력해 주세요.")]

    # 저장된 Chroma 식물 도감에서 질문과 관련된 문서를 검색합니다.
    plant_catalog = Chroma(
        collection_name=COLLECTION_NAME,
        persist_directory=CHROMA_PATH,
        embedding_function=embeddings_model,
    )

    retriever = plant_catalog.as_retriever(
        search_kwargs={"k": TOP_K}
    )

    documents = retriever.invoke(query)

    if not documents:
        return [Document(page_content="관련 식물 정보를 찾지 못했습니다.")]

    return documents


# 이 파일을 직접 실행했을 때 CSV를 Chroma에 색인합니다.
if __name__ == "__main__":
    document_count = create_plant_catalog()
    print(f"식물 정보 {document_count}개를 Chroma에 저장했습니다.")