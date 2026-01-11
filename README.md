# Ingestion and Semantic Search with LangChain and Postgres

This project implements a RAG (Retrieval-Augmented Generation) system that ingests PDF documents into a PostgreSQL database with `pgVector` and provides a CLI for semantic search.

## Prerequisites

- Python 3.10+
- Docker and Docker Compose
- API Key for OpenAI or Google Gemini

## Setup

1. **Clone the repository** (if you haven't already).
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Configure Environment**:
   Copy `.env.example` to `.env` and fill in your API keys and configuration.
   ```bash
   cp .env.example .env
   ```
4. **Start Database**:
   ```bash
   docker compose up -d
   ```
5. **Place your PDF**:
   Ensure there is a `document.pdf` file in the root directory.

## Execution

### 1. Ingest Data
Run the ingestion script to process the PDF and store vectors in the database:
```bash
python src/ingest.py
```

### 2. Chat with your PDF
Start the CLI chat interface:
```bash
python src/chat.py
```

## Dev Container
This project includes a `.devcontainer` configuration for VS Code, which sets up the entire environment (Python + PostgreSQL) automatically.
