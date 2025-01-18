import streamlit as st
from pyparsing import empty
from streamlit_extras.add_vertical_space import add_vertical_space
from streamlit_quill import st_quill


def sidebar():
    st.markdown(
        """
        <style>
            [data-testid="stSidebar"] {
                background-color: #031924; /* 사이드바 배경색 */
            }
            /* Removed the conflicting rule */
            .css-1d391kg {
                background-color: #ffffff; /* 사이드바 확장 버튼 배경색 */
            }
            .css-1d391kg:hover {
                background-color: #f0f2f6; /* 사이드바 확장 버튼 호버 시 배경색 */
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # 커스텀 CSS 스타일 적용
    st.markdown(
        """
    <style>
        /* 사이드바 전체 스타일 */
        [data-testid="stSidebar"] {
            width: 100%;
        }
        
        /* 사이드바 내 컬럼 스타일 */
        [data-testid="stSidebar"] [data-testid="column"] {
            width: 100% !important;
            padding: 0 !important;
        }
        
        /* info 박스 스타일링 */
        [data-testid="stSidebar"] .stAlert {
            background-color: #031924; /* info 박스 배경색 */
            width: 100%;
            padding: 10px 0;
            text-align: center;
            margin: 0;
        }
        
        /* info 박스 내부 텍스트 스타일링 */
        [data-testid="stSidebar"] .stAlert > div {
            color: #e6f3ff !important; /* 텍스트 색상 */
            font-weight: bold;
        }
    </style>
    """,
        unsafe_allow_html=True,
    )

    st.sidebar.image("images/logo-removebg.png", width=128, use_container_width=True)

    # 현재 페이지 상태 초기화
    if "current_page" not in st.session_state:
        st.session_state.current_page = "디지털 리터러시 with AI"  # 기본 페이지

    # 버튼 생성
    buttons = [
        "📊 주제 탐색",
        "📝 자료 탐색",
        "📓 자료 분석",
        "🔍 자료 평가",
        "🤝 결과 공유",
        "📄 매뉴얼",
        "❔ FAQ",
    ]

    for i, button_text in enumerate(buttons):
        st.markdown(
            f"""
            <style>
            .element-container:has(style){{
                display: none;
            }}
            #button-option{i} {{
                display: none;
            }}
            .element-container:has(#button-option{i}) {{
                display: none;
            }}
            .element-container:has(#button-option{i}) + div button {{
                background-color: #031924;
                color: #e6f3ff;
                width: 100%;
                margin: 1px 0;
                padding: 5px;
                border-radius: 5px;
                text-align: left;
            }}
            .element-container:has(#button-option{i}) + div button:hover {{
                background-color: #052e3d;
            }}
            </style>
            """,
            unsafe_allow_html=True,
        )

        # 버튼 생성 및 페이지 상태 업데이트
        st.sidebar.markdown(
            f'<span id="button-option{i}"></span>', unsafe_allow_html=True
        )
        if st.sidebar.button(button_text, key=f"option_{i}"):
            st.session_state.current_page = button_text

    # Create columns for buttons and space
    col1, col2, col3 = st.sidebar.columns(
        [1, 0.2, 1]
    )  # Adjust the middle column width for space
    empty()

    st.markdown(
        """
        <style>
        .element-container:has(style){
            display: none;
        }
        #button-manual {
            display: none;
        }
        .element-container:has(#button-manual) {
            display: none;
        }
        .element-container:has(#button-manual) + div button {
            background-color: #031924;
            color: #e6f3ff;  /* 텍스트 색상을 흰색으로 설정 */
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <style>
        .element-container:has(style){
            display: none;
        }
        #button-logout {
            display: none;
        }
        .element-container:has(#button-logout) {
            display: none;
        }
        .element-container:has(#button-logout) + div button {
            background-color: #031924;
            color: #e6f3ff;  /* 텍스트 색상을 흰색으로 설정 */
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def main(mainCenter):
    with mainCenter:
        # 현재 선택된 페이지에 따라 다른 내용 표시
        if st.session_state.current_page == "📝 자료 탐색":
            st.subheader("자료 탐색")
            st.write("AI와 협력을 통해 학습에 필요한 자료를 탐색하고 수집합니다.")
            with center:
                st.markdown(
                    """
                    <style>
                    .vertical-line {
                        border-left: 2px solid #F0F0F0;  /* 세로 줄 색상 및 두께 */
                        height: 70vh;  /* 화면 전체 높이 */
                        margin: 0 auto;  /* 중앙 정렬 */
                    }
                    </style>
                    <div class="vertical-line"></div>
                    """,
                    unsafe_allow_html=True,
                )

            # Create columns within keywordSection
            (
                keywordSection_recommandKeyword,
                keywordSection_selectionSubject,
                keywordSection_UserInput,
            ) = keywordSection.columns([0.2, 0.3, 0.5])

            keywordSection_recommandKeyword.write("학습 주제")
            keywordSection_selectionSubject.selectbox(
                "교과선택",
                ["전체분야", "국어", "수학", "영어", "과학", "사회"],
                label_visibility="collapsed",
            )
            keywordSection_UserInput.text_input(
                "학습 주제 입력",
                placeholder="학습 주제를 입력하세요",
                label_visibility="collapsed",
            )

            add_vertical_space(1)

            # 단일 선택을 위한 세션 스테이트 초기화 (여러 개가 아닌 하나의 문자열만 저장)
            if "selected_text" not in st.session_state:
                st.session_state.selected_text = None

            # 스타일 정의
            keywordSection.markdown(
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

            # 버튼 생성 로직
            texts = [
                "바람을 통해 씨가 퍼지는 식물",
                "물에 의해 씨가 퍼지는 식물",
                "동물에 의해 씨가 퍼지는 식물",
                "중력에 의해 씨가 퍼지는 식물",
                "사람의 도움으로 퍼지는 식물",
            ]

            # 단일 선택을 위한 세션 스테이트 초기화
            if "selected_text" not in st.session_state:
                st.session_state.selected_text = None

            # 버튼 생성
            for i, text in enumerate(texts):
                is_selected = text == st.session_state.selected_text
                button_label = f"**{text}**" if is_selected else text

                # 버튼 생성
                keywordSection.markdown(
                    '<span id="keyword-button"></span>', unsafe_allow_html=True
                )
                if keywordSection.button(
                    button_label,
                    key=f"text_{i}",
                    help=None,  # 툴팁 제거
                    on_click=None,  # 클릭 시 콜백 함수 (필요 시 추가)
                ):
                    if text == st.session_state.selected_text:
                        st.session_state.selected_text = None  # 선택 해제
                    else:
                        st.session_state.selected_text = text  # 선택 설정
                    st.rerun()  # 상태 변경 후 페이지 리프레시

                # 선택된 버튼의 스타일 적용
                if is_selected:
                    keywordSection.markdown(
                        f"""
                        <style>
                        .element-container:has(#keyword-button) + div button[key="text_{i}"] {{
                            background-color: #003366 !important; /* 선택된 버튼 배경색 */
                            border-color: #003366 !important; /* 선택된 버튼 테두리 색상 */
                            color: #0047AB !important; /* 선택된 버튼 텍스트 색상 */
                            font-weight: bold; /* 텍스트 굵게 */
                        }}
                        </style>
                        """,
                        unsafe_allow_html=True,
                    )

            # 선택된 텍스트 표시
            if st.session_state.selected_text:
                documentSection.markdown(st.session_state.selected_text)

                if "editor_content" not in st.session_state:
                    st.session_state.editor_content = """
                    1. 바람을 통해 씨가 퍼지는 식물의 특징 
                    바람으로 씨앗이 퍼지는 식물들은 다음과 같은 특징을 가집니다:
                    씨앗이 가볍고 작은 크기.
                    씨앗에 날개나 털 같은 구조가 있어 공기 중에서 오래 떠다닐 수 있음.
                    바람이 잘 통하는 개방된 장소에서 씨앗을 떨어뜨림.

                    2. 바람으로 씨앗이 퍼지는 대표적인 식물
                    1) 민들레
                    특징: 씨앗에 솜털이 달려 있어 바람에 의해 멀리 날아감.
                    주변 환경: 넓은 초원이나 공원처럼 바람이 잘 부는 곳.
                    특이점: 씨앗이 가벼워 작은 바람에도 쉽게 멀리 퍼질 수 있음.
                    2) 단풍나무
                    특징: 씨앗에 프로펠러 모양의 날개가 달려 있어 떨어질 때 회전하며 멀리 날아감.
                    주변 환경: 숲이나 공원.
                    특이점: 바람이 부는 방향으로 멀리 이동할 수 있음.
                    """

                with documentSection:

                    content = st_quill(
                        value=st.session_state.editor_content,
                        html=True,
                        key="quill_editor",
                    )

                    (
                        documentSection_col1,
                        documentSection_col2,
                        documentSection_col3,
                        documentSection_col4,
                    ) = documentSection.columns(
                        [0.2, 0.2, 0.4, 0.2]
                    )  # 컬럼 분할
                    with documentSection_col2:
                        # CSS 스타일 정의
                        st.markdown(
                            """
                            <style>
                            /* 기본 버튼 스타일 (회색) */
                            .stButton button[kind="secondary"] {
                                background-color: #E0E0E0;
                                color: #31333F;
                                border: none;
                                with: 100%;
                            }
                            
                            /* 선택된 버튼 스타일 (파란색) */
                            .stButton button[kind="primary"] {
                                background-color: #0047AB;
                                color: white;
                                border: none;
                                with: 100%;
                            }
                            </style>
                        """,
                            unsafe_allow_html=True,
                        )

                        # 현재 모드에 따라 버튼 스타일 설정
                        current_mode = st.session_state.get("mode", "기본")
                        심화_style = (
                            "primary" if current_mode == "심화" else "secondary"
                        )
                        기본_style = (
                            "primary" if current_mode == "기본" else "secondary"
                        )

                        if documentSection_col1.button("심화", type=심화_style):
                            st.session_state.mode = "심화"
                            st.rerun()
                        if documentSection_col2.button("기본", type=기본_style):
                            st.session_state.mode = "기본"
                            st.rerun()

                    # 보고서 생성과 출력 버튼을 위한 CSS 스타일 추가
                    documentSection_col3.markdown(
                        """
                        <style>
                        .element-container:has(style){
                            display: none;
                        }
                        #create-reports {
                            display: none;
                        }
                        .element-container:has(#create-reports) {
                            display: none;
                        }
                        .element-container:has(#create-reports) + div button {
                            background-color: #031924;
                            color: #e6f3ff;  /* 텍스트 색상을 흰색으로 설정 */
                            width: 100%;
                            }
                        </style>
                        """,
                        unsafe_allow_html=True,
                    )

                    documentSection_col4.markdown(
                        """
                        <style>
                        .element-container:has(style){
                            display: none;
                        }
                        #print {
                            display: none;
                        }
                        .element-container:has(#print) {
                            display: none;
                        }
                        .element-container:has(#print) + div button {
                            background-color: #031924;
                            color: #e6f3ff;  /* 텍스트 색상을 흰색으로 설정 */
                            width: 100%;
                            }
                        </style>
                        """,
                        unsafe_allow_html=True,
                    )

                    documentSection_col3.markdown(
                        '<span id="create-reports"></span>', unsafe_allow_html=True
                    )
                    if documentSection_col3.button("보고서 생성"):
                        documentSection.write("보고서 생성 버튼이 클릭되었습니다.")
                    documentSection_col4.markdown(
                        '<span id="print"></span>', unsafe_allow_html=True
                    )
                    if documentSection_col4.button("출력"):
                        documentSection.write("출력 버튼이 클릭되었습니다.")

            add_vertical_space(1)
        elif st.session_state.current_page == "📊 NOK AI":
            st.subheader("NOK AI")
            st.write("NOK AI 페이지 내용")
        elif st.session_state.current_page == "📓 내 노트":
            st.subheader("내 노트")
            st.write("내 노트 페이지 내용")


def setting(mainCenter):
    sidebar()
    main(mainCenter)


if __name__ == "__main__":
    st.set_page_config(
        page_title="NOK(Research report)",  # Set page title
        page_icon="🔎",  # Set page icon
        layout="wide",  # Set layout to wide
        initial_sidebar_state="expanded",  # Set sidebar to expanded
    )

    leftMargin, mainCenter, rightMargin = st.columns([0.01, 1.0, 0.01])
    leftMargin, keywordSection, center, documentSection, rightMargin = st.columns(
        [0.05, 0.7, 0.05, 0.6, 0.1]
    )

    setting(mainCenter)
