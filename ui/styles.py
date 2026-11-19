CSS = """
<style>

/* 1. 색상 변수
   - 여기서 정한 색을 아래에서 var(--이름) 으로 가져다 씀 */
:root {
    --zoom: 1.1;               /* 화면 확대 비율 (아래 .stApp, 높이 계산에 사용) */

    /* 포인트 색 */
    --green: #03C75A;          /* 사용자 말풍선, 버튼 hover 테두리 */
    --dark-green: #008F45;     /* 배지 글자, 관리 버튼 글자 */
    --light-green: #EAF8EF;    /* 관리 버튼 hover 배경 */

    /* 배경 */
    --page-bg: #eff9f2;        /* 전체 화면 배경 */
    --card-bg: #F7FAF7;        /* 카드(식물, 상태창, 채팅), 사이드바, 버튼 배경 */
    --plant-top: #E3F1E7;      /* 식물 영역 위쪽 그라데이션 */
    --ai-bubble: #E8EFE9;      /* AI 말풍선 */
    --badge-bg: #DDF0E3;       /* 식물 이름 배지, AI 아이콘 배경 */

    /* 테두리 */
    --border: #22a643;         /* 상태창, 채팅 카드, 사이드바 테두리 */
    --plant-border: #C4DECB;   /* 식물 영역, 관리 버튼 테두리 */

    /* 글자 */
    --text: #26382D;           /* 기본 글자 (제목, 말풍선 등) */
    --sub-text: #5F7064;       /* 보조 글자 (게이지 이름, 설명) */
}


/* 2. 앱 전체 레이아웃 */

/* 앱 전체: 확대 비율 + 배경색 */
.stApp {
    zoom: var(--zoom);         /* 브라우저 110% 확대와 같은 효과 */
    background: var(--page-bg);
}

/* 본문 영역: 폭과 위아래 여백 */
.block-container {
    padding-left: 100px;
    max-width: 980px;
    padding-top: 2.5rem;
    padding-bottom: 2rem;
}

/* 맨 위 헤더 띠: 투명하게 (제목 잘림 방지) */
header[data-testid="stHeader"] {
    background: transparent;
}

/* 사이드바 → st.sidebar */
[data-testid="stSidebar"] {
    background: var(--card-bg);
    background-color: #e3f1e7;
    border-right: 1px solid var(--border);
}

/* 제목 글자색 → st.title, st.header 등 */
h1, h2, h3 {
    color: var(--text);
}


/* 3. 화면 높이에 맞춰 카드 크기 자동 조절
   - 브라우저 창 높이(100vh)에 따라 카드 높이가 늘어남
   - max(최소값, 계산값): 창이 작아도 최소값보다 작아지지 않음
   - 주의: 이 값이 파이썬의 height= 값보다 우선함 */

/* 오른쪽 AI 채팅 카드 → key="ai_box" */
div:has(> .st-key-ai_box) {
    flex-basis: max(517px, calc(100vh / var(--zoom) - 160px)) !important;
    height:     max(517px, calc(100vh / var(--zoom) - 160px)) !important;
}

/* 채팅 기록 스크롤 영역 → key="chat_area" */
div:has(> .st-key-chat_area) {
    flex-basis: max(282px, calc(100vh / var(--zoom) - 395px)) !important;
    height:     max(282px, calc(100vh / var(--zoom) - 395px)) !important;
}

/* 왼쪽 식물 영역 → key="plant_box" */
div:has(> .st-key-plant_box) {
    flex-basis: max(210px, calc(100vh / var(--zoom) - 467px)) !important;
    height:     max(210px, calc(100vh / var(--zoom) - 467px)) !important;
}


/* 4. 카드 공통 모양
   → key="status_box" (상태창), key="ai_box" (AI 채팅) */
.st-key-status_box,
.st-key-ai_box {
    border: 1px solid var(--border) !important;
    border-radius: 16px !important;
    background: var(--card-bg) !important;
}


/* 5. 식물 영역 → render_plant_area() 의 key="plant_box" */

/* 식물 카드 */
.st-key-plant_box {
    position: relative;
    border: 1px solid var(--border) !important;
    border-radius: 16px !important;
    background:
        linear-gradient(to top, #654323 5%, #9B7046 16%, transparent 25%),   /* 흙 */
        linear-gradient(to top, #ffffff) !important;  /* 배경 */
    background-origin: border-box !important;
    background-repeat: no-repeat !important;
}

/* 식물 카드 안의 요소들이 카드 기준으로 위치를 잡도록 */
.st-key-plant_box [data-testid="stElementContainer"] {
    position: static;
}

/* "● 식물 이름" 배지 → <div class="plant-badge"> */
.plant-badge {
    display: inline-block;
    background: var(--badge-bg);
    color: var(--dark-green);
    padding: 6px 13px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 600;
}

/* 식물 이모지 + 성장 단계 + 설명을 감싸는 가운데 정렬 영역
   → <div class="plant-center"> */
.plant-center {
    text-align: center;
    margin-top: 30px;
}

/* 식물 이모지 (🌱 등) → <div class="plant-emoji"> */
.plant-emoji {
    font-size: 72px;
    line-height: 1;
}

/* 성장 단계 글자 ("새싹" 등) → <div class="plant-stage"> */
.plant-stage {
    font-size: 15px;
    font-weight: 700;
    color: #315C40;
    margin-top: 10px;
}

/* 식물 상황 설명 → <div class="plant-desc"> */
.plant-desc {
    font-size: 12px;
    color: var(--sub-text);
    margin-top: 5px;
}


/* 6. 상태창 → render_plant_area() 의 key="status_box" */
/* "식물 상태" 제목 → <div class="status-title"> */
.status-title {
    font-weight: 700;
    color: var(--text);
    margin-bottom: 4px;
}

/* 게이지 이름 ("수분", "영양") → <div class="status-label"> */
.status-label {
    color: var(--sub-text);
    font-size: 13px;
    margin-bottom: 5px;
}


/* 7. 식물 관리 버튼 (💧, 2, 3, 4) → key="care_buttons"
   - 이 컨테이너 안의 버튼에만 적용됨 */

/* 기본 상태 */
.st-key-care_buttons button {
    background: var(--card-bg);
    color: var(--black);
    border: 1px solid var(--border);
    border-radius: 10px;
    font-weight: 600;
    transition: 0.2s;          /* hover 색이 부드럽게 바뀌도록 */
}

/* 마우스를 올렸을 때 */
.st-key-care_buttons button:hover {
    background: var(--light-green);
    border-color: var(--green);
    color: var(--dark-green);
}


/* 8. AI 채팅 → render_chat_area() */

/* 채팅 카드 맨 위 헤더 (아이콘 + "AI") → <div class="ai-header"> */
.ai-header {
    display: flex;
    align-items: center;
    gap: 10px;
}

/* 헤더의 🌱 아이콘 상자 → <div class="ai-header-icon"> */
.ai-header-icon {
    width: 40px;
    height: 40px;
    background: var(--badge-bg);
    border-radius: 12px;
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: 25px;
}

/* 헤더의 "AI" 글자 → <div class="ai-header-title"> */
.ai-header-title {
    font-size: 20px;
    font-weight: 700;
    color: var(--text);
}


/* 9. 채팅 말풍선 → chat_bubble() 함수가 만드는 HTML */

/* 말풍선 한 줄 (아이콘 + 말풍선을 가로로 배치) */
.chat-row {
    display: flex;
    align-items: flex-start;
    gap: 8px;
    margin: 6px 0;
}

/* 사용자 메시지 줄: 순서를 뒤집어 오른쪽 정렬 */
.chat-user {
    flex-direction: row-reverse;
}

/* 말풍선 옆 아이콘*/
.chat-icon {
    width: 32px;
    height: 32px;
    flex-shrink: 0;            /* 말풍선이 길어져도 아이콘이 찌그러지지 않게 */
    border-radius: 10px;
    background: var(--badge-bg);
    display: flex;
    justify-content: center;
    align-items: center;
}

/* 말풍선 공통 모양 */
.chat-bubble {
    max-width: 75%;
    padding: 9px 13px;
    border-radius: 14px;
    font-size: 14px;
    line-height: 1.5;
    color: var(--text);
    word-break: break-word;    /* 긴 단어·URL이 말풍선 밖으로 넘치지 않게 */
}

/* AI 말풍선: 왼쪽, 연한 회녹색 */
.chat-ai .chat-bubble {
    background: var(--ai-bubble);
    border-top-left-radius: 4px;    /* 꼬리처럼 보이도록 한쪽 모서리만 덜 둥글게 */
}

/* 사용자 말풍선: 오른쪽, 초록색 */
.chat-user .chat-bubble {
    background: var(--green);
    color: #FFFFFF;
    border-top-right-radius: 4px;
}

/* 10. 사이드바 메뉴 버튼 → app.py 의 key="sidebar_menu" */
.st-key-sidebar_menu button {
    background: var(--card-bg);
    color: var(--text);
    border: 1px solid var(--plant-border);
    border-radius: 12px;
    width: 200px
    justify-content: flex-start;    /* 글자를 왼쪽 정렬 */
    padding-left: 14px;
    transition: 0.2s;
}
.st-key-sidebar_menu button:hover {
    background: var(--light-green);
    border-color: var(--green);
    color: var(--dark-green);
}


/* 11. 팝업창 공통 → ui/dialogs.py 의 @st.dialog 들 */

/* 팝업창 배경, 모서리 */
div[role="dialog"] {
    background: var(--card-bg);
    border-radius: 20px;
}

/* "식물 4개" 개수 표시 */
.picker-count {
    font-size: 13px;
    color: var(--sub-text);
    margin-bottom: 8px;
}


/* 12. 식물 카드 → 새로 키우기, 식물 조회 팝업
   key="plant_card_new_0", "plant_card_search_0", ...
   [class*="..."] : 클래스 이름에 이 글자가 들어간 요소를 모두 고름 */
[class*="st-key-plant_card_"] {
    background: #FFFFFF;
    border: 1px solid var(--plant-border) !important;
    border-radius: 14px !important;
    transition: 0.2s;
}
[class*="st-key-plant_card_"]:hover {
    border-color: var(--green) !important;
}

/* 카드 윗줄 (이모지 + 이름) */
.plant-card-head {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 8px;
}
.plant-card-emoji {
    font-size: 28px;
}
.plant-card-name {
    font-size: 16px;
    font-weight: 700;
    color: var(--text);
}

/* 태그 (관엽식물, 반그늘 ...) */
.plant-card-tags {
    display: flex;
    flex-wrap: wrap;
    gap: 4px;
    margin-bottom: 4px;
}
.plant-tag {
    background: var(--badge-bg);
    color: var(--dark-green);
    font-size: 11px;
    padding: 2px 8px;
    border-radius: 10px;
}


/* 13. 내 기록 팝업 → key="record_row_0", "record_row_1", ... */

/* 기록 한 줄 */
[class*="st-key-record_row_"] {
    background: #FFFFFF;
    border: 1px solid var(--plant-border) !important;
    border-radius: 14px !important;
}

/* 이모지 + (이름 / 기간) */
.record-head {
    display: flex;
    align-items: center;
    gap: 12px;
}
.record-emoji {
    font-size: 30px;
}
.record-name {
    font-size: 15px;
    font-weight: 700;
    color: var(--text);
}
.record-sub {
    font-size: 12px;
    color: var(--sub-text);
    margin-top: 2px;
}

/* 상태 배지: 키우는 중(초록) / 완료(회색) */
.record-badge {
    display: inline-block;
    font-size: 12px;
    font-weight: 600;
    padding: 4px 10px;
    border-radius: 12px;
}
.record-badge.ongoing {
    background: var(--badge-bg);
    color: var(--dark-green);
}
.record-badge.done {
    background: #ECEFED;
    color: var(--sub-text);
}


/* 14. 통계 팝업 */

/* 그래프 제목 */
.stat-title {
    font-size: 14px;
    font-weight: 700;
    color: var(--text);
    margin-bottom: 4px;
}

/* 숫자 카드 (st.metric) */
div[role="dialog"] [data-testid="stMetric"] {
    background: #FFFFFF;
    border-radius: 14px;
}

</style>
"""