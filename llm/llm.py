from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic

from config import CLAUDE_MODEL, PROJECT_ROOT, QWEN_MODEL, OLLAMA_BASE_URL

# 프로젝트 루트의 .env에서 ANTHROPIC_API_KEY를 읽습니다.
load_dotenv(PROJECT_ROOT / ".env")

# 기본 설정: Claude API
llm = ChatAnthropic(model=CLAUDE_MODEL)

# Ollama의 Qwen3를 사용하려면 위 Claude 설정을 주석 처리하고,
# 아래 두 줄의 주석을 해제하세요. Ollama가 실행 중이어야 합니다.
# from langchain_ollama import ChatOllama
# llm = ChatOllama(model=QWEN_MODEL, base_url=OLLAMA_BASE_URL)
