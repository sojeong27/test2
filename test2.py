# -*- coding: utf-8 -*-
import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space
from streamlit_quill import st_quill


# 기존 임포트 아래에 추가
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
from functools import lru_cache
import pyperclip
import os

# API KEY 정보로드
load_dotenv()

llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)

def create_prompt(selected_subject, keyword):
    prompt_template = f"""
    당신은 {selected_subject} 교과목 전문가입니다. 사용자가 입력한 키워드 '{keyword}'와 관련된 연구 주제를 5가지 생성해주세요.
    각 주제는 {selected_subject} 교과목과 관련되어야 하며, 학문적으로 유의미하고 구체적이어야 합니다.
    주제는 번호 없이 쉼표로 구분된 문자열로 반환해주세요.

    예시:
    단백질 구조와 그 기능에 미치는 영향 분석, 단백질 구조 예측을 위한 컴퓨터 알고리즘 분석과 비교, 단백질 구조의 변화가 없긴 건강에 미치는 영향, 단백질 구조와 그 기능간의 상호작용에 대한 연구, 단백질 구조의 3차원 모델링과 그 기능에 대한 연구
    """
    return ChatPromptTemplate.from_template(prompt_template)

# 주제 생성 함수
@st.cache_data(max_entries=32)
def generate_topics(selected_subject, keyword):
    prompt = create_prompt(selected_subject, keyword)
    chain = prompt | llm | StrOutputParser()
    response = chain.invoke({"keyword": keyword})
    return response.split(", ")


@st.cache_data(max_entries=32)
def generate_report(selected_subject, topic):
    prompt = create_report_prompt(selected_subject, topic)
    # Build a simple chain: prompt | llm | output parser
    chain = prompt | llm | StrOutputParser()
    response = chain.invoke({"topic": topic})
    return response

@st.cache_data(max_entries=32)
def create_report_prompt(selected_subject, topic):
    prompt_template = f"""
다음의 과목{selected_subject}의 주제 "{topic}" 및 편집기에 입력된 내용을 바탕으로, 아래의 보고서 형식에 맞는 연구 보고서를 작성해 주세요.

[보고서 형식]
1. 서론 </bold>
1.1 연구 배경 및 목적  
단백질은 생명체에서 효소 작용, 신호 전달, 면역 반응 물질 운반 등 다양한 필수 기능을 수행하는 고분자 단백질의 고유한 3차원 구조를 가지고 있습니다. 이 구조의 변화는 기능 이상과 밀접하게 관련되어 있으며, 알츠하이머, 파킨슨병 등의 신경계 질환과 관련된 단백질 구조 이상에 대한 연구가 보고되고 있습니다. 따라서 본 연구는 단백질 구조 변화를 심층적으로 이해하고, 질병 발생 메커니즘을 규명하여 질병 예방 및 치료 가능성을 모색하는 것을 목적으로 합니다. 궁극적으로 단백질 구조 변화에 대한 이해를 바탕으로 인류 건강 증진에 기여하고자 합니다.

1.2 단백질 구조의 중요성  
단백질의 기능은 그 구조와 밀접하게 관련되어 있습니다. 단백질은 20종류의 아미노산으로 구성된 폴리펩타이드 사슬이 고유하게 접혀 특정 3차원 구조를 형성하며, 이 구조가 단백질의 기능을 결정합니다. 단백질 구조는 1차 구조(아미노산 서열), 2차 구조, 3차 구조(3D 구조), 4차 구조(다중 폴리펩타이드 사슬의 결합)로 구분됩니다. 구조가 유지되지 않으면 단백질의 기능에 이상이 발생할 수 있습니다.

...

위 내용을 바탕으로 보고서를 작성해 주세요.
    """
    return ChatPromptTemplate.from_template(prompt_template)

@st.cache_data(max_entries=32)
def create_summary_prompt(content):
    prompt_template = f"""
    다음은 연구 보고서의 내용입니다. 이 내용을 간결하게 요약해 주세요. 요약은 다음 형식을 따르세요:

    [요약 형식]
    1. 핵심 주제: 보고서의 주요 주제를 한 문장으로 요약하세요.
    2. 주요 내용: 보고서의 핵심 내용을 3~4개의 bullet point로 요약하세요.
    3. 결론: 보고서의 결론 또는 시사점을 간단히 설명하세요.

    [보고서 내용]
    {content}
    """
    return ChatPromptTemplate.from_template(prompt_template)

@st.cache_data(max_entries=32)
def generate_summary(content):
    prompt = create_summary_prompt(content)
    chain = prompt | llm | StrOutputParser()
    response = chain.invoke({"content": content})
    return response

def load_css():
    """CSS 파일들 로드"""
    css_files = ["base", "sidebar", "main"]
    for css_file in css_files:
        with open(f"assets/style_{css_file}.css", encoding='utf-8') as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


import pandas as pd
from fpdf import FPDF
import tempfile
import os

def create_excel_and_convert_to_pdf(content):
    # 임시 파일 경로 생성
    with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp_excel:
        excel_path = tmp_excel.name
    
    # 엑셀 파일 생성
    df = pd.DataFrame({
        "Content": [content]
    })
    with pd.ExcelWriter(excel_path, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Report")
    
    # PDF 파일 생성
    pdf_path = excel_path.replace(".xlsx", ".pdf")
    pdf = FPDF()
    pdf.add_page()
    
    # 현재 디렉토리의 fonts 폴더에서 폰트 찾기
    font_path = os.path.join('fonts', 'YBLO05.TTF')  # 맑은 고딕 폰트
        
    if not os.path.exists(font_path):
        raise Exception("fonts 폴더에서 한글 폰트를 찾을 수 없습니다. malgun.ttf 또는 NanumGothic.ttf 파일이 필요합니다.")
    
    # 폰트 추가
    pdf.add_font("CustomFont", "", font_path, uni=True)
    pdf.set_font("CustomFont", size=12)
    
    # 제목 추가
    pdf.cell(200, 10, txt="Report Content", ln=True, align="C")
    
    # 내용 추가 (한글 지원)
    pdf.multi_cell(0, 10, txt=content)
    
    # PDF 파일 저장
    pdf.output(pdf_path)
    
    return excel_path, pdf_path


def sidebar():
    """사이드바 구성"""
    load_css()
    
    # 로고 이미지
    st.sidebar.image("images/logo-removebg.png", width=128, use_container_width=True)

    # 사용자 정보 표시
    sidebar_col1, sidebar_col, sidebar_col2 = st.sidebar.columns([1.0, 0.2, 1.0]) 

    # 사용자 정보 버튼으로 변경
    sidebar_col1.markdown('<span id="button-user"></span>', unsafe_allow_html=True)
    sidebar_col1.button(
        "👋 강지원 님",
        key="user_button",
        help="사용자 프로필 메뉴",  # 툴팁 추가
        use_container_width=True
    )

    # 알림 버튼 추가
    sidebar_col2.markdown('<span id="button-alert"></span>', unsafe_allow_html=True)
    sidebar_col2.button(
        "👤 알림",
        key="alert_button",
        help="새 알림 확인",  # 툴팁 추가
        use_container_width=True  # <-- 이 부분을 True로
    )


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
        st.sidebar.markdown('<span id="button-manu"></span>', unsafe_allow_html=True)
        if st.sidebar.button(button_text, key=f"option_{i}"):
            st.session_state.current_page = button_text

    # 하단 버튼 그룹
    col1, col2, col3 = st.sidebar.columns([1, 0.2, 1])
    # 수정된 코드
    col1.markdown('<span id="button-manual"></span>', unsafe_allow_html=True)
    col1.button("메뉴얼")
    col3.markdown('<span id="button-logout"></span>', unsafe_allow_html=True)
    col3.button("로그아웃", key="logout", use_container_width=True)

def main_content():
    """메인 콘텐츠 영역"""
    # 레이아웃 컬럼 설정
    left_margin, main_center, right_margin = st.columns([0.01, 1.0, 0.01])
    left_margin, keyword_section, center, document_section, right_margin = st.columns(
        [0.05, 0.7, 0.05, 0.6, 0.1]
    )

    if 'editor_content' not in st.session_state:
        st.session_state.editor_content = ""

    with main_center:
        if st.session_state.current_page == "📝 Research Report":
            st.subheader("Research Report")
            st.write("수업, 진료설계에 도움이 되는 주제와 보고서를 생성합니다.")
            
            # 세로 구분선
            with center:
                st.markdown('<div class="vertical-line"></div>', unsafe_allow_html=True)

            # 키워드 섹션
            with keyword_section:
                keyword_col1, keyword_col2, keyword_col3 = st.columns([0.2, 0.3, 0.5])
                keyword_col1.markdown('<div class="info-cmd">추천 키워드</div>', unsafe_allow_html=True)

                
                keyword_col2.markdown('<span id="selectbox-curriculum"></span>', unsafe_allow_html=True)
                keyword_col2.selectbox(
                    "교과선택", 
                    ["국어", "사회", "과학"], 
                    label_visibility="collapsed",
                    key='selected_subject'
                )
                                
                keyword_col3.text_input(
                    "키워드 입력", 
                    placeholder="키워드를 입력하세요", 
                    label_visibility="collapsed",
                    key='keyword_input'
                )

                add_vertical_space(1)
                
                # 키워드 버튼 생성
                if 'selected_text' not in st.session_state:
                    st.session_state.selected_text = None

                # RAG 결과를 담을 리스트 초기화
                if 'keywords' not in st.session_state:
                    st.session_state.keywords = []
                
                if st.session_state.keyword_input:
                    st.session_state.keywords = generate_topics(st.session_state.selected_subject, st.session_state.keyword_input)

                # keywords = [
                #     "단백질 구조와 그 기능에 미치는 영향 분석",
                #     "단백질 구조 예측을 위한 컴퓨터 알고리즘 분석과 비교",
                #     "단백질 구조의 변화가 없긴 건강에 미치는 영향",
                #     "단백질 구조와 그 기능간의 상호작용에 대한 연구",
                #     "단백질 구조의 3차원 모델링과 그 기능에 대한 연구"
                # ]
                
                if 'keywords' in st.session_state and st.session_state.keywords:
                    for idx, keyword in enumerate(st.session_state.keywords):
                        is_selected = keyword == st.session_state.selected_text
                        if is_selected:
                            st.markdown('<span class="selected-keyword"></span>', unsafe_allow_html=True)
                        else:
                            st.markdown('<span id="keyword-button"></span>', unsafe_allow_html=True)

                        button_label = f"**{keyword}**" if is_selected else keyword
                        
                        # 콜백 함수 추가
                        def select_keyword(keyword):
                            if st.session_state.selected_text == keyword:
                                st.session_state.selected_text = None
                            else:
                                st.session_state.selected_text = keyword

                        # if st.button(button_label, key=f"kw_{idx}", help=None):
                        #     if is_selected:
                        #         st.session_state.selected_text = None
                        #     else:
                        #         st.session_state.selected_text = keyword
    #                        st.rerun()
                        # 버튼 클릭 핸들러
                        if st.button(button_label, 
                                    key=f"kw_{idx}", 
                                    help=None,
                                    # 버튼 클릭 시 부분 리렌더링 방지
                                    on_click=lambda k=keyword: select_keyword(k)):
                            pass
                    

            # 문서 편집기 섹션
            with document_section:
                if st.session_state.selected_text:
                    st.markdown(f'<div class="selected-text">{st.session_state.selected_text}</div>', unsafe_allow_html=True)
                    
                if 'editor_key' not in st.session_state:
                    st.session_state.editor_key = 0
                    
                # 에디터 초기화
                content = st_quill(
                    value=st.session_state.editor_content,
                    html=True,
                    key=f'quill_editor_{st.session_state.editor_key}'  # 동적 키 적용
                )


                # Create three columns to hold the buttons in one row.
                col1, col2, col3, col4, col5, col6 = st.columns([0.2, 0.5, 0.5, 0.5, 0.5, 0.2])

                with col2:
                    # Insert a marker before the button so that we can style it via CSS.
                    st.markdown('<span id="button-summary"></span>', unsafe_allow_html=True)
                    if st.button("생성", key="create_button"):
                        st.session_state.editor_content = generate_report(st.session_state.selected_subject, st.session_state.selected_text)
                        st.session_state.editor_key += 1  # 키 값 변경으로 컴포넌트 강제 리렌더링
                        st.rerun()

                with col3:
                    # Insert a marker before the button so that we can style it via CSS.
                    st.markdown('<span id="button-summary"></span>', unsafe_allow_html=True)
                    if st.button("요약", key="summary_button"):
                        if st.session_state.editor_content:
                            summary = generate_summary(st.session_state.editor_content)
                            st.session_state.editor_content = summary  # 요약 결과를 편집기에 반영
                            st.session_state.editor_key += 1  # 키 값 변경으로 컴포넌트 강제 리렌더링
                            st.rerun()
                        else:
                            st.warning("요약할 내용이 없습니다. 먼저 보고서를 생성해 주세요.")

                with col4:
                    st.markdown('<span id="button-copy"></span>', unsafe_allow_html=True)
                    if st.button("복사", key="copy_button"):
                        if st.session_state.editor_content:
                            pyperclip.copy(st.session_state.editor_content)
                            st.success("클립보드에 복사되었습니다!")
                        else:
                            st.warning("복사할 내용이 없습니다.")

                with col5:
                    st.markdown('<span id="button-print"></span>', unsafe_allow_html=True)
                    if st.button("출력", key="print_button"):
                        if st.session_state.editor_content:
                            # 엑셀 및 PDF 파일 생성
                            excel_path, pdf_path = create_excel_and_convert_to_pdf(st.session_state.editor_content)

                            # PDF 파일 다운로드 링크 제공
                            with open(pdf_path, "rb") as f:
                                st.download_button(
                                    label="PDF 다운로드",
                                    data=f,
                                    file_name="report.pdf",
                                    mime="application/pdf"
                                )

                            # 임시 파일 삭제
                            os.remove(excel_path)
                            os.remove(pdf_path)

                            st.success("PDF 파일이 생성되었습니다. 다운로드 버튼을 클릭하세요.")
                        else:
                            st.warning("출력할 내용이 없습니다. 먼저 보고서를 생성해 주세요.")



        elif st.session_state.current_page == "📊 NOK AI":
            st.subheader("NOK AI")
            st.write("인공지능 분석 기능이 준비 중입니다.")
        
        elif st.session_state.current_page == "📓 내 노트":
            st.subheader("내 노트")
            st.write("개인 노트 관리 기능이 준비 중입니다.")

def main():
    """메인 앱 설정"""
    st.set_page_config(
        page_title="NOK(Research report)",
        page_icon="🔎",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    
    sidebar()
    main_content()

if __name__ == '__main__':
    main()