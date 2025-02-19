from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
import pandas as pd
from typing import List, Dict, Optional
from langchain.schema import Document
from langchain.vectorstores import FAISS
import time
import os
import re
import logging
import shutil

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

openai_apikey =  ""


def preprocess_text(text: str) -> str:
    """텍스트 전처리 함수"""
    text = re.sub(r'-{2,}', '-', text)
    text = re.sub(r'={2,}', '=', text)
    text = re.sub(r'_{2,}', '_', text)
    text = re.sub(r'\n+', '\n', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def load_documents(excel_file_path: str) -> tuple[List[Document], pd.DataFrame]:
    """엑셀 파일에서 문서 로드 및 키워드 처리"""
    logger.info(f"Loading documents from {excel_file_path}")
    
    try:
        df = pd.read_excel(excel_file_path)
        required_columns = ['학년', '교과', '주제어'] + [f'키워드{i}' for i in range(1,6)]
        df = df[required_columns]  # 필요한 컬럼만 필터링
        
        docs = []
        for _, row in df.iterrows():
            # 키워드 리스트 생성 (NaN 처리 포함)
            keywords = []
            for i in range(1,6):
                keyword = row[f'키워드{i}']
                keywords.append(str(keyword) if not pd.isna(keyword) else "")
            
            # 문서 내용 구성
            content = "\n".join([
                f"교과: {preprocess_text(str(row['교과']))}",
                f"학년: {preprocess_text(str(row['학년']))}",
                f"주제어: {preprocess_text(str(row['주제어']))}"
            ])
            
            # 메타데이터 구성
            metadata = {
                'subject': preprocess_text(str(row['교과'])),
                'grade': preprocess_text(str(row['학년'])),
                'topic': preprocess_text(str(row['주제어'])),
                'keywords': keywords  # 키워드 리스트 저장
            }
            
            docs.append(Document(page_content=content, metadata=metadata))
        
        logger.info(f"Created {len(docs)} document objects with keywords")
        return docs, df
        
    except Exception as e:
        logger.error(f"Error loading documents: {str(e)}")
        raise

def query_keywords(vectorstore: FAISS, subject: str, grade: str, topic: str) -> List[str]:
    """학년, 교과, 주제어 입력 시 해당 키워드 검색"""
    query_text = f"교과: {subject} 학년: {grade} 주제어: {topic}"
    results = vectorstore.similarity_search(query_text, k=1)
    
    if not results:
        logger.warning("No matching documents found")
        return []
    
    best_match = results[0]
    return best_match.metadata['keywords']

def create_vectorstore_sequentially(
    docs: List[Document],
    embeddings: OpenAIEmbeddings,
    save_path: str,
    batch_size: int = 100,
    sleep_time: int = 2
) -> FAISS:
    """문서를 배치 단위로 순차적으로 처리하여 벡터 스토어 생성"""
    logger.info("Starting sequential vector store creation")
    vectorstore = None
    
    # 배치 단위로 문서 처리
    for i in range(0, len(docs), batch_size):
        batch = docs[i:i + batch_size]
        logger.info(f"Processing batch {i//batch_size + 1}/{(len(docs)-1)//batch_size + 1}")
        
        try:
            if vectorstore is None:
                vectorstore = FAISS.from_documents(batch, embeddings)
            else:
                temp_store = FAISS.from_documents(batch, embeddings)
                vectorstore.merge_from(temp_store)
            
            # 중간 저장
            vectorstore.save_local(f"{save_path}_temp")
            logger.info(f"Saved temporary vector store after batch {i//batch_size + 1}")
            
            # API 레이트 리밋 방지를 위한 딜레이
            time.sleep(sleep_time)
            
        except Exception as e:
            logger.error(f"Error processing batch {i//batch_size + 1}: {str(e)}")
            # 마지막 저장된 상태 복구 가능
            if os.path.exists(f"{save_path}_temp"):
                logger.info("Attempting to recover from last saved state")
                vectorstore = FAISS.load_local(f"{save_path}_temp", embeddings)
            raise

    # 최종 저장
    if vectorstore:
        vectorstore.save_local(save_path)
        # 임시 저장 폴더 삭제 (파일이 아니라 디렉토리라면 shutil.rmtree 사용)
        temp_path = f"{save_path}_temp"
        if os.path.exists(temp_path):
            try:
                if os.path.isdir(temp_path):
                    shutil.rmtree(temp_path)
                else:
                    os.remove(temp_path)
                logger.info(f"Temporary vector store {temp_path} removed successfully.")
            except Exception as e:
                logger.error(f"Error removing temporary vector store: {str(e)}")
        logger.info(f"Vector store successfully saved to {save_path}")

    return vectorstore

def test_vectorstore(vectorstore: FAISS):
    """벡터 스토어 검색 테스트 (실제 사용 예시)"""
    test_cases = [
        ('사회', '6학년', '국회'),
        ('과학', '6학년', '지구와 달'),
        ('국어', '6학년', '속담')
    ]
    
    for subject, grade, topic in test_cases:
        logger.info(f"\n검색 조건: 교과={subject}, 학년={grade}, 주제어={topic}")
        keywords = query_keywords(vectorstore, subject, grade, topic)
        logger.info(f"추출 키워드: {keywords}")

def main():
    """메인 실행 함수"""
    try:
        # 1. 문서 로드
        docs, df = load_documents("../data/키워드.xlsx")
        
        # 2. 임베딩 모델 초기화
        embeddings = OpenAIEmbeddings(
            model="text-embedding-3-large",
            openai_api_key=openai_apikey
        )
        
        # 3. 벡터 스토어 생성
        save_path = "curriculum_keyword_vectorstore"
        vectorstore = create_vectorstore_sequentially(
            docs=docs,
            embeddings=embeddings,
            save_path=save_path,
            batch_size=50,
            sleep_time=2
        )
        
        # 4. 테스트 케이스로 검증
        test_vectorstore(vectorstore)
        
        logger.info("Process completed successfully")
        
    except Exception as e:
        logger.error(f"Error in main process: {str(e)}")
        raise

if __name__ == "__main__":
    load_dotenv()
    main()