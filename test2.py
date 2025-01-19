import streamlit as st
from streamlit_quill import st_quill
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
import os
import clipboard  # 클립보드 복사 라이브러리

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
    st.sidebar.title("디지털 리터러시 with AI")
    st.sidebar.info("AI를 활용한 학습 주제 탐색")


def main():
    st.title("디지털 리터러시 with AI")

    # 상태 초기화
    if "suggestions" not in st.session_state:
        st.session_state.suggestions = []
    if "selected_text" not in st.session_state:
        st.session_state.selected_text = None
    if "topic_details" not in st.session_state:
        st.session_state.topic_details = ""

    # 입력창과 버튼
    input_topic = st.text_input("학습 주제 입력", placeholder="학습 주제를 입력하세요")
    if st.button("주제 생성"):
        if not input_topic.strip():
            st.warning("학습 주제를 입력하세요.")
        else:
            st.session_state.suggestions = get_chatgpt_suggestions(input_topic)
            st.session_state.selected_text = None

    # 추천 주제 버튼
    if st.session_state.suggestions:
        st.subheader("추천 주제")
        for i, suggestion in enumerate(st.session_state.suggestions):
            if st.button(suggestion, key=f"suggestion_{i}"):
                st.session_state.selected_text = suggestion
                st.session_state.topic_details = get_topic_details(suggestion)

    # 선택된 주제 내용 표시
    if st.session_state.selected_text:
        st.subheader(f"선택한 주제: {st.session_state.selected_text}")
        details = st.session_state.topic_details
        content = st_quill(value=details, key="editor", html=False)

        if content:
            st.session_state.editor_content = content

        # 복사 버튼 생성
        if st.button("복사"):
            try:
                # clipboard 라이브러리를 사용해 내용 복사
                clipboard.copy(st.session_state.editor_content)
                st.success("내용이 클립보드에 복사되었습니다!")
            except Exception as e:
                st.error(f"복사 실패: {str(e)}")


if __name__ == "__main__":
    st.set_page_config(
        page_title="디지털 리터러시 with AI",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    sidebar()
    main()

