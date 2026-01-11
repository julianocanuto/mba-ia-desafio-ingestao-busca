import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_postgres import PGVector
from langchain_openai import OpenAIEmbeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings

load_dotenv()

def get_embeddings():
    provider = os.getenv("LLM_PROVIDER", "gemini").lower()
    if provider == "openai":
        return OpenAIEmbeddings(model="text-embedding-3-small")
    elif provider == "gemini":
        return GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    else:
        raise ValueError(f"Unknown LLM_PROVIDER: {provider}")

def ingest_pdf(pdf_path, collection_name="pdf_docs"):
    # Load PDF
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()

    # Split PDF content
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150,
        length_function=len,
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Split {len(documents)} pages into {len(chunks)} chunks.")

    # Get Embeddings
    embeddings = get_embeddings()

    # Database connection string
    connection = os.getenv("DB_URL")
    
    # Store vectors in PostgreSQL using PGVector
    vector_store = PGVector(
        embeddings=embeddings,
        collection_name=collection_name,
        connection=connection,
        use_jsonb=True,
    )
    
    vector_store.add_documents(chunks)
    print(f"Successfully ingested {len(chunks)} chunks into the database.")

if __name__ == "__main__":
    pdf_file = "document.pdf"
    if not os.path.exists(pdf_file):
        print(f"Error: {pdf_file} not found. Please place the PDF in the root directory.")
    else:
        ingest_pdf(pdf_file)
