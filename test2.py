import streamlit as st
from streamlit.components.v1 import html

# Streamlit 상태 초기화
if "selected_button" not in st.session_state:
    st.session_state.selected_button = None

# 추천 주제 리스트
topics = [
    "식물의 씨앗 퍼뜨리기: 바람을 이용하는 전략",
    "동물에 의한 식물 씨앗의 전파 방법",
    "식물이 씨앗을 퍼뜨리기 위해 사용하는 물의 역할",
    "인간에 의해 퍼져가는 식물 씨앗의 이동 방식",
    "자기 자신 퍼뜨리기: 식물이 씨앗을 퍼뜨리는 독특한 방법"
]

# 버튼 스타일 CSS 정의
st.markdown(
    """
    <style>
    .custom-button {
        background-color: #E6F3FF;
        color: black;
        border: 2px solid #003366;
        border-radius: 5px;
        padding: 10px;
        text-align: left;
        width: 100%;
        margin: 5px 0;
        font-size: 16px;
        cursor: pointer;
    }
    .custom-button:hover {
        background-color: #CCE5FF;
    }
    .selected-button {
        background-color: #003366;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# HTML 버튼 생성
def create_buttons():
    buttons_html = ""
    for i, topic in enumerate(topics):
        # 버튼 스타일: 선택된 버튼은 다른 스타일 적용
        button_class = (
            "custom-button selected-button"
            if st.session_state.selected_button == i
            else "custom-button"
        )
        # 각 버튼에 대해 HTML 작성
        buttons_html += f"""
        <button class=\"{button_class}\" onclick=\"handleClick({i})\">{topic}</button>
        """
    # JavaScript 코드와 버튼 HTML 삽입
    st.markdown(
        f"""
        <div>
            {buttons_html}
        </div>
        <script>
        function handleClick(index) {{
            // Streamlit에 버튼 클릭 정보를 전달
            window.parent.postMessage({{index: index}}, "*");
        }}
        </script>
        """,
        unsafe_allow_html=True,
    )

# 버튼 클릭 이벤트 처리
def handle_click_event():
    clicked_index = st.session_state.get("clicked_index", None)
    if clicked_index is not None:
        st.session_state.selected_button = clicked_index
        st.session_state.clicked_index = None  # 상태 초기화

# HTML에서 전달된 클릭 정보를 수신하는 JavaScript
html("""
<script>
window.addEventListener('message', (event) => {
    const index = event.data.index;
    if (index !== undefined) {
        Streamlit.setComponentValue(index);
    }
});
</script>
""", height=0)

# 버튼 생성 및 이벤트 처리
create_buttons()
handle_click_event()

# 선택된 주제 내용 표시
if st.session_state.selected_button is not None:
    selected_topic = topics[st.session_state.selected_button]
    st.subheader(f"선택한 주제: {selected_topic}")
    st.text_area("내용", f"{selected_topic}에 대한 설명을 입력하세요.", height=200)


