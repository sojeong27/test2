import streamlit as st
from streamlit_quill import st_quill
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
import os

# Load environment variables
load_dotenv()

# Initialize ChatGPT
llm = ChatOpenAI(model_name="gpt-4", temperature=0)

def get_chatgpt_suggestions(input_text):
    """Generate 5 suggestions using ChatGPT."""
    prompt = f"'{input_text}'와 관련된 5개의 세부 주제를 간결하게 생성해 주세요."
    response = llm.predict(prompt)
    return [line.strip() for line in response.split("\n") if line.strip()][:5]

def get_topic_details(selected_text):
    """Generate detailed explanation for a selected topic."""
    prompt = f"'{selected_text}'에 대해 초등학교 6학년 수준으로 상세히 설명해 주세요."
    response = llm.predict(prompt)
    return response

def sidebar():
    """Render the sidebar."""
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

    # Page layout
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

                # Button styling
                button_style = (
                    "background-color: #003366; color: white; border: 2px solid #003366; padding: 10px; border-radius: 5px; width: 100%; margin-bottom: 10px;"
                    if is_selected
                    else "background-color: #E6F3FF; color: black; border: 2px solid #003366; padding: 10px; border-radius: 5px; width: 100%; margin-bottom: 10px;"
                )

                # HTML button
                if st.button(suggestion, key=f"btn_{i}"):
                    st.session_state.selected_text = suggestion
                    st.session_state.topic_details = get_topic_details(suggestion)

    with col2:
        if "selected_text" in st.session_state and st.session_state.selected_text:
            st.subheader(f"선택한 주제: {st.session_state.selected_text}")
            details = st.session_state.topic_details

            # Quill editor for content
            content = st_quill(value=details, key="editor", html=False)
            if content:
                st.session_state.editor_content = content

            # Output button
            if st.button("출력"):
                st.download_button(
                    label="다운로드",
                    data=st.session_state.editor_content,
                    file_name="output.txt",
                    mime="text/plain",
                )

if __name__ == "__main__":
    st.set_page_config(
        page_title="디지털 리터러시 with AI",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    sidebar()
    main()

