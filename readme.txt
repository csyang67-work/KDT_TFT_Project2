# 🌱 Oh My Garden

AI와 대화하며 식물을 키우는 Streamlit 웹앱입니다.

> **현재 상태:** 화면(UI)만 완성된 상태입니다.
> 데이터는 모두 **예시 데이터**이고, 기능이 필요한 곳에는 `# TODO` 주석이 달려 있습니다.
> 이 문서를 보고 `TODO` 자리에 기능을 채워 넣으면 됩니다.

---

## 목차

1. [실행 방법](#1-실행-방법)
2. [폴더 구조](#2-폴더-구조)
3. [화면 구성](#3-화면-구성)
4. [기능 넣을 곳 (TODO 목록)](#4-기능-넣을-곳-todo-목록)
5. [자주 하는 작업](#5-자주-하는-작업)
6. [꼭 지켜야 할 규칙](#6-꼭-지켜야-할-규칙)
7. [자주 나는 에러](#7-자주-나는-에러)

---

## 1. 실행 방법

```bash
pip install -r requirements.txt
streamlit run app.py
```

- **Streamlit 1.67 이상**이 필요합니다. 팝업 폭을 픽셀로 정하는 기능(`st.dialog(width=1000)`) 때문입니다.
  버전 확인: `streamlit version` / 업데이트: `pip install -U streamlit`
- `streamlit run app.py`는 꼭 **`app.py`가 있는 폴더에서** 실행하세요. 다른 곳에서 실행하면 `ModuleNotFoundError: No module named 'ui'`가 납니다.

---

## 2. 폴더 구조

```
KDT_TFT_Project2/
├── app.py              # 메인 화면 (헤더, 식물 영역, 상태창, 채팅, 사이드바)
├── assets/
│   └── logo.png        # 로고 이미지 (없으면 🌱 이모지로 대신 표시)
├── .streamlit/
│   └── config.toml     # 테마 색 (게이지, 입력창 강조색 등)
└── ui/
    ├── __init__.py
    ├── dialogs.py      # 사이드바 메뉴의 팝업창 전부
    └── styles.py       # CSS 전부 (CSS = """...""")
```

| 파일 | 고칠 때 |
|---|---|
| `app.py` | 메인 화면, 물주기 등 식물 관리 버튼, AI 채팅 |
| `ui/dialogs.py` | 새로 키우기 / 식물 조회 / 내 기록 / 통계 팝업 |
| `ui/styles.py` | 색, 크기, 모양 |
| `.streamlit/config.toml` | Streamlit 기본 위젯 색 (`primaryColor` 등) |

---

## 3. 화면 구성

```
┌────────────┬──────────────────────────────────────────────┐
│ 사이드바   │ 🌱 Oh My Garden                ← render_header() │
│            │ ┌─────────────┐  ┌────────────────────────┐ │
│ 🌱 새로 키우기 │ │  식물 영역   │  │  AI 채팅               │ │
│ 🔍 식물 조회  │ │ plant_box   │  │  ai_box                │ │
│ 📒 내 기록    │ └─────────────┘  │                        │ │
│ 📊 통계      │ [💧][2][3][4]    │  chat_area (스크롤)    │ │
│            │ ┌─────────────┐  │                        │ │
│            │ │ 상태창       │  │ [메시지 입력]           │ │
│            │ │ status_box  │  └────────────────────────┘ │
└────────────┴──────────────────────────────────────────────┘
```

### 팝업 흐름

```
🌱 새로 키우기 ─ 식물 카드 [🌱 키우기]

🔍 식물 조회 ─ 식물 카드 [자세히 보기 ›] ──▶ 식물 정보 ─ ‹ 돌아가기
📒 내 기록   ─ 기록 줄   [자세히 보기 ›] ──▶ 기록 자세히 ─ ‹ 돌아가기
📊 통계     ─ 숫자 카드 [자세히 보기 ›] ──▶ 키운 식물 / 돌본 기간 / 물 준 기록 ─ ‹ 돌아가기
```

| 팝업 함수 (`ui/dialogs.py`) | DIALOGS 이름 | 여는 곳 |
|---|---|---|
| `new_plant_dialog` | — | 사이드바 "새로 키우기" |
| `search_plant_dialog` | `search` | 사이드바 "식물 조회" |
| `plant_detail_dialog` | `plant_detail` | 식물 조회 → 자세히 보기 |
| `my_record_dialog` | `record` | 사이드바 "내 기록" |
| `record_detail_dialog` | `record_detail` | 내 기록 → 자세히 보기 |
| `my_statistics_dialog` | `stats` | 사이드바 "통계" |
| `stat_count_dialog` | `stat_count` | 통계 → 키운 식물 |
| `stat_days_dialog` | `stat_days` | 통계 → 총 돌본 기간 |
| `stat_water_dialog` | `stat_water` | 통계 → 물 준 횟수 |


### app.py

| 위치 | 할 일 |
|---|---|
| `render_chat_area()` → `# TODO: 여기서 실제 AI 응답을...` | AI 응답 연결 (지금은 고정 문장) |
| `render_plant_area()` → 버튼 `2`, `3`, `4` | 식물 관리 기능 연결 (💧 물주기만 동작) |
| `st.session_state.plant` 의 `"행복도"` | 상태창에 표시할지 결정 |

### ui/dialogs.py

| 팝업 | 할 일 |
|---|---|
| 공통 | `SAMPLE_PLANTS`, `SAMPLE_RECORDS` 를 실제 데이터로 교체 ([5-1](#5-1-예시-데이터를-실제-데이터로-바꾸기)) |
| 새로 키우기 | `🌱 키우기` 버튼 → 선택한 식물로 키우기 시작 |
| 새로 키우기, 식물 조회 | 필터(`render_filters`)로 카드 걸러내기 |
| 식물 조회 | 검색창(`search_query`)으로 이름 검색 |
| 식물 정보 | 물 주기·햇빛·온도·습도 값, 소개, 관리 팁, `이 식물 키우기` 버튼 |
| 내 기록 | 상태 필터(`record_status`: 전체 / 키우는 중 / 완료) |
| 기록 자세히 | 성장 기록, 메모 |
| 통계 | 그래프 4개(`chart_...` 함수)의 숫자를 실제 기록에서 계산 |