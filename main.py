import streamlit as st
from pyparsing import empty
from streamlit_extras.add_vertical_space import add_vertical_space
from streamlit_quill import st_quill


def sidebar():            
    st.markdown("""
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
        """, unsafe_allow_html=True)
    
    # 커스텀 CSS 스타일 적용
    st.markdown("""
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
    """, unsafe_allow_html=True)
    
    st.sidebar.image("images/logo-removebg.png", width=128, use_container_width =True)

    sidebar_col1, sidebar_col2 = st.sidebar.columns(2)    
    sidebar_col1.info("👋 강지원 님")
    sidebar_col2.info("👤 알림")

        # 현재 페이지 상태 초기화
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "Research Report"  # 기본 페이지

    # 버튼 생성
    buttons = ["📊 NOK AI", 
            "📝 Research Report", 
            "📓 내 노트", 
            "🤝 공유 노트", 
            "👨‍🎓 학생 관리", 
            "🔍 탐구 라브러리", 
            "📄 문서 서식", 
            "❔ FAQ"
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
        st.sidebar.markdown(f'<span id="button-option{i}"></span>', unsafe_allow_html=True)
        if st.sidebar.button(button_text, key=f"option_{i}"):
            st.session_state.current_page = button_text
    
    

    

    
    
    
        
    # Create columns for buttons and space
    col1, col2, col3 = st.sidebar.columns([1, 0.2, 1])  # Adjust the middle column width for space    
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

    col1.markdown('<span id="button-manual"></span>', unsafe_allow_html=True)
    col1.button("메뉴얼")
    
    col2.markdown("&nbsp;", unsafe_allow_html=True)
    
    col3.markdown('<span id="button-logout"></span>', unsafe_allow_html=True)
    col3.button("로그아웃", key="로그아웃")
    


def main(mainCenter):    
    with mainCenter:
        # 현재 선택된 페이지에 따라 다른 내용 표시
        if st.session_state.current_page == "📝 Research Report":
            st.subheader("Research Report")    
            st.write("수업, 진료설계에 도움이 되는 주제와 보고서를 생성합니다.")
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
                    unsafe_allow_html=True
                )
            
            # Create columns within keywordSection
            keywordSection_recommandKeyword, keywordSection_selectionSubject, keywordSection_UserInput = keywordSection.columns([0.2, 0.3, 0.5]) 
            
            keywordSection_recommandKeyword.write("추천 키워드")
            keywordSection_selectionSubject.selectbox("교과선택", ["전체분야", "국어", "수학", "영어", "과학", "사회"], label_visibility="collapsed")
            keywordSection_UserInput.text_input("키워드 입력", placeholder="키워드를 입력하세요", label_visibility="collapsed")
            
            add_vertical_space(1)            
            
            # 단일 선택을 위한 세션 스테이트 초기화 (여러 개가 아닌 하나의 문자열만 저장)
            if 'selected_text' not in st.session_state:
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
                "단백질 구조와 그 기능에 미치는 영향 분석",
                "단백질 구조 예측을 위한 컴퓨터 알고리즘 분석과 비교",
                "단백질 구조의 변화가 없긴 건강에 미치는 영향",
                "단백질 구조와 그 기능간의 상호작용에 대한 연구",
                "단백질 구조의 3차원 모델링과 그 기능에 대한 연구"
            ]

            # 단일 선택을 위한 세션 스테이트 초기화
            if 'selected_text' not in st.session_state:
                st.session_state.selected_text = None

            # 버튼 생성
            for i, text in enumerate(texts):
                is_selected = text == st.session_state.selected_text
                button_label = f"**{text}**" if is_selected else text

                # 버튼 생성
                keywordSection.markdown('<span id="keyword-button"></span>', unsafe_allow_html=True)
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
                        unsafe_allow_html=True
                    )
                    
            # 선택된 텍스트 표시
            if st.session_state.selected_text:
                documentSection.markdown(st.session_state.selected_text)

                if 'editor_content' not in st.session_state:
                    st.session_state.editor_content = '''
                    1. 서론</Bold>

                    1.1 연구배경 및 목적
                    단백질은 생명체내에서 효소작용, 신호 전달, 면역 반응 물질 운반 등 다양한 필수적인 기능을 수행하는 고분 단백질의 고유한 3차원 구조는 이러한 기능 수행에 직접적인 영 자입니다
                    향을 미치며 구조의 변화는 기능 이상 발생과 밀접하게 연관되어 있습니다. 알츠하이머 파킨슨병과 같은 신경성 질환, 입, 남포성 섬유증, 경상적혈구빈 등 심각한 질환들이 단백 구조 이상과 연관되어 있다는 연구 결과들이 보고되고 있습니다. 따라서 본 연구는 단백질 구조 변화 예거니즘을 심층적으로 이해하고, 이를 통해 질병 발생 기전을 규명하여 질병 예방 및 치료 가능성을 색하고자 합니다. 궁극적으로는 단백질 구조 변화에 대한 이해를 바탕으로 인류 건강 증진에 기여 하는 것을 목표로 합니다.

                    1.2 단백질 구조의 중요성
                    단백질의 기능은 그 구조와 밀접하게 연관되어 있습니다. 단백질은 20가지 종류의 아미노산이다 이드 결합으로 연결된 폴리펩타이드사로 구성됩니다. 이 다이드 사슴은 고유한 방식으로 접혀서 특정한 3차원 구조를 형성하는데, 이 구조가 단백질의 기능을 결정합니다. 단백질 구조는 1차 구조아미노산 서열 2차 구조나 구조 3차 구조(단백질체인 3차원 구조 그 리고 4차 구조(여러 폴리라이드 사슴의 결합)로 구분됩니다. 각 단계의 구조는 단백질의 안정성과 기능에 중요한 역할을 합니다. 한약 단백질 구조가 성적으로 유지되지않으면, 효소 활씀하신
                    기본
                    보고서 생성
                    '''

                
                with documentSection:
                    
                    content = st_quill(
                        value=st.session_state.editor_content,
                        html=True,
                        key='quill_editor'
                    )
                                        
                    documentSection_col1, documentSection_col2, documentSection_col3, documentSection_col4 = documentSection.columns([0.2, 0.2, 0.4, 0.2])  # 컬럼 분할
                    with documentSection_col2:
                        # CSS 스타일 정의
                        st.markdown("""
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
                        """, unsafe_allow_html=True)
                        
                        # 현재 모드에 따라 버튼 스타일 설정
                        current_mode = st.session_state.get('mode', '기본')
                        심화_style = "primary" if current_mode == "심화" else "secondary"
                        기본_style = "primary" if current_mode == "기본" else "secondary"
                        
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
                    
                    documentSection_col3.markdown('<span id="create-reports"></span>', unsafe_allow_html=True)
                    if documentSection_col3.button("보고서 생성"):
                        documentSection.write("보고서 생성 버튼이 클릭되었습니다.")
                    documentSection_col4.markdown('<span id="print"></span>', unsafe_allow_html=True)
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
    
    



if __name__ == '__main__':
    st.set_page_config(
        page_title="NOK(Research report)",  # Set page title
        page_icon="🔎",  # Set page icon
        layout="wide",  # Set layout to wide
        initial_sidebar_state="expanded",  # Set sidebar to expanded
    )
    
    leftMargin, mainCenter, rightMargin = st.columns([0.01, 1.0, 0.01])         
    leftMargin, keywordSection, center, documentSection, rightMargin = st.columns([0.05, 0.7,  0.05,  0.6, 0.1])             
    
    setting(mainCenter)