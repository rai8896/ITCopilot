# ITCopilot — Agentic RAG Support Assistant

An AI-powered IT support assistant that uses **Agentic RAG** to answer employee questions from a private knowledge base and can fall back to web search when internal evidence is insufficient.

Built with **LangGraph, FastAPI, Groq, Hugging Face, Pinecone, Tavily, HTML, CSS, and JavaScript**.

## 1. Project Overview

### Business Problem

IT teams manage multiple documents covering VPN access, password policies, MFA rules, software installation, laptop troubleshooting, and service-desk procedures.

Employees often struggle to find the correct information, while traditional chatbots may generate answers without sufficient evidence.

**ITCopilot** addresses this problem by combining private knowledge retrieval, evidence evaluation, and external web search in an agentic workflow.

### Key Objectives

- Retrieve information from the private company knowledge base first.
- Evaluate whether retrieved evidence is sufficient to answer a question.
- Generate answers grounded in relevant internal documents.
- Use web search when internal knowledge is insufficient.
- Support query rewriting and retrieval retries where configured.
- Return source information and workflow traces for transparency.

> The included company IT documents are sample data for demonstration purposes, not real corporate policies.

## 2. Key Features

- **Agentic RAG:** Uses LangGraph to coordinate the question-answering workflow.
- **Private Knowledge Retrieval:** Uses Pinecone to search indexed company IT documents.
- **Local Embeddings:** Uses Hugging Face's `sentence-transformers/all-MiniLM-L6-v2` model.
- **Evidence Evaluation:** Checks retrieved information before generating an answer.
- **Web Search Fallback:** Integrates Tavily for external information retrieval.
- **Workflow Transparency:** Exposes source information and workflow traces where available.
- **FastAPI Backend:** Provides the backend for the application.
- **Web Interface:** Includes a browser-based UI built with HTML, CSS, and JavaScript.

## 3. Architecture

```text
              Employee / User
                     |
                     v
           HTML / CSS / JavaScript
                  Web UI
                     |
                     v
                  FastAPI
                     |
                     v
           LangGraph Workflow
                     |
                     v
          Private Knowledge Retrieval
                     |
                     v
                  Pinecone
                     ^
                     |
             Hugging Face
               Embeddings
                     |
                     v
             Evidence Evaluation
                     |
             +-------+-------+
             |               |
         Sufficient       Insufficient
             |               |
             v               v
       Private KB        Tavily Web
          Answer           Search
                             |
                             v
                     Evidence Evaluation
                             |
                             v
                       Final Answer
```

## 4. Agentic RAG Workflow

The application follows an evidence-aware retrieval workflow.

```text
User Question
      |
      v
Route Question
      |
      +---- Casual Message ----> Direct Answer
      |
      v
Retrieve from Private Pinecone KB
      |
      v
Evaluate Private Evidence
      |
      +---- Sufficient ----> Generate Grounded KB Answer
      |
      +---- Insufficient
                 |
                 v
           Tavily Web Search
                 |
                 v
          Evaluate Web Evidence
                 |
          +------+------+
          |             |
      Sufficient     Insufficient
          |             |
          v             v
      Web Answer    Retry / Insufficient
                    Evidence Handling
```

The exact route depends on the workflow logic and the evidence returned during execution.

Unlike basic RAG, which typically retrieves documents and generates an answer, Agentic RAG uses conditional decisions to determine the next step.

## 5. Technology Stack

| Component | Technology | Purpose |
|---|---|---|
| Agent Workflow | LangGraph | Stateful workflow and conditional routing |
| LLM | Groq | Language-model tasks |
| Embeddings | Hugging Face | Local text embeddings |
| Embedding Model | `sentence-transformers/all-MiniLM-L6-v2` | 384-dimensional embeddings |
| Vector Database | Pinecone | Private knowledge-base retrieval |
| Web Search | Tavily | External search fallback |
| Backend | FastAPI | Application and API endpoints |
| Frontend | HTML, CSS, JavaScript | User interface |
| Packaging | Docker | Container packaging |

## 6. Project Structure

```text
ITCopilot/
├── app/
│   ├── api/
│   ├── core/
│   ├── rag/
│   │   ├── state.py
│   │   ├── vectorstore.py
│   │   └── workflow.py
│   ├── services/
│   └── main.py
├── data/
│   └── sample_kb/
│       ├── company_it_handbook.md
│       └── service_desk_runbook.md
├── static/
├── templates/
├── uploads/
├── .env.example
├── .gitignore
├── Dockerfile
├── ingest_sample_kb.py
├── requirements.txt
├── run.py
└── README.md
```

## 7. Prerequisites

Before running the project, ensure you have:

- Python installed.
- A Groq API key.
- A Pinecone API key and configured index.
- A Tavily API key for web-search functionality.
- Git installed.

The Pinecone index must support **384-dimensional vectors** for the configured embedding model.

## 8. Installation and Setup

### Step 1: Clone the Repository

```bash
git clone https://github.com/rai8896/ITCopilot.git
cd ITCopilot
```

### Step 2: Create a Virtual Environment

**Windows PowerShell**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux**

```bash
python -m venv .venv
source .venv/bin/activate
```

### Step 3: Install Dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables

Create a `.env` file in the project root and add your own API credentials.

```env
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=openai/gpt-oss-120b

PINECONE_API_KEY=your_pinecone_api_key
PINECONE_INDEX_NAME=fde-it-support-rag
PINECONE_NAMESPACE=company-it-kb

TAVILY_API_KEY=your_tavily_api_key
ADMIN_API_KEY=replace_with_a_secure_key
```

**Important:** Verify the exact environment variable names in `app/core/config.py`. The values above reflect the current project setup; adjust them if your local configuration differs.

Never upload your real `.env` file or API keys to GitHub.

### Step 5: Index the Sample Knowledge Base

```bash
python ingest_sample_kb.py
```

This script processes the sample knowledge-base documents, generates embeddings, and indexes the resulting vectors in Pinecone.

The demonstrated setup uses:

- **Index:** `fde-it-support-rag`
- **Namespace:** `company-it-kb`
- **Embedding model:** `sentence-transformers/all-MiniLM-L6-v2`

### Step 6: Run the Application

```bash
python run.py
```

Open the application in your browser:

- **Web UI:** http://127.0.0.1:8000
- **FastAPI documentation:** http://127.0.0.1:8000/docs

## 9. Example Questions

### Private Knowledge Base

**Question:**

> How do I connect to the company VPN from home?

Expected behavior: retrieve relevant internal documentation and answer from the private knowledge base when the evidence is sufficient.

### IT Policy Question

**Question:**

> Can I share my MFA code with the IT support team?

Expected behavior: retrieve the relevant company policy and provide an answer grounded in the available documentation.

### External Information

**Question:**

> What is the latest Microsoft Teams outage guidance?

Expected behavior: if the private knowledge base lacks sufficient evidence, the workflow can attempt a Tavily web search.

External information should be checked against reliable sources before being used for operational decisions.

### Casual Conversation

**Question:**

> Hello!

Expected behavior: simple greetings may be handled directly without running knowledge-base retrieval.

## 10. API Documentation

The running application may expose endpoints such as:

| Endpoint | Purpose |
|---|---|
| `GET /api/health` | Health check |
| `POST /api/chat` | Submit a user question |
| `POST /api/ingest` | Add documents to the knowledge base, if enabled |

Check `http://127.0.0.1:8000/docs` for the actual endpoints, request formats, and response schemas in your current version.

If document ingestion is enabled, protect it with the configured admin-key mechanism.



## Author

**Manish Rai**

GitHub: [@rai8896](https://github.com/rai8896)
