import sys
from search import get_answer

def main():
    print("--- Bem-vindo ao Chat de Busca Semântica ---")
    print("Digite 'sair' para encerrar.")
    
    while True:
        try:
            user_input = input("\nPERGUNTA: ")
            if user_input.lower() in ["sair", "exit", "quit"]:
                print("Encerrando chat...")
                break
            
            if not user_input.strip():
                continue
                
            response = get_answer(user_input)
            print(f"RESPOSTA: {response}")
            
        except KeyboardInterrupt:
            print("\nEncerrando chat...")
            break
        except Exception as e:
            print(f"Erro ao processar a pergunta: {e}")

if __name__ == "__main__":
    main()
