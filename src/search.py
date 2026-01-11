import os
from dotenv import load_dotenv
from langchain_postgres import PGVector
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

load_dotenv()

def get_embeddings():
    provider = os.getenv("LLM_PROVIDER", "gemini").lower()
    if provider == "openai":
        return OpenAIEmbeddings(model="text-embedding-3-small")
    elif provider == "gemini":
        return GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    else:
        raise ValueError(f"Unknown LLM_PROVIDER: {provider}")

def get_llm():
    provider = os.getenv("LLM_PROVIDER", "gemini").lower()
    if provider == "openai":
        return ChatOpenAI(model="gpt-4o-mini", temperature=0) # Using 4o-mini as gpt-5-nano might not be available
    elif provider == "gemini":
        return ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest", temperature=0)
    else:
        raise ValueError(f"Unknown LLM_PROVIDER: {provider}")

def get_vector_store(collection_name="pdf_docs"):
    embeddings = get_embeddings()
    connection = os.getenv("DB_URL")
    return PGVector(
        embeddings=embeddings,
        collection_name=collection_name,
        connection=connection,
        use_jsonb=True,
    )

def perform_search(query, k=10):
    vector_store = get_vector_store()
    # Search for the top k most relevant results
    results = vector_store.similarity_search_with_score(query, k=k)
    return results

def get_answer(question):
    vector_store = get_vector_store()
    retriever = vector_store.as_retriever(search_kwargs={"k": 10})

    template = """CONTEXT:
{context}

RULES:
- Answer ONLY based on the CONTEXT.
- If the information is not explicitly in the CONTEXT, respond:
  "Não tenho informações necessárias para responder sua pergunta."
- Never hallucinate or use external knowledge.
- Never provide opinions or interpretations beyond what is written.

OUT-OF-CONTEXT EXAMPLES:
Question: "What is the capital of France?"
Response: "Não tenho informações necessárias para responder sua pergunta."

Question: "How many customers do we have in 2024?"
Response: "Não tenho informações necessárias para responder sua pergunta."

Question: "Do you think this is good or bad?"
Response: "Não tenho informações necessárias para responder sua pergunta."

USER QUESTION:
{question}

ANSWER THE "USER QUESTION"
"""
    prompt = PromptTemplate.from_template(template)
    llm = get_llm()

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    return rag_chain.invoke(question)
