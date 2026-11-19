"""사이드바 메뉴에서 여는 팝업창 4개 (UI만, 기능은 TODO)

- new_plant_dialog()     : 새로 키우기 — 필터 + 식물 카드 + [키우기]
- search_plant_dialog()  : 식물 조회   — 검색창 + 필터 + 식물 카드 + [자세히 보기]
- my_record_dialog()     : 내 기록     — 상태 필터 + 키웠던 식물 목록
- my_statistics_dialog() : 통계       — 숫자 카드 3개 + 막대 그래프
"""

import altair as alt
import pandas as pd
import streamlit as st

# ============================================================
# 화면 확인용 예시 데이터 (나중에 CSV / DB 로 교체)
# ============================================================
SAMPLE_PLANTS = [
    {"emoji": "🪴", "name": "몬스테라",   "tags": ["관엽식물", "반그늘", "인테리어"]},
    {"emoji": "🌵", "name": "스투키",     "tags": ["다육식물", "그늘", "공기정화"]},
    {"emoji": "🌿", "name": "로즈마리",   "tags": ["허브", "양지", "요리"]},
    {"emoji": "🍅", "name": "방울토마토", "tags": ["채소", "양지", "수확"]},
]

SAMPLE_RECORDS = [
    {"emoji": "🪴", "name": "몬스테라",   "period": "2026.10.05 ~ 지금",       "days": 45, "status": "키우는 중"},
    {"emoji": "🌿", "name": "로즈마리",   "period": "2026.09.01 ~ 2026.10.20", "days": 49, "status": "완료"},
    {"emoji": "🍅", "name": "방울토마토", "period": "2026.07.10 ~ 2026.09.15", "days": 67, "status": "완료"},
]

FILTER_OPTIONS = {
    "종류": ["관엽식물", "다육식물", "허브", "채소"],
    "환경": ["양지", "반그늘", "그늘"],
    "용도": ["공기정화", "인테리어", "요리", "수확"],
}


# ============================================================
# 공통 부품 (여러 팝업에서 같이 씀)
# ============================================================
def render_filters(prefix):
    """종류 / 환경 / 용도 필터 (알약 버튼)
    prefix: 팝업마다 key 를 다르게 해서 선택값이 서로 섞이지 않게 함"""
    for label, options in FILTER_OPTIONS.items():
        st.pills(label, options, selection_mode="multi", key=f"{prefix}_filter_{label}")


def render_plant_cards(plants, prefix, button_label):
    """식물 카드 2열 배치
    button_label: 카드 아래 버튼 글자 ("키우기", "자세히 보기" 등)"""
    st.markdown(f'<div class="picker-count">식물 {len(plants)}개</div>',
                unsafe_allow_html=True)

    cols = st.columns(2)
    for i, p in enumerate(plants):
        with cols[i % 2]:                                     # 왼쪽, 오른쪽 번갈아 배치
            # key 에 "plant_card_" 가 들어가야 CSS([class*="st-key-plant_card_"])가 적용됨
            with st.container(border=True, key=f"plant_card_{prefix}_{i}"):
                tags = "".join(f'<span class="plant-tag">{t}</span>' for t in p["tags"])
                st.markdown(
                    f'<div class="plant-card-head">'
                    f'<span class="plant-card-emoji">{p["emoji"]}</span>'
                    f'<span class="plant-card-name">{p["name"]}</span>'
                    f'</div>'
                    f'<div class="plant-card-tags">{tags}</div>',
                    unsafe_allow_html=True,
                )
                st.button(button_label, key=f"{prefix}_btn_{i}", width="stretch")  # TODO: 기능 연결


# ============================================================
# 1. 새로 키우기
# ============================================================
@st.dialog("새로 키우기", width="large")
def new_plant_dialog():
    st.caption("키우고 싶은 식물을 골라 보세요.")
    render_filters("new")
    st.divider()
    render_plant_cards(SAMPLE_PLANTS, "new", "🌱 키우기")


# ============================================================
# 2. 식물 조회 (도감처럼 정보 찾아보기)
# ============================================================
@st.dialog("식물 조회", width="large")
def search_plant_dialog():
    st.caption("궁금한 식물의 정보를 찾아보세요.")
    st.text_input("검색", placeholder="🔍 식물 이름을 입력하세요",
                  key="search_query", label_visibility="collapsed")   # TODO: 검색 연결
    render_filters("search")
    st.divider()
    render_plant_cards(SAMPLE_PLANTS, "search", "자세히 보기")


# ============================================================
# 3. 내 기록 (키웠던 식물 목록)
# ============================================================
@st.dialog("내 기록", width="large")
def my_record_dialog():
    st.caption("지금까지 키운 식물이에요.")

    st.pills("상태", ["전체", "키우는 중", "완료"], selection_mode="single",
             default="전체", key="record_status", label_visibility="collapsed")  # TODO: 필터 연결

    for i, r in enumerate(SAMPLE_RECORDS):
        with st.container(border=True, key=f"record_row_{i}"):
            left, right = st.columns([4, 1], vertical_alignment="center")
            with left:
                st.markdown(
                    f'<div class="record-head">'
                    f'<span class="record-emoji">{r["emoji"]}</span>'
                    f'<div>'
                    f'<div class="record-name">{r["name"]}</div>'
                    f'<div class="record-sub">{r["period"]} · {r["days"]}일</div>'
                    f'</div>'
                    f'</div>',
                    unsafe_allow_html=True,
                )
            with right:
                badge = "ongoing" if r["status"] == "키우는 중" else "done"
                st.markdown(f'<span class="record-badge {badge}">{r["status"]}</span>',
                            unsafe_allow_html=True)


# ============================================================
# 4. 통계
# ============================================================
@st.dialog("통계", width="large")
def my_statistics_dialog():
    st.caption("내가 키운 식물을 한눈에 볼 수 있어요.")

    # ── 숫자 카드 3개 ──
    m1, m2, m3 = st.columns(3)
    m1.metric("키운 식물", "3개", border=True)
    m2.metric("총 돌본 기간", "161일", border=True)
    m3.metric("물 준 횟수", "48회", border=True)

    st.divider()

    # ── 종류별 막대 그래프 ──
    st.markdown('<div class="stat-title">종류별로 키운 식물</div>', unsafe_allow_html=True)
    df = pd.DataFrame(
        {"종류": ["관엽식물", "다육식물", "허브", "채소"], "개수": [1, 0, 1, 1]}
    )

    chart = (
        alt.Chart(df)
        .mark_bar(
            size=40,                         # 막대 두께
            color="#03C75A",
            cornerRadiusTopLeft=6,           # 막대 윗모서리 둥글게
            cornerRadiusTopRight=6,
        )
        .encode(
            x=alt.X("종류:N", sort=None,     # sort=None: 데이터 순서 그대로
                    axis=alt.Axis(labelAngle=0, title=None, labelFontSize=13)),  # 글자 눕지 않게
            y=alt.Y("개수:Q",
                    axis=alt.Axis(title=None, tickMinStep=1, format="d")),       # 눈금을 정수로
        )
        .properties(height=500)              # 그래프 높이 (팝업도 같이 길어짐)
    )
    st.altair_chart(chart, width="stretch")