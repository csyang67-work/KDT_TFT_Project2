import html

import streamlit as st

from ui.styles import CSS
from ui.dialogs import (
    new_plant_dialog,
    search_plant_dialog,
    my_record_dialog,
    my_statistics_dialog,
)

# 1. 페이지 설정
st.set_page_config(
    page_title="Oh My Garden",
    page_icon="🌱",
    layout="centered",
)

#2. CSS 
st.markdown(CSS, unsafe_allow_html=True)

# 3. 상태 초기화 (처음 접속했을 때 한 번만 실행)
if "messages" not in st.session_state:
    st.session_state.messages = []

if "plant" not in st.session_state:
    st.session_state.plant = {
        "name": "식물 이름",
        "수분": 0,
        "영양": 0,
        "행복도": 0,
    }

plant = st.session_state.plant


# 4. 도우미 함수
def clamp(value):
    """값을 0~100 사이로 제한"""
    return max(0, min(100, value))


def water_plant():
    """물주기 버튼 콜백 (on_click은 화면을 다시 그리기 전에 실행됨)"""
    plant["수분"] = clamp(plant["수분"] + 20)
    plant["영양"] = clamp(plant["영양"] + 10)


def chat_bubble(role, content):
    """말풍선 생성"""
    safe_text = html.escape(content).replace("\n", "<br>")

    row_class = "chat-ai" if role == "assistant" else "chat-user"
    icon = "🌱" if role == "assistant" else "🐸"

    return (
        f'<div class="chat-row {row_class}">'
        f'<div class="chat-icon">{icon}</div>'
        f'<div class="chat-bubble">{safe_text}</div>'
        f"</div>"
    )


# 5. 화면 그리기
def render_plant_area():
    # 식물 영역
    with st.container(border=True, width=330, height=400, key="plant_box"):
        st.markdown(
            f'<div class="plant-badge">● {html.escape(plant["name"])}</div>'
            f'<div class="plant-center">'
            f"</div>",
            unsafe_allow_html=True,
        )

    # 식물 관리 버튼
    with st.container(width=330, key="care_buttons"):
        b1, b2, b3, b4 = st.columns(4)
        with b1:
            st.button("💧", width="stretch", help="물주기", on_click=water_plant)
        with b2:
            st.button("2", width="stretch", help="?")    # TODO: 기능 연결
        with b3:
            st.button("3", width="stretch", help="??")   # TODO: 기능 연결
        with b4:
            st.button("4", width="stretch", help="???")  # TODO: 기능 연결

    # 상태창
    with st.container(border=True, width=330, height=235, key="status_box"):
        st.markdown('<div class="status-title">식물 상태</div>', unsafe_allow_html=True)

        for label in ["수분", "영양"]:
            value = int(plant[label])
            st.markdown(f'<div class="status-label">{label}</div>', unsafe_allow_html=True)
            st.progress(value / 100, text=f"{value}%")


def render_chat_area():
    with st.container(border=True, width=560, height=715, key="ai_box"):
        st.markdown(
            '<div class="ai-header">'
            '<div class="ai-header-icon">🌱</div>'
            '<div class="ai-header-title">AI</div>'
            "</div>",
            unsafe_allow_html=True,
        )

        st.divider()

        # 대화 기록 (이 안에서만 스크롤, 새 메시지가 오면 자동으로 맨 아래로)
        with st.container(height=480, border=False, autoscroll=True, key="chat_area"):
            for message in st.session_state.messages:
                st.markdown(
                    chat_bubble(message["role"], message["content"]),
                    unsafe_allow_html=True,
                )

        # 메시지 입력
        user_input = st.chat_input("메시지를 입력하세요.")

        if user_input:
            st.session_state.messages.append({"role": "user", "content": user_input})

            # TODO: 여기서 실제 AI 응답을 받아서 넣으면 됨
            st.session_state.messages.append(
                {"role": "assistant", "content": "AI 응답이 여기에 표시됩니다."}
            ) 

            st.rerun()


# 6. 사이드바 (팝업 내용은 ui/dialogs.py)
with st.sidebar:
    st.title("내 정보")

    with st.container(key="sidebar_menu"):
        if st.button("🌱 새로 키우기", width="stretch", key="menu_new"):
            new_plant_dialog()
        if st.button("📒 내 기록", width="stretch", key="menu_record"):
            my_record_dialog()
        if st.button("📊 통계", width="stretch", key="menu_stats"):
            my_statistics_dialog()
        if st.button("🔍 식물 조회", width="stretch", key="menu_search"):
            search_plant_dialog()


# 7. 실행
col_plants, col_ai = st.columns([0.8, 1.2])

with col_plants:
    render_plant_area()

with col_ai:
    render_chat_area()