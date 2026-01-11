# Ingestion and Semantic Search with LangChain and Postgres

This project implements a RAG (Retrieval-Augmented Generation) system that ingests PDF documents into a PostgreSQL database with `pgVector` and provides a CLI for semantic search.

## Prerequisites

- Python 3.10+
- Docker and Docker Compose
- API Key for OpenAI or Google Gemini

## Quick Start

You can now run the entire application lifecycle with a single command:

```bash
python app.py
```

This script will:
1. Spin up the Docker containers.
2. Wait for the database to be healthy.
3. Prompt you to add `document.pdf` to the root folder.
4. Run the ingestion process.
5. Start the chat interface.

---

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

## Manual Execution (Advanced)

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
