import streamlit as st
from streamlit_quill import st_quill
from dotenv import load_dotenv
import pyperclip
import os

# 환경 변수 로드
load_dotenv()

# 상태 초기화
if "editor_content" not in st.session_state:
    st.session_state.editor_content = "복사할 내용을 여기에 생성합니다."

def sidebar():
    """사이드바 렌더링"""
    st.sidebar.title("디지털 리터러시 with AI")
    st.sidebar.markdown("사이드바 내용")
    st.sidebar.image(
        "images/logo-removebg.png",
        use_container_width=True,
        caption="AI 디지털 리터러시",
    )

def main():
    st.title("디지털 리터러시 with AI")

    # 텍스트 편집기 영역
    st.subheader("편집 가능한 내용")
    content = st_quill(value=st.session_state.editor_content, key="editor", html=False)
    if content:
        st.session_state.editor_content = content

    # 복사 기능
    st.subheader("복사 기능")
    st.text_area("복사할 내용", st.session_state.editor_content, height=200, key="copy_area")

    if st.button("복사"):
        try:
            pyperclip.copy(st.session_state.editor_content)
            st.success("내용이 클립보드에 복사되었습니다!")
        except pyperclip.PyperclipException:
            st.error("복사 실패: 클립보드 접근 권한이 없습니다.")

if __name__ == "__main__":
    st.set_page_config(
        page_title="디지털 리터러시 with AI",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    sidebar()
    main()

