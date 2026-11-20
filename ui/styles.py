# 앱 전체 CSS — app.py 에서 st.markdown(CSS, unsafe_allow_html=True) 로 적용
# .st-key-XXX  → 파이썬에서 key="XXX" 를 준 요소
# [class*="st-key-XXX_"] → key 가 "XXX_" 로 시작하는 요소 전부
CSS = """
<style>

/* 1. 색상 변수 — 여기서 정한 색을 아래에서 var(--이름) 으로 가져다 씀 */
:root {
    --zoom: 1.1;               /* 화면 확대 비율 (.stApp, 높이 계산에 사용) */
    --header-h: 56px;          /* 로고 헤더 높이 + 아래 여백 (카드 높이 계산에 사용) */

    /* 포인트 색 */
    --green: #03C75A;          /* 사용자 말풍선, hover 테두리 */
    --dark-green: #008F45;     /* 배지 글자, 버튼 글자 */
    --light-green: #EAF8EF;    /* 버튼 hover 배경 */

    /* 배경 */
    --page-bg: #eff9f2;        /* 전체 화면 배경 */
    --sidebar-bg: #e3f1e7;     /* 사이드바 배경 */
    --card-bg: #F7FAF7;        /* 카드(상태창, 채팅), 버튼, 팝업 배경 */
    --white-card: #FFFFFF;     /* 팝업 안의 흰 카드 */
    --ai-bubble: #E8EFE9;      /* AI 말풍선 */
    --badge-bg: #DDF0E3;       /* 배지, 아이콘 배경 */
    --done-bg: #ECEFED;        /* "완료" 배지 배경 */

    /* 테두리 */
    --border: #22a643;         /* 식물 영역, 상태창, 채팅 카드, 사이드바, 관리 버튼 */
    --plant-border: #C4DECB;   /* 팝업 안 카드, 사이드바 메뉴 버튼 */

    /* 글자 */
    --text: #26382D;           /* 기본 글자 */
    --sub-text: #5F7064;       /* 보조 글자 (설명, 날짜 등) */
}


/* 2. 앱 전체 레이아웃 */

/* 앱 전체: 확대 비율 + 배경색 */
.stApp {
    zoom: var(--zoom);
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

/* 사이드바 */
[data-testid="stSidebar"] {
    background: var(--sidebar-bg);
    border-right: 1px solid var(--border);
}

/* 제목 글자색 → st.title, st.header 등 */
h1, h2, h3 {
    color: var(--text);
}


/* 2-1. 로고 헤더 → app.py 의 render_header() */
.app-header {
    display: flex;
    align-items: center;
    gap: 10px;
    height: 44px;
    margin-bottom: 12px;               /* height + margin-bottom = --header-h */
}
.app-logo-img {                        /* assets/logo.png 가 있을 때 */
    height: 40px;
    width: 40px;
    object-fit: contain;
    border-radius: 10px;
}
.app-logo-emoji {                      /* 로고 파일이 없을 때 */
    width: 40px;
    height: 40px;
    display: flex;
    justify-content: center;
    align-items: center;
    background: var(--badge-bg);
    border-radius: 10px;
    font-size: 24px;
}
.app-name {
    font-size: 22px;
    font-weight: 800;
    color: var(--dark-green);
    letter-spacing: -0.3px;
}


/* 3. 화면 높이에 맞춰 카드 크기 자동 조절
   - max(최소값, 계산값): 창이 작아도 최소값보다 작아지지 않음
   - var(--header-h): 위쪽 로고 헤더만큼 카드 높이를 줄임
   - 주의: 이 값이 파이썬의 height= 값보다 우선함 */
div:has(> .st-key-ai_box) {            /* AI 채팅 카드 */
    flex-basis: max(517px, calc(100vh / var(--zoom) - 160px - var(--header-h))) !important;
    height:     max(517px, calc(100vh / var(--zoom) - 160px - var(--header-h))) !important;
}
div:has(> .st-key-chat_area) {         /* 채팅 기록 스크롤 영역 */
    flex-basis: max(282px, calc(100vh / var(--zoom) - 395px - var(--header-h))) !important;
    height:     max(282px, calc(100vh / var(--zoom) - 395px - var(--header-h))) !important;
}
div:has(> .st-key-plant_box) {         /* 식물 영역 */
    flex-basis: max(210px, calc(100vh / var(--zoom) - 467px - var(--header-h))) !important;
    height:     max(210px, calc(100vh / var(--zoom) - 467px - var(--header-h))) !important;
}


/* 4. 메인 화면 카드 공통 → key="status_box", "ai_box" */
.st-key-status_box,
.st-key-ai_box {
    border: 1px solid var(--border) !important;
    border-radius: 16px !important;
    background: var(--card-bg) !important;
}


/* 5. 식물 영역 → key="plant_box" */

/* 아래쪽 흙(갈색 그라데이션) + 나머지 흰 배경 */
.st-key-plant_box {
    position: relative;
    border: 1px solid var(--border) !important;
    border-radius: 16px !important;
    background:
        linear-gradient(to top, #654323 5%, #9B7046 16%, transparent 25%),   /* 흙 */
        #FFFFFF !important;                                                   /* 배경 */
    background-origin: border-box !important;
    background-repeat: no-repeat !important;
}

/* 안쪽 요소들이 식물 영역 기준으로 위치를 잡도록 */
.st-key-plant_box [data-testid="stElementContainer"] {
    position: static;
}

/* "● 식물 이름" 배지 */
.plant-badge {
    display: inline-block;
    background: var(--badge-bg);
    color: var(--dark-green);
    padding: 6px 13px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 600;
}

/* 식물 이모지·성장 단계·설명 영역 (아래 3개는 나중에 성장 단계 표시할 때 사용) */
.plant-center {
    text-align: center;
    margin-top: 30px;
}
.plant-emoji {
    font-size: 72px;
    line-height: 1;
}
.plant-stage {
    font-size: 15px;
    font-weight: 700;
    color: #315C40;
    margin-top: 10px;
}
.plant-desc {
    font-size: 12px;
    color: var(--sub-text);
    margin-top: 5px;
}


/* 6. 상태창 → key="status_box" */
.status-title {                        /* "식물 상태" */
    font-weight: 700;
    color: var(--text);
    margin-bottom: 4px;
}
.status-label {                        /* "수분", "영양" */
    color: var(--sub-text);
    font-size: 13px;
    margin-bottom: 5px;
}


/* 7. 식물 관리 버튼 (💧, 2, 3, 4) → key="care_buttons" */
.st-key-care_buttons button {
    background: var(--card-bg);
    color: var(--text);
    border: 1px solid var(--border);
    border-radius: 10px;
    font-weight: 600;
    transition: 0.2s;
}
.st-key-care_buttons button:hover {
    background: var(--light-green);
    border-color: var(--green);
    color: var(--dark-green);
}


/* 8. AI 채팅 헤더 (아이콘 + "AI") */
.ai-header {
    display: flex;
    align-items: center;
    gap: 10px;
}
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
.ai-header-title {
    font-size: 20px;
    font-weight: 700;
    color: var(--text);
}


/* 9. 채팅 말풍선 → app.py 의 chat_bubble() */
.chat-row {                            /* 아이콘 + 말풍선 한 줄 */
    display: flex;
    align-items: flex-start;
    gap: 8px;
    margin: 6px 0;
}
.chat-user {                           /* 사용자 줄: 오른쪽 정렬 */
    flex-direction: row-reverse;
}
.chat-icon {
    width: 32px;
    height: 32px;
    flex-shrink: 0;                    /* 말풍선이 길어져도 찌그러지지 않게 */
    border-radius: 10px;
    background: var(--badge-bg);
    display: flex;
    justify-content: center;
    align-items: center;
}
.chat-bubble {
    max-width: 75%;
    padding: 9px 13px;
    border-radius: 14px;
    font-size: 14px;
    line-height: 1.5;
    color: var(--text);
    word-break: break-word;            /* 긴 단어·URL 줄바꿈 */
}
.chat-ai .chat-bubble {                /* AI: 왼쪽, 회녹색 */
    background: var(--ai-bubble);
    border-top-left-radius: 4px;
}
.chat-user .chat-bubble {              /* 사용자: 오른쪽, 초록색 */
    background: var(--green);
    color: #FFFFFF;
    border-top-right-radius: 4px;
}


/* 10. 사이드바 메뉴 버튼 → key="sidebar_menu" */
.st-key-sidebar_menu button {
    background: var(--card-bg);
    color: var(--text);
    border: 1px solid var(--plant-border);
    border-radius: 12px;
    justify-content: flex-start;       /* 글자 왼쪽 정렬 */
    padding-left: 14px;
    transition: 0.2s;
}
.st-key-sidebar_menu button:hover {
    background: var(--light-green);
    border-color: var(--green);
    color: var(--dark-green);
}


/* 11. 팝업 공통 → ui/dialogs.py */

div[role="dialog"] {                   /* 팝업창 배경, 모서리 */
    background: var(--card-bg);
    border-radius: 20px;
}

/* 팝업 안의 흰 카드 전부 */
[class*="st-key-plant_card_"],         /* 식물 카드 */
[class*="st-key-record_row_"],         /* 내 기록 한 줄 */
[class*="st-key-stat_card_"],          /* 통계 그래프 카드 */
[class*="st-key-stat_metric_"],        /* 통계 숫자 카드 */
[class*="st-key-detail_box_"] {        /* 상세 팝업의 소개·메모 상자 */
    background: var(--white-card);
    border: 1px solid var(--plant-border) !important;
    border-radius: 14px !important;
    transition: 0.2s;
}

/* 누를 수 있는 카드는 마우스를 올리면 초록 테두리 */
[class*="st-key-plant_card_"]:hover,
[class*="st-key-stat_metric_"]:hover {
    border-color: var(--green) !important;
}

/* 글자만 보이는 "자세히 보기 ›" 버튼 → key="stat_btn_...", "record_btn_..." */
[class*="st-key-stat_btn_"] button,
[class*="st-key-record_btn_"] button {
    background: transparent;
    border: none;
    color: var(--dark-green);
    font-size: 13px;
    min-height: 0;
    padding: 2px 0;
}
[class*="st-key-stat_btn_"] button:hover,
[class*="st-key-record_btn_"] button:hover {
    background: var(--badge-bg);
    color: var(--dark-green);
}

/* "‹ ~로 돌아가기" 버튼 → key="back_to_..." */
[class*="st-key-back_to_"] button {
    background: transparent;
    border: none;
    color: var(--sub-text);
    font-size: 13px;
    padding: 0;
    min-height: 0;
}
[class*="st-key-back_to_"] button:hover {
    color: var(--dark-green);
    background: transparent;
}

/* 팝업 안의 숫자 카드 (st.metric) */
div[role="dialog"] [data-testid="stMetric"] {
    background: var(--white-card);
    border-radius: 14px;
}

/* 작은 굵은 제목 → section_title(), stat_card() */
.stat-title {
    font-size: 14px;
    font-weight: 700;
    color: var(--text);
    margin-bottom: 4px;
}

/* "식물 4개" 개수 표시 */
.picker-count {
    font-size: 13px;
    color: var(--sub-text);
    margin-bottom: 8px;
}


/* 12. 식물 카드 내용 → render_plant_cards() */
.plant-card-head {                     /* 이모지 + 이름 */
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
.plant-card-tags {                     /* 태그 묶음 */
    display: flex;
    flex-wrap: wrap;
    gap: 4px;
    margin-bottom: 4px;
}
.plant-tag {                           /* 태그 하나 (관엽식물, 반그늘 ...) */
    background: var(--badge-bg);
    color: var(--dark-green);
    font-size: 11px;
    padding: 2px 8px;
    border-radius: 10px;
}


/* 13. 내 기록 한 줄 내용 → my_record_dialog() */
.record-head {                         /* 이모지 + (이름 / 기간) */
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

/* 상태 배지 → status_badge_html() */
.record-badge {
    display: inline-block;
    font-size: 12px;
    font-weight: 600;
    padding: 4px 10px;
    border-radius: 12px;
}
.record-badge.ongoing {                /* 키우는 중 */
    background: var(--badge-bg);
    color: var(--dark-green);
}
.record-badge.done {                   /* 완료 */
    background: var(--done-bg);
    color: var(--sub-text);
}


/* 14. 상세 팝업 → 식물 정보, 기록 자세히 */
.detail-head {                         /* 큰 이모지 + 이름 → detail_header() */
    display: flex;
    align-items: center;
    gap: 16px;
    margin: 8px 0 16px;
}
.detail-emoji {
    font-size: 56px;
    line-height: 1;
}
.detail-name {
    font-size: 22px;
    font-weight: 700;
    color: var(--text);
    margin-bottom: 6px;
}

/* 키우기 정보 칸 (물 주기, 햇빛, 온도, 습도) */
.info-tile {
    background: var(--white-card);
    border: 1px solid var(--plant-border);
    border-radius: 14px;
    padding: 12px;
    text-align: center;
    margin-bottom: 12px;
}
.info-icon {
    font-size: 22px;
}
.info-label {
    font-size: 12px;
    color: var(--sub-text);
    margin-top: 4px;
}
.info-value {
    font-size: 15px;
    font-weight: 700;
    color: var(--text);
    margin-top: 2px;
}

/* 소개·관리 팁·성장 기록·메모 상자 높이 */
[class*="st-key-detail_box_"] {
    min-height: 160px;
}

</style>
"""