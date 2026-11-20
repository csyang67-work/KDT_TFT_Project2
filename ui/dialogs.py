"""사이드바 메뉴에서 여는 팝업창 4개 (UI만, 기능은 TODO)

- new_plant_dialog()     : 새로 키우기 — 필터 + 식물 카드 + [키우기]
- search_plant_dialog()  : 식물 조회   — 검색창 + 필터 + 식물 카드 + [자세히 보기]
  └ plant_detail_dialog  : 식물 정보 상세 팝업
- my_record_dialog()     : 내 기록     — 상태 필터 + 키웠던 식물 목록 + [자세히 보기]
  └ record_detail_dialog : 기록 상세 팝업
- my_statistics_dialog() : 통계       — 숫자 카드 3개(누르면 상세 팝업) + 그래프 4개 (막대, 도넛, 꺾은선, 가로 막대)
  └ stat_count_dialog / stat_days_dialog / stat_water_dialog : 통계 카드별 상세 팝업
"""

import altair as alt
import pandas as pd
import streamlit as st

# 화면 확인용 예시 데이터 (나중에 CSV로 교체)
SAMPLE_PLANTS = [
    {"emoji": "🌱", "name": "몬스테라",   "tags": ["관엽식물", "반그늘", "인테리어"]},
    {"emoji": "🌵", "name": "스투키",     "tags": ["다육식물", "그늘", "공기정화"]},
    {"emoji": "🌿", "name": "로즈마리",   "tags": ["허브", "양지", "요리"]},
    {"emoji": "🍅", "name": "방울토마토", "tags": ["채소", "양지", "수확"]},
]

SAMPLE_RECORDS = [
    {"emoji": "🌱", "name": "몬스테라",   "type": "관엽식물", "period": "2026.10.05 ~ 지금",
     "days": 45, "status": "키우는 중", "water": 14, "last_water": "2026.11.18"},
    {"emoji": "🌿", "name": "로즈마리",   "type": "허브",     "period": "2026.09.01 ~ 2026.10.20",
     "days": 49, "status": "완료",      "water": 16, "last_water": "2026.10.19"},
    {"emoji": "🍅", "name": "방울토마토", "type": "채소",     "period": "2026.07.10 ~ 2026.09.15",
     "days": 67, "status": "완료",      "water": 18, "last_water": "2026.09.14"},
]

FILTER_OPTIONS = {
    "종류": ["관엽식물", "다육식물", "허브", "채소"],
    "환경": ["양지", "반그늘", "그늘"],
    "용도": ["공기정화", "인테리어", "요리", "수확"],
}


# 공통 부품 (여러 팝업에서 같이 씀)
def set_next_dialog(name, data=None):
    """버튼 콜백: 다음에 열 팝업 이름(+ 넘겨줄 값)을 저장"""
    st.session_state.next_dialog = name
    st.session_state.dialog_data = data      # 예: 몇 번째 식물/기록을 눌렀는지


def nav_button(label, target, key, data=None, **kwargs):
    """누르면 지금 팝업을 닫고 target 팝업을 여는 버튼
    - data: 다음 팝업에 넘겨줄 값 (다음 팝업에서 st.session_state.dialog_data 로 꺼냄)
    Streamlit 은 팝업을 한 번에 하나만 열 수 있어서,
    열 팝업 이름을 저장해 두고 앱 전체를 다시 실행함 → app.py 의 open_next_dialog() 가 열어 줌"""
    st.button(label, key=key, on_click=set_next_dialog, args=(target, data), **kwargs)
    if st.session_state.get("next_dialog") == target:
        st.rerun()          # 팝업 안에서 부르면 앱 전체를 다시 실행 → 지금 팝업이 닫힘


def open_next_dialog():
    """app.py 에서 매번 호출: 열기로 예약된 팝업이 있으면 연다"""
    name = st.session_state.pop("next_dialog", None)    # 한 번 열면 예약 지움
    if name in DIALOGS:
        DIALOGS[name]()


def back_button(label, target, key):
    """상세 팝업 맨 위의 뒤로 가기 버튼
    key 를 "back_to_..." 로 지어야 CSS([class*="st-key-back_to_"])가 적용됨"""
    nav_button(f"‹ {label}", target, key=key)


def render_filters(prefix):
    """종류 / 환경 / 용도 필터 (알약 버튼)
    prefix: 팝업마다 key 를 다르게 해서 선택값이 서로 섞이지 않게 함"""
    for label, options in FILTER_OPTIONS.items():
        st.pills(label, options, selection_mode="multi", key=f"{prefix}_filter_{label}")


