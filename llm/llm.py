"""
Qwen3를 기본 채팅 모델로 사용합니다.
Claude API를 사용하려면 아래 Claude 설정을 활성화하고
Qwen 설정을 주석 처리하세요.
"""

from langchain_ollama import ChatOllama
from config import OLLAMA_BASE_URL, QWEN_MODEL

# 기본 모델: Ollama에서 실행하는 Qwen3
llm = ChatOllama(
    model=QWEN_MODEL,
    base_url=OLLAMA_BASE_URL,
)

# Claude API로 바꿀 때 사용할 설정
# config.py의 CLAUDE_MODEL은 .env의 LLM_MODEL_C 값을 사용합니다.
# from langchain_anthropic import ChatAnthropic
# from config import CLAUDE_MODEL

# llm = ChatAnthropic(model_name=CLAUDE_MODEL)

# 도구들 모음
tools = []

llm_with_tools = llm.bind_tools(tools)