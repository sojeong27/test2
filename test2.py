import streamlit as st
from streamlit_quill import st_quill
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


def generate_pdf(content):
    """
    Generate a PDF file from the provided content.
    """
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    c.drawString(100, 750, "출력 내용")
    lines = content.split("\n")
    y = 730
    for line in lines:
        c.drawString(100, y, line)
        y -= 20
        if y < 50:  # Add a new page if content exceeds the current page
            c.showPage()
            y = 750
    c.save()
    buffer.seek(0)
    return buffer


def sidebar():
    """사이드바 설정"""
    st.sidebar.image("images/logo-removebg.png", use_container_width=True)


def main():
    """메인 화면 구성"""
    st.title("디지털 리터러시 with AI")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("자료 탐색")
        input_topic = st.text_input("학습 주제 입력", placeholder="학습 주제를 입력하세요")

        if st.button("주제 생성"):
            if not input_topic.strip():
                st.warning("학습 주제를 입력하세요.")
            else:
                st.session_state.suggestions = [
                    "바람을 통해 씨가 퍼지는 식물",
                    "물에 의해 씨가 퍼지는 식물",
                    "동물에 의해 씨가 퍼지는 식물",
                    "중력에 의해 씨가 퍼지는 식물",
                    "사람의 도움으로 퍼지는 식물",
                ]
                st.session_state.selected_text = None

        if "suggestions" in st.session_state:
            st.markdown("**추천 주제**")
            for i, suggestion in enumerate(st.session_state.suggestions):
                is_selected = (
                    "selected_text" in st.session_state
                    and st.session_state.selected_text == suggestion
                )

                button_style = (
                    "background-color: #003366; color: white; border: 2px solid #003366; padding: 10px; border-radius: 5px; width: 100%; margin-bottom: 10px;"
                    if is_selected
                    else "background-color: #E6F3FF; color: black; border: 2px solid #003366; padding: 10px; border-radius: 5px; width: 100%; margin-bottom: 10px;"
                )

                if st.button(suggestion, key=f"btn_{i}"):
                    st.session_state.selected_text = suggestion
                    st.session_state.topic_details = f"{suggestion}에 대한 세부 내용이 여기에 표시됩니다."

    with col2:
        if "selected_text" in st.session_state and st.session_state.selected_text:
            st.subheader(f"선택한 주제: {st.session_state.selected_text}")
            details = st.session_state.topic_details

            # Quill 에디터로 내용 표시
            content = st_quill(value=details, key="editor", html=False)
            if content:
                st.session_state.editor_content = content

            # Add "출력" button
            if st.button("출력"):
                pdf_file = generate_pdf(st.session_state.editor_content)
                st.download_button(
                    label="PDF 파일 다운로드",
                    data=pdf_file,
                    file_name="output.pdf",
                    mime="application/pdf",
                )


if __name__ == "__main__":
    st.set_page_config(
        page_title="디지털 리터러시 with AI",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    sidebar()
    main()

