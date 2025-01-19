import streamlit as st
from streamlit_quill import st_quill
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
import os
import pyperclip  # 클립보드 복사 모듈

# 환경 변수 로드
load_dotenv()

# ChatGPT 초기화
llm = ChatOpenAI(model_name="gpt-4", temperature=0)

def get_chatgpt_suggestions(input_text):
    """ChatGPT로부터 세부 주제 생성"""
    prompt = f"'{input_text}'와 관련된 5개의 세부 주제를 간결하게 생성해 주세요."
    response = llm.predict(prompt)
    return [line.strip() for line in response.split("\n") if line.strip()][:5]

def get_topic_details(selected_text):
    """선택된 주제에 대한 상세 설명 생성"""
    prompt = f"'{selected_text}'에 대해 초등학교 6학년 수준으로 상세히 설명해 주세요."
    response = llm.predict(prompt)
    return response

def sidebar():
    """사이드바 렌더링"""
    st.markdown(
        """
        <style>
            [data-testid="stSidebar"] {
                background: linear-gradient(45deg, #003366, #0055AA);
                padding-top: 20px;
                color: white;
            }
            [data-testid="stSidebar"] h2 {
                color: #E6F3FF;
                text-align: center;
                font-weight: bold;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )
    try:
        st.sidebar.image(
            "images/logo-removebg.png",
            use_container_width=True,
            caption="AI 디지털 리터러시",
        )
    except FileNotFoundError:
        st.sidebar.write("로고 이미지를 찾을 수 없습니다.")

def main():
    st.markdown(
        """
        <style>
            .main-title {
                text-align: center;
                font-size: 36px;
                color: #003366;
                font-weight: bold;
                margin-bottom: 20px;
                text-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2);
            }
            .sub-title {
                font-size: 22px;
                color: #0055AA;
                font-weight: bold;
                margin-bottom: 15px;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="main-title">디지털 리터러시 with AI</div>', unsafe_allow_html=True)

    # 화면 분할
    col1, col2 = st.columns([2, 3])

    # 상태 초기화
    if "suggestions" not in st.session_state:
        st.session_state.suggestions = []
    if "selected_text" not in st.session_state:
        st.session_state.selected_text = None
    if "topic_details" not in st.session_state:
        st.session_state.topic_details = ""

    with col1:
        st.markdown('<div class="sub-title">자료 탐색</div>', unsafe_allow_html=True)
        input_topic = st.text_input("학습 주제 입력", placeholder="학습 주제를 입력하세요")

        if st.button("주제 생성", help="학습 주제에 따라 추천 주제를 생성합니다"):
            if not input_topic.strip():
                st.warning("학습 주제를 입력하세요.")
            else:
                with st.spinner("ChatGPT에서 데이터를 가져오는 중..."):
                    st.session_state.suggestions = get_chatgpt_suggestions(input_topic)
                    st.session_state.selected_text = None

        if st.session_state.suggestions:
            st.markdown('<div class="sub-title">추천 주제</div>', unsafe_allow_html=True)

            # 버튼 생성 및 상태 관리
            for i, suggestion in enumerate(st.session_state.suggestions):
                if st.button(
                    suggestion,
                    key=f"suggestion_{i}",
                    help="이 주제를 선택합니다.",
                ):
                    st.session_state.selected_text = suggestion
                    st.session_state.topic_details = get_topic_details(suggestion)

    with col2:
        if st.session_state.selected_text:
            st.markdown('<div class="sub-title">선택한 주제</div>', unsafe_allow_html=True)
            st.markdown(
                f"<div class='content-box'><strong>{st.session_state.selected_text}</strong></div>",
                unsafe_allow_html=True,
            )

            details = st.session_state.topic_details

            # Quill 에디터로 내용 표시
            content = st_quill(value=details, key="editor", html=False)
            if content:
                st.session_state.editor_content = content

            # 복사 버튼 생성
            if st.button("복사"):
                try:
                    pyperclip.copy(st.session_state.editor_content)
                    st.success("내용이 클립보드에 복사되었습니다.")
                except pyperclip.PyperclipException as e:
                    st.error(f"복사 실패: {str(e)}")

if __name__ == "__main__":
    st.set_page_config(
        page_title="디지털 리터러시 with AI",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    sidebar()
    main()