def render_plant_cards(plants, prefix, button_label, target=None):
    """식물 카드 2열 배치
    button_label: 카드 아래 버튼 글자 ("키우기", "자세히 보기" 등)
    target: 버튼을 누르면 열 팝업 이름 (없으면 일반 버튼)"""
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
                if target:
                    nav_button(button_label, target, key=f"{prefix}_btn_{i}",
                               data=i, width="stretch")      # 몇 번째 식물인지 넘김
                else:
                    st.button(button_label, key=f"{prefix}_btn_{i}", width="stretch")  # TODO: 기능 연결


# 1. 새로 키우기
@st.dialog("새로 키우기", width="large")
def new_plant_dialog():
    st.caption("키우고 싶은 식물을 골라 보세요.")
    render_filters("new")
    st.divider()
    render_plant_cards(SAMPLE_PLANTS, "new", "🌱 키우기")


# 2. 식물 조회 (도감처럼 정보 찾아보기)
@st.dialog("식물 조회", width="large")
def search_plant_dialog():
    st.caption("궁금한 식물의 정보를 찾아보세요.")
    st.text_input("검색", placeholder="🔍 식물 이름을 입력하세요",
                  key="search_query", label_visibility="collapsed")   # TODO: 검색 연결
    render_filters("search")
    st.divider()
    render_plant_cards(SAMPLE_PLANTS, "search", "자세히 보기 ›", target="plant_detail")


