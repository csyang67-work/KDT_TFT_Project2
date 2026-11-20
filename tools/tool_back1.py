

from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_core.documents import Document

# 1차 검색 후 rerabker로 결과를 재정렬 하는 검색기
from langchain_classic.retrievers import ContextualCompressionRetriever

# Cross-Encoder모델 쿼리-문서 싸의 관련도를 재채점하여 상위 N개만 넘기는 압축기
from langchain_classic.retrievers.document_compressors import CrossEncoderReranker
# 위 라이브러리는 ContextualCompressionRetriever 얘랑 같이 써야함

# HugginFace의 Cross-Encoder모델을 로드하고 실행하는 클래스
from langchain_community.cross_encoders import HuggingFaceCrossEncoder

from langchain_core.tools import tool # 도구
from typing import List

# Tavily웹 검색! - 검색 결과를 Retriever방식으로 가져와 RAG에 활용( 반환값: list(Document))
from langchain_community.retrievers import TavilySearchAPIRetriever

'''
구분            TavilySearchAPIRetriever            TavilySearch
---------------------------------------------------------------------------
역할            검색기반 문서 검색기                    검색도구(tool)
반환            list(Document)                       검색결과 딕셔너리
목적            RAG                                  AI Agent
주체            Retriever/Chain                      LLM / Agent
활용            문서분할, 임베딩, 답변생성               결과를 관찰하고 응답
결정            개발자가 전달                           Agent가 결정 가능
'''

# 필요한 임베딩 모델 - pdfData_load에 있는 embeddings_model을 임포트 해도 됨
embeddings_model = OllamaEmbeddings(model="bge-m3")

# 재정렬 인코더 모델
rerank_model = HuggingFaceCrossEncoder(model_name="BAAI/bge-reranker-v2-m3")

# 재정렬기 생성
cross_reranker = CrossEncoderReranker(model=rerank_model, top_n=2)

# 개인정보 보호법 검색 도구
personal_db = Chroma(
    embedding_function=embeddings_model,
    collection_name="personal_law", # 컬렉션(테이블) 명 지정
    persist_directory="./chroma_db"
)
personal_db_retriever = ContextualCompressionRetriever(
    base_compressor=cross_reranker, # 1차 검색 결과를 재정렬, 압축할 reranker객체 지정
    base_retriever=personal_db.as_retriever(search_kwargs={"k":5})
)

# 도구 설정
@tool
def personal_law_search(query: str) -> List[Document]:
    """개인정보보호법 법률 조항을 검색합니다."""
    docs = personal_db_retriever.invoke(query) # 쿼리가 1 검색 후 rerank하여 상위문서 반환
    if len(docs) > 0:
        return docs
    
    # 검색 결과가 없는 경우 안내메시지가 담긴 Document를 반환하자
    return[Document(page_content="관련정보를 찾을 수 없습니다.")]

# 근로기준법 법률 조항을 검색하는 객체들 만들자
labor_db = Chroma(
    embedding_function=embeddings_model,
    collection_name="labor_law", # 컬렉션(테이블) 명 지정
    persist_directory="./chroma_db"
)
labor_db_retriever = ContextualCompressionRetriever(
    base_compressor=cross_reranker, # 1차 검색 결과를 재정렬, 압축할 reranker객체 지정
    base_retriever=labor_db.as_retriever(search_kwargs={"k":5})
)

# 도구 설정
@tool
def labor_law_search(query: str) -> List[Document]:
    """근로기준법 법률 조항을 검색합니다."""
    docs = labor_db_retriever.invoke(query) # 쿼리가 1 검색 후 rerank하여 상위문서 반환
    if len(docs) > 0:
        return docs
    
    # 검색 결과가 없는 경우 안내메시지가 담긴 Document를 반환하자
    return[Document(page_content="관련정보를 찾을 수 없습니다.")]

# 주택임대차 법률 조항을 검색하는 객체들 만들자
housing_lease_db = Chroma(
    embedding_function=embeddings_model,
    collection_name="housing_lease_law", # 컬렉션(테이블) 명 지정
    persist_directory="./chroma_db"
)
housing_lease_db_retriever = ContextualCompressionRetriever(
    base_compressor=cross_reranker, # 1차 검색 결과를 재정렬, 압축할 reranker객체 지정
    base_retriever=housing_lease_db.as_retriever(search_kwargs={"k":5})
)

# 도구 설정
@tool
def housing_lease_law_search(query: str) -> List[Document]:
    """주택임대차보호법 법률 조항을 검색합니다."""
    docs = housing_lease_db_retriever.invoke(query) # 쿼리가 1 검색 후 rerank하여 상위문서 반환
    if len(docs) > 0:
        return docs
    
    # 검색 결과가 없는 경우 안내메시지가 담긴 Document를 반환하자
    return[Document(page_content="관련정보를 찾을 수 없습니다.")]

# 웹 검색 도구
web_retriever = ContextualCompressionRetriever(
    base_compressor=cross_reranker,
    base_retriever=TavilySearchAPIRetriever(k=5) # Tavily API로 웹 에서 관련페이지 5개 검색
)

@tool
def web_search(query:str) -> List[Document]:
    """"데이터베이스에 없는 정보 또는 최신정보를 웹에서 검색합니다."""
    docs = web_retriever.invoke(query) # Tavily 웹 검색 후 rerank하여 상위 문서만 반환됨
    formatted_docs = []
    for doc in docs:
        formatted_docs.append(
            Document(
                page_content=doc.page_content,
                metadata={
                    "source":"web search",
                    "url":doc.metadata["source"]
                }
            )
        )
    if len(formatted_docs) > 0:
        return formatted_docs
    
    return[Document(page_content="관련정보를 찾을 수 없습니다.")]