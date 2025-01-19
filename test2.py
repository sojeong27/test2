import streamlit as st
from streamlit_quill import st_quill
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
import os

# Load environment variables
load_dotenv()

# Initialize ChatGPT model
llm = ChatOpenAI(model_name="gpt-4o", temperature=0)


def get_chatgpt_suggestions(input_text):
    """Generate suggestions using ChatGPT."""
    prompt = f"'{input_text}'에 대한 관련된 5개의 세부 주제를 생성해 주세요."
    response = llm.predict(prompt)
    return list(set(response.split("\n")[:5]))  # 중복 제거 후 상위 5개


def get_topic_details(selected_text):
    """Provide detailed explanation for a selected topic using ChatGPT."""
    prompt = f"'{selected_text}'에 대해 초등학교 6학년 수준으로 상세히 설명해 주세요."
    response = llm.predict(prompt)
    return response


def sidebar():
    st.markdown(
        """
        <style>
            [data-testid="stSidebar"] {
                background-color: #031924; /* 사이드바 배경색 */
                padding-top: 10px;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.sidebar.image("images/logo-removebg.png", width=128, use_container_width=True)


def main():
    st.title("디지털 리터러시 with AI")

    col1, col2 = st.columns([1, 1])  # 1:1 화면 분할

    with col1:
        st.subheader("자료 탐색")
        input_topic = st.text_input(
            "학습 주제 입력", placeholder="학습 주제를 입력하세요"
        )

        if st.button("주제 생성"):
            if not input_topic.strip():
                st.warning("학습 주제를 입력하세요.")
            else:
                st.session_state.suggestions = get_chatgpt_suggestions(input_topic)
                st.session_state.selected_text = None

        if "suggestions" in st.session_state:
            st.markdown("**추천 주제**")

            st.markdown(
                """
                <style>
                .element-container:has(style) {
                    display: none;
                }
                #keyword-button {
                    display: none;
                }
                .element-container:has(#keyword-button) + div button {
                    display: block !important;
                    background-color: #E6F3FF !important; /* 기본 배경색 */
                    color: black !important; /* 기본 텍스트 색상 */
                    border: 3px solid #003366 !important; /* 기본 테두리 색상 */
                    padding: 10px !important;
                    margin: 2px 0 !important;
                    font-size: 18px !important;
                    text-align: left !important;
                    width: 100% !important;
                    white-space: normal !important;
                    border-radius: 4px !important;
                    height: auto !important;
                    min-height: 0 !important;
                    transition: background-color 0.3s, color 0.3s; /* 부드러운 전환 효과 */
                }
                .element-container:has(#keyword-button) + div button:hover {
                    background-color: #CCE5FF !important; /* 호버 시 배경색 */
                    border-color: #003366 !important; /* 호버 시 테두리 색상 */
                }
                .element-container:has(#keyword-button) + div button.selected-button {
                    background-color: #003366 !important; /* 선택된 버튼 배경색 */
                    border-color: #003366 !important; /* 선택된 버튼 테두리 색상 */
                    color: #0047AB !important; /* 선택된 버튼 텍스트 색상 */
                    font-weight: bold; /* 텍스트 굵게 */
                }
                </style>
                """,
                unsafe_allow_html=True,
            )

            for i, suggestion in enumerate(st.session_state.suggestions):
                if st.button(suggestion, key=f"suggestion_{i}"):
                    st.session_state.selected_text = suggestion

    with col2:
        if "selected_text" in st.session_state and st.session_state.selected_text:
            st.subheader(f"선택한 주제: {st.session_state.selected_text}")
            if "topic_details" not in st.session_state:
                st.session_state.topic_details = get_topic_details(
                    st.session_state.selected_text
                )

            details = st.session_state.topic_details

            if "editor_content" not in st.session_state:
                st.session_state.editor_content = details

            content = st_quill(
                value=st.session_state.editor_content, key="editor", html=False
            )

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
