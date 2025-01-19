import streamlit as st
from streamlit_quill import st_quill
from dotenv import load_dotenv
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

    # 복사 버튼 생성 (HTML + JavaScript)
    st.subheader("복사 기능")
    st.text_area("복사할 내용", st.session_state.editor_content, height=200, key="copy_area")

    st.markdown(
        f"""
        <button onclick="navigator.clipboard.writeText(`{st.session_state.editor_content}`)"
        style="
            background-color: #0055AA;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        ">
            복사
        </button>
        <p id="copy-result" style="color: green; margin-top: 10px;"></p>
        <script>
            const copyButton = document.querySelector('button');
            copyButton.addEventListener('click', () => {{
                const resultText = document.getElementById('copy-result');
                resultText.textContent = "내용이 클립보드에 복사되었습니다!";
                setTimeout(() => {{
                    resultText.textContent = "";
                }}, 3000);
            }});
        </script>
        """,
        unsafe_allow_html=True,
    )

if __name__ == "__main__":
    st.set_page_config(
        page_title="디지털 리터러시 with AI",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    sidebar()
    main()


