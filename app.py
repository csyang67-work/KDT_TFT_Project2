"""Oh My Garden — 웹 화면 진입점

화면 구성
- 맨 위 왼쪽: 로고 + 앱 이름
- 왼쪽: 식물 영역 + 관리 버튼 + 상태창
- 오른쪽: AI 채팅
- 사이드바: 메뉴 버튼 (누르면 ui/dialogs.py 의 팝업이 열림)
"""

import base64
import html
from pathlib import Path

import streamlit as st

from ui.dialogs import (
    my_record_dialog,
    my_statistics_dialog,
    new_plant_dialog,
    open_next_dialog,
    search_plant_dialog,
)
from ui.styles import CSS

APP_NAME = "Oh! My Garden"
LOGO_PATH = Path(__file__).parent / "assets" / "logo.png"   # 없으면 🌱 이모지로 대신 표시

# 1. 페이지 설정 (st 명령 중 가장 먼저 실행되어야 함)
st.set_page_config(
    page_title=APP_NAME,
    page_icon="🌱",
    layout="centered",
)

st.markdown(CSS, unsafe_allow_html=True)


# 2. 상태 초기화 (처음 접속했을 때 한 번만 실행)
if "messages" not in st.session_state:
    st.session_state.messages = []

if "plant" not in st.session_state:
    st.session_state.plant = {
        "name": "식물 이름",
        "수분": 0,
        "영양": 0,
        "행복도": 0,      # TODO: 상태창에 표시할지 결정
    }

plant = st.session_state.plant


# 3. 도우미 함수
def clamp(value):
    """값을 0~100 사이로 제한"""
    return max(0, min(100, value))


def water_plant():
    """물주기 버튼: AI에게 메시지를 보낸다"""

    st.session_state.pending_input="물을 줄게"

def repotting_plant():
    """ 분갈이 버튼: AI에게 메시지를 보낸다 """
    st.session_state.pending_input="분갈이를 할게"

def fertilization_plant():
    """ 비료주기 버튼: AI에게 메시지를 보낸다 """
    st.session_state.pending_input="비료를 줄게"

def move_plant():
    """ 자리옮기기 버튼: AI에게 메시지를 보낸다. """
    st.session_state.pending_input="자리를 옮길게"

def chat_bubble(role, content):
    """말풍선 HTML 생성"""
    # <, > 같은 문자가 HTML 로 해석되지 않게 바꾸고, 줄바꿈은 <br> 로 변환
    safe_text = html.escape(content).replace("\n", "<br>")

    row_class = "chat-ai" if role == "assistant" else "chat-user"
    icon = "🌱" if role == "assistant" else "🐸"

    return (
        f'<div class="chat-row {row_class}">'
        f'<div class="chat-icon">{icon}</div>'
        f'<div class="chat-bubble">{safe_text}</div>'
        f"</div>"
    )


# 4. 화면 그리기
def logo_html():
    """로고: assets/logo.png 가 있으면 그 이미지, 없으면 🌱 이모지"""
    if LOGO_PATH.exists():
        encoded = base64.b64encode(LOGO_PATH.read_bytes()).decode()
        return f'<img class="app-logo-img" src="data:image/png;base64,{encoded}" alt="logo">'
    return '<span class="app-logo-emoji">🌱</span>'


def render_header():
    """메인 화면 왼쪽 위: 로고 + 앱 이름"""
    st.markdown(
        f'<div class="app-header">'
        f'{logo_html()}'
        f'<span class="app-name">{html.escape(APP_NAME)}</span>'
        f'</div>',
        unsafe_allow_html=True,
    )


def render_plant_area():
    """왼쪽: 식물 영역 + 관리 버튼 + 상태창"""
    # 식물 영역
    with st.container(border=True, width=330, height=400, key="plant_box"):
        st.markdown(
            f'<div class="plant-badge">● {html.escape(plant["name"])}</div>'
            f'<div class="plant-center"></div>',
            unsafe_allow_html=True,
        )

    # 식물 관리 버튼
    with st.container(width=330, key="care_buttons"):
        b1, b2, b3, b4 = st.columns(4)
        b1.button("💧", width="stretch", help="물주기", on_click=water_plant)
        b2.button("🌿", width="stretch", help="분갈이", on_click=repotting_plant)
        b3.button("💩", width="stretch", help="비료주기", on_click=fertilization_plant, key="ddongbutton_key")
        b4.button("➡️", width="stretch", help="자리옮기기", on_click=move_plant)
    # 상태창
    with st.container(border=True, width=330, height=235, key="status_box"):
        st.markdown('<div class="status-title">식물 상태</div>', unsafe_allow_html=True)

        for label in ["수분", "영양"]:
            value = int(plant[label])
            st.markdown(f'<div class="status-label">{label}</div>', unsafe_allow_html=True)
            st.progress(value / 100, text=f"{value}%")


def render_chat_area():
    """오른쪽: AI 채팅"""
    with st.container(border=True, width=560, height=715, key="ai_box"):
        st.markdown(
            '<div class="ai-header">'
            '<div class="ai-header-icon">🌱</div>'
            '<div class="ai-header-title">AI</div>'
            "</div>",
            unsafe_allow_html=True,
        )

        st.divider()

        # 대화 기록 
        with st.container(height=480, border=False, autoscroll=True, key="chat_area"):
            for message in st.session_state.messages:
                st.markdown(
                    chat_bubble(message["role"], message["content"]),
                    unsafe_allow_html=True,
                )

        # 메시지 입력
        typed = st.chat_input("메시지를 입력하세요.")
        # 직접 입력한 메시지가 없으면, 버튼이 예약한 메시지를 꺼냄 (pop: 한 번 쓰면 삭제)
        user_input = typed or st.session_state.pop("pending_input", None)

        if user_input:
            st.session_state.messages.append({"role": "user", "content": user_input})

            # TODO: 여기서 실제 AI 응답을 받아서 넣으면 됨
            st.session_state.messages.append(
                {"role": "assistant", "content": "AI 응답이 여기에 표시됩니다."}
            )

            st.rerun()


def render_sidebar():
    """사이드바 메뉴 (팝업 내용은 ui/dialogs.py)"""
    with st.sidebar:
        st.title("내 정보")

        with st.container(key="sidebar_menu"):
            if st.button("🌱 새로 키우기", width="stretch", key="menu_new"):
                new_plant_dialog()
            if st.button("🔍 식물 조회", width="stretch", key="menu_search"):
                search_plant_dialog()
            if st.button("📒 내 기록", width="stretch", key="menu_record"):
                my_record_dialog()
            if st.button("📊 통계", width="stretch", key="menu_stats"):
                my_statistics_dialog()


# 5. 실행
render_sidebar()
open_next_dialog()      # 팝업 안에서 다른 팝업으로 이동하도록 예약된 게 있으면 열기
render_header()

col_plants, col_ai = st.columns([0.8, 1.2])

with col_plants:
    render_plant_area()

with col_ai:
    render_chat_area()