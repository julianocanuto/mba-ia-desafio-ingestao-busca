# Desafio de Ingestão e Busca Semântica

Este projeto é uma implementação de um sistema de RAG (Retrieval-Augmented Generation) como parte de um desafio de MBA.

## Funcionalidades

- **Ingestão de Documentos**: Processamento e vetorização de arquivos PDF.
- **Busca Semântica**: Recuperação de trechos relevantes baseada em similaridade.
- **Chat Interativo**: Interface para perguntas e respostas sobre o documento.

## Configuração

1. Clone o repositório.
2. Copie `.env.example` para `.env` e configure suas chaves de API.
3. Coloque seu arquivo PDF na raiz como `document.pdf`.
4. Suba o banco de dados:
   ```bash
   docker-compose up -d
   ```
5. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

## Uso

1. Realize a ingestão do documento:
   ```bash
   python src/ingest.py
   ```

2. Inicie o chat:
   ```bash
   python src/chat.py
   ```
