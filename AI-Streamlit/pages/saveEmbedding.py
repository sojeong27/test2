import os

#openai_api_key = os.getenv("")

# 직접 API 키를 c명시 (실제 키로 교체하세요)
#openai_api_key = "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"

# Import required modules from LangChain and FAISS
try:
    from langchain_community.document_loaders import UnstructuredExcelLoader
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    from langchain_openai import OpenAIEmbeddings
    from langchain_community.vectorstores import FAISS
except ImportError as e:
    raise ImportError("Please ensure you have installed the required packages for LangChain and FAISS.") from e

def main():
    # Step 1: Load the Excel document.
    try:
        loader = UnstructuredExcelLoader("../data/교육과정성취기준.xlsx", mode="elements")
        docs = loader.load()
        print("Excel document loaded successfully.")
    except Exception as e:
        print(f"Error loading Excel file: {e}")
        return

    # Step 2: Split the documents into manageable chunks.
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=50)
    split_documents = text_splitter.split_documents(docs)
    print(f"Documents split into {len(split_documents)} chunks.")

    # Step 3: Create the embedding model using the directly specified API key.
    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
    print("Embedding model created using OpenAIEmbeddings.")

    # Step 4: Build the FAISS vector store from the split documents.
    vectorstore = FAISS.from_documents(
        documents=split_documents,
        embedding=embeddings
    )
    print("FAISS vector store created.")

    # Step 5: Save the vector store locally.
    save_path = "faiss_index"
    vectorstore.save_local(save_path)
    print(f"Vector store saved locally at: {save_path}")

if __name__ == "__main__":
    main()
