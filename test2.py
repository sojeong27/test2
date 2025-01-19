import streamlit as st
from streamlit_quill import st_quill
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
import os

# 환경 변수 로드
load_dotenv()

# ChatGPT 초기화
llm = ChatOpenAI(model_name="gpt-4", temperature=0)


# ChatGPT로부터 추천 주제 가져오기
def get_chatgpt_suggestions(input_text):
    prompt = f"'{input_text}'와 관련된 5개의 세부 주제를 간결하게 생성해 주세요."
    response = llm.predict(prompt)
    return [line.strip() for line in response.split("\n") if line.strip()][:5]


# 선택된 주제 상세 내용 가져오기
def get_topic_details(selected_text):
    prompt = f"'{selected_text}'에 대해 초등학교 6학년 수준으로 상세히 설명해 주세요."
    response = llm.predict(prompt)
    return response


# 사이드바 디자인
def sidebar():
    st.sidebar.image("images/logo-removebg.png", width=150)
    st.sidebar.markdown(
        """
        <style>
            [data-testid="stSidebar"] {
                background-color: #031924; 
            }
            .sidebar-title {
                font-size: 1.5rem; 
                color: white; 
                text-align: center;
                margin-bottom: 1rem;
            }
        </style>
        <div class="sidebar-title">디지털 리터러시 with AI</div>
        """,
        unsafe_allow_html=True,
    )


# 메인 화면 디자인
def main():
    st.title("자료 탐색")
    st.markdown("AI와 협력을 통해 학습에 필요한 자료를 탐색하고 수집합니다.")

    # 중앙 레이아웃
    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("학습 주제 입력")
        input_topic = st.text_input("학습 주제", placeholder="학습 주제를 입력하세요")

        if st.button("주제 생성"):
            if not input_topic.strip():
                st.warning("학습 주제를 입력하세요.")
            else:
                st.session_state.suggestions = get_chatgpt_suggestions(input_topic)
                st.session_state.selected_text = None

        if "suggestions" in st.session_state:
            st.subheader("추천 주제")
            for i, suggestion in enumerate(st.session_state.suggestions):
                button_style = (
                    "background-color: #003366; color: white;"
                    if st.session_state.get("selected_text") == suggestion
                    else "background-color: #E6F3FF; color: black;"
                )
                if st.button(suggestion, key=f"suggestion_{i}"):
                    st.session_state.selected_text = suggestion
                    st.session_state.topic_details = get_topic_details(suggestion)

    with col2:
        if "selected_text" in st.session_state and st.session_state.selected_text:
            st.subheader(f"선택한 주제: {st.session_state.selected_text}")
            details = st.session_state.topic_details
            content = st_quill(value=details, key="editor", html=False)
            if content:
                st.session_state.editor_content = content


# 실행
if __name__ == "__main__":
    st.set_page_config(
        page_title="디지털 리터러시 with AI",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    sidebar()
    main()
