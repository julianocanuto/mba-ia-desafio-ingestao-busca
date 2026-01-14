import os
from dotenv import load_dotenv
from search import search
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

def get_llm():
    if os.getenv("OPENAI_API_KEY"):
        return ChatOpenAI(model="gpt-3.5-turbo")
    elif os.getenv("GOOGLE_API_KEY"):
        return ChatGoogleGenerativeAI(model="gemini-pro")
    else:
        raise ValueError("Nenhuma chave de API configurada")

def chat_loop():
    llm = get_llm()
    
    template = """Responda à pergunta com base apenas no seguinte contexto:
    {context}

    Pergunta: {question}
    """
    prompt = ChatPromptTemplate.from_template(template)
    
    chain = (
        {"context": lambda x: search(x), "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    print("--- Chat Iniciado (Digite 'sair' para encerrar) ---")
    while True:
        question = input("\nVocê: ")
        if question.lower() in ['sair', 'exit', 'quit']:
            break
            
        response = chain.invoke(question)
        print(f"IA: {response}")

if __name__ == "__main__":
    chat_loop()
