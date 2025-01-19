import streamlit as st
from streamlit_quill import st_quill
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
import os

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
                background-color: #031924;
                padding-top: 20px;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )
    st.sidebar.image("images/logo-removebg.png", use_container_width=True)

def main():
    st.title("디지털 리터러시 with AI")

    # 화면 분할
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("자료 탐색")
        input_topic = st.text_input("학습 주제 입력", placeholder="학습 주제를 입력하세요")

        if st.button("주제 생성"):
            if not input_topic.strip():
                st.warning("학습 주제를 입력하세요.")
            else:
                st.session_state.suggestions = get_chatgpt_suggestions(input_topic)
                st.session_state.selected_text = None

        if "suggestions" in st.session_state:
            st.markdown("**추천 주제**")
            for i, suggestion in enumerate(st.session_state.suggestions):
                is_selected = (
                    "selected_text" in st.session_state
                    and st.session_state.selected_text == suggestion
                )

                # 버튼 스타일 적용
                button_style = (
                    "background-color: #003366; color: white;"
                    if is_selected
                    else "background-color: #E6F3FF; color: black;"
                )

                # Streamlit 버튼으로 생성
                if st.button(suggestion, key=f"btn_{i}"):
                    st.session_state.selected_text = suggestion
                    st.session_state.topic_details = get_topic_details(suggestion)

    with col2:
        if "selected_text" in st.session_state and st.session_state.selected_text:
            st.subheader(f"선택한 주제: {st.session_state.selected_text}")
            details = st.session_state.topic_details

            # Quill 에디터로 내용 표시
            content = st_quill(value=details, key="editor", html=False)
            if content:
                st.session_state.editor_content = content

if __name__ == "__main__":
    st.set_page_config(
        page_title="디지털 리터러시 with AI",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    sidebar()
    main()