@st.dialog("식물 정보", width=1000)
def plant_detail_dialog():
    """식물 조회 → 자세히 보기 (UI만, 내용은 TODO)"""
    back_button("식물 조회로 돌아가기", "search", key="back_to_search")

    i = st.session_state.get("dialog_data") or 0
    p = SAMPLE_PLANTS[i]                                   # TODO: 실제 식물 데이터로 교체

    # ── 머리: 이모지 + 이름 + 태그 ──
    tags = "".join(f'<span class="plant-tag">{t}</span>' for t in p["tags"])
    st.markdown(
        f'<div class="detail-head">'
        f'<span class="detail-emoji">{p["emoji"]}</span>'
        f'<div>'
        f'<div class="detail-name">{p["name"]}</div>'
        f'<div class="plant-card-tags">{tags}</div>'
        f'</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

    # ── 키우기 정보 4칸 ──
    info = [("💧", "물 주기", "-"), ("☀️", "햇빛", "-"),
            ("🌡️", "온도", "-"), ("💦", "습도", "-")]          # TODO: 데이터 연결
    for col, (icon, label, value) in zip(st.columns(4), info):
        col.markdown(
            f'<div class="info-tile">'
            f'<div class="info-icon">{icon}</div>'
            f'<div class="info-label">{label}</div>'
            f'<div class="info-value">{value}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

    # ── 소개 | 관리 팁 ──
    left, right = st.columns(2)
    with left:
        with st.container(border=True, key="detail_box_intro"):
            st.markdown('<div class="stat-title">소개</div>', unsafe_allow_html=True)
            st.caption("식물 소개가 여기에 표시됩니다.")          # TODO
    with right:
        with st.container(border=True, key="detail_box_tips"):
            st.markdown('<div class="stat-title">관리 팁</div>', unsafe_allow_html=True)
            st.caption("관리 팁이 여기에 표시됩니다.")            # TODO

    st.button("🌱 이 식물 키우기", type="primary", width="stretch",
              key="detail_grow")                                 # TODO: 기능 연결


# 3. 내 기록 (키웠던 식물 목록)
@st.dialog("내 기록", width="large")
def my_record_dialog():
    st.caption("지금까지 키운 식물이에요.")

    st.pills("상태", ["전체", "키우는 중", "완료"], selection_mode="single",
             default="전체", key="record_status", label_visibility="collapsed")  # TODO: 필터 연결

    for i, r in enumerate(SAMPLE_RECORDS):
        with st.container(border=True, key=f"record_row_{i}"):
            left, right = st.columns([4, 1.3], vertical_alignment="center")
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
                nav_button("자세히 보기 ›", "record_detail", key=f"record_btn_{i}",
                           data=i, width="stretch")       # 몇 번째 기록인지 넘김


@st.dialog("기록 자세히", width=1000)
def record_detail_dialog():
    """내 기록 → 자세히 보기 (UI만, 내용은 TODO)"""
    back_button("내 기록으로 돌아가기", "record", key="back_to_record")

    i = st.session_state.get("dialog_data") or 0
    r = SAMPLE_RECORDS[i]                                  # TODO: 실제 기록 데이터로 교체

    # ── 머리: 이모지 + 이름 + 상태 + 기간 ──
    badge = "ongoing" if r["status"] == "키우는 중" else "done"
    st.markdown(
        f'<div class="detail-head">'
        f'<span class="detail-emoji">{r["emoji"]}</span>'
        f'<div>'
        f'<div class="detail-name">{r["name"]} '
        f'<span class="record-badge {badge}">{r["status"]}</span></div>'
        f'<div class="record-sub">{r["period"]}</div>'
        f'</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

    # ── 숫자 3칸 ──
    a, b, c = st.columns(3)
    a.metric("키운 기간", f'{r["days"]}일', border=True)
    b.metric("물 준 횟수", f'{r["water"]}회', border=True)
    c.metric("마지막으로 물 준 날", r["last_water"], border=True)

    # ── 성장 기록 | 메모 ──
    left, right = st.columns(2)
    with left:
        with st.container(border=True, key="detail_box_timeline"):
            st.markdown('<div class="stat-title">성장 기록</div>', unsafe_allow_html=True)
            st.caption("날짜별 성장 기록이 여기에 표시됩니다.")    # TODO
    with right:
        with st.container(border=True, key="detail_box_memo"):
            st.markdown('<div class="stat-title">메모</div>', unsafe_allow_html=True)
            st.caption("남긴 메모가 여기에 표시됩니다.")          # TODO


# 4. 통계
GREEN = "#03C75A"
GREEN_SHADES = ["#03C75A", "#7FD9A4", "#C4DECB"]   # 도넛 그래프 조각 색


def stat_card(title, key):
    """그래프 하나를 감싸는 흰 카드 + 제목"""
    box = st.container(border=True, key=f"stat_card_{key}")
    box.markdown(f'<div class="stat-title">{title}</div>', unsafe_allow_html=True)
    return box


def render_stat_card(key, label, value):
    """누를 수 있는 숫자 카드 → 누르면 해당 상세 팝업으로 이동"""
    with st.container(border=True, key=f"stat_metric_{key}"):
        st.metric(label, value)
        nav_button("자세히 보기 ›", f"stat_{key}", key=f"stat_btn_{key}", width="stretch")


def back_to_stats_button():
    back_button("통계로 돌아가기", "stats", key="back_to_stats")


def detail_count():
    """키운 식물 → 식물 목록"""
    st.markdown('<div class="stat-title">키운 식물 목록</div>', unsafe_allow_html=True)
    df = pd.DataFrame([
        {"식물": f'{r["emoji"]} {r["name"]}', "종류": r["type"],
         "기간": r["period"], "상태": r["status"]}
        for r in SAMPLE_RECORDS
    ])
    st.dataframe(df, hide_index=True, width="stretch")


def detail_days():
    """총 돌본 기간 → 식물별 기간 + 평균·최장·최단"""
    days = [r["days"] for r in SAMPLE_RECORDS]
    longest = max(SAMPLE_RECORDS, key=lambda r: r["days"])
    shortest = min(SAMPLE_RECORDS, key=lambda r: r["days"])

    st.markdown('<div class="stat-title">돌본 기간 자세히</div>', unsafe_allow_html=True)
    a, b, c = st.columns(3)
    a.metric("평균", f"{round(sum(days) / len(days))}일")
    b.metric("가장 오래", f'{longest["name"]} {longest["days"]}일')
    c.metric("가장 짧게", f'{shortest["name"]} {shortest["days"]}일')

    df = pd.DataFrame([
        {"식물": f'{r["emoji"]} {r["name"]}', "기간": r["period"], "일수": r["days"]}
        for r in SAMPLE_RECORDS
    ])
    st.dataframe(
        df, hide_index=True, width="stretch",
        column_config={
            "일수": st.column_config.ProgressColumn(      # 숫자를 막대로 표시
                "일수", min_value=0, max_value=max(days), format="%d일"),
        },
    )


def detail_water():
    """물 준 횟수 → 식물별 횟수 + 마지막으로 물 준 날"""
    counts = [r["water"] for r in SAMPLE_RECORDS]

    st.markdown('<div class="stat-title">물 준 기록</div>', unsafe_allow_html=True)
    a, b = st.columns(2)
    a.metric("식물당 평균", f"{round(sum(counts) / len(counts))}회")
    b.metric("며칠에 한 번꼴",
             f'{round(sum(r["days"] for r in SAMPLE_RECORDS) / sum(counts), 1)}일')

    df = pd.DataFrame([
        {"식물": f'{r["emoji"]} {r["name"]}', "횟수": r["water"],
         "마지막으로 물 준 날": r["last_water"]}
        for r in SAMPLE_RECORDS
    ])
    st.dataframe(
        df, hide_index=True, width="stretch",
        column_config={
            "횟수": st.column_config.ProgressColumn(
                "횟수", min_value=0, max_value=max(counts), format="%d회"),
        },
    )


# 상세 팝업 3개 (통계 카드를 누르면 열림)
@st.dialog("키운 식물", width=1000)
def stat_count_dialog():
    back_to_stats_button()
    detail_count()                # TODO: 실제 기록 데이터 연결


@st.dialog("돌본 기간", width=1000)
def stat_days_dialog():
    back_to_stats_button()
    detail_days()                 # TODO: 실제 기록 데이터 연결


@st.dialog("물 준 기록", width=1000)
def stat_water_dialog():
    back_to_stats_button()
    detail_water()                # TODO: 실제 기록 데이터 연결


# width=정수: 팝업 가로 폭을 픽셀로 지정 (최신 Streamlit 에서 지원)
@st.dialog("통계", width=1000)
def my_statistics_dialog():
    st.caption("내가 키운 식물을 한눈에 볼 수 있어요.")

    # ── 1줄: 누를 수 있는 숫자 카드 3개 ──
    total_days = sum(r["days"] for r in SAMPLE_RECORDS)
    total_water = sum(r["water"] for r in SAMPLE_RECORDS)

    cards = [
        ("count", "키운 식물",    f"{len(SAMPLE_RECORDS)}개"),
        ("days",  "총 돌본 기간", f"{total_days}일"),
        ("water", "물 준 횟수",   f"{total_water}회"),
    ]

    cols = st.columns(len(cards))
    for col, (key, label, value) in zip(cols, cards):
        with col:
            render_stat_card(key, label, value)

    # ── 2줄: 종류별 막대 | 환경별 도넛 ──
    left, right = st.columns(2)

    with left:
        with stat_card("종류별로 키운 식물", "type"):
            df = pd.DataFrame({"종류": ["관엽식물", "다육식물", "허브", "채소"],
                               "개수": [1, 0, 1, 1]})
            chart = (
                alt.Chart(df)
                .mark_bar(size=48, color=GREEN,
                          cornerRadiusTopLeft=6, cornerRadiusTopRight=6)
                .encode(
                    x=alt.X("종류:N", sort=None,
                            axis=alt.Axis(labelAngle=0, title=None, labelFontSize=12)),
                    y=alt.Y("개수:Q", axis=alt.Axis(title=None, tickMinStep=1, format="d")),
                )
                .properties(height=260)
            )
            st.altair_chart(chart, width="stretch")

    with right:
        with stat_card("환경별 비율", "env"):
            df = pd.DataFrame({"환경": ["양지", "반그늘", "그늘"], "개수": [2, 1, 0]})
            chart = (
                alt.Chart(df)
                .mark_arc(innerRadius=60)                       # 가운데를 비워서 도넛 모양
                .encode(
                    theta="개수:Q",                              # 조각 크기
                    color=alt.Color("환경:N", sort=None,
                                    scale=alt.Scale(range=GREEN_SHADES),
                                    legend=alt.Legend(orient="bottom", title=None)),
                    tooltip=["환경", "개수"],
                )
                .properties(height=260)
            )
            st.altair_chart(chart, width="stretch")

    # ── 3줄: 월별 물 준 횟수 (꺾은선) ──
    with stat_card("월별 물 준 횟수", "water"):
        df = pd.DataFrame({"월": ["7월", "8월", "9월", "10월", "11월"],
                           "횟수": [6, 12, 14, 9, 7]})
        chart = (
            alt.Chart(df)
            .mark_line(point=alt.OverlayMarkDef(size=70, color=GREEN),
                       color=GREEN, strokeWidth=3)
            .encode(
                x=alt.X("월:N", sort=None, axis=alt.Axis(labelAngle=0, title=None)),
                y=alt.Y("횟수:Q", axis=alt.Axis(title=None, tickMinStep=1, format="d")),
                tooltip=["월", "횟수"],
            )
            .properties(height=240)
        )
        st.altair_chart(chart, width="stretch")

    # ── 4줄: 식물별 키운 기간 (가로 막대) ──
    with stat_card("식물별 키운 기간", "days"):
        df = pd.DataFrame({"식물": [r["name"] for r in SAMPLE_RECORDS],
                           "일수": [r["days"] for r in SAMPLE_RECORDS]})
        chart = (
            alt.Chart(df)
            .mark_bar(size=28, color=GREEN,
                      cornerRadiusTopRight=6, cornerRadiusBottomRight=6)
            .encode(
                y=alt.Y("식물:N", sort="-x", axis=alt.Axis(title=None, labelFontSize=12)),  # 긴 순서
                x=alt.X("일수:Q", axis=alt.Axis(title="일", format="d")),
                tooltip=["식물", "일수"],
            )
            .properties(height=180)
        )
        st.altair_chart(chart, width="stretch")


# 팝업 이름 → 팝업 함수 
DIALOGS = {
    "search": search_plant_dialog,
    "plant_detail": plant_detail_dialog,
    "record": my_record_dialog,
    "record_detail": record_detail_dialog,
    "stats": my_statistics_dialog,
    "stat_count": stat_count_dialog,
    "stat_days": stat_days_dialog,
    "stat_water": stat_water_dialog,
}