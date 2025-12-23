# 🚛 FMCSA Regulatory AI Assistant

**A RAG-based (Retrieval-Augmented Generation) system that answers compliance questions using official FMCSA documentation.**

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![LangChain](https://img.shields.io/badge/LangChain-RAG-green)
![Gemini](https://img.shields.io/badge/AI-Gemini%202.5-orange)
![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-red)

## 🎯 The Problem
Commercial drivers and fleet managers struggle to navigate 1,000+ pages of complex federal regulations (FMCSA). Keyword search is often insufficient for questions requiring synthesis of multiple rules.

## 💡 The Solution
This project ingests the official **FMCSA Electronic Field Operations Training Manual**, chunks it into semantic vectors, and uses a Large Language Model (Gemini 2.5) to provide cited, accurate answers.
`![App Demo](demo_screenshot.png)`

### Key Features
* **Hybrid RAG Architecture:** Combines vector search (ChromaDB) with LLM synthesis.
* **Strict Citation:** Every answer includes specific page numbers from the source PDF.
* **Security First:** API keys are managed via environment variables; no hardcoded secrets.
* **Modular Design:** Logic is decoupled into a reusable `rag_engine` class, separating the ingestion pipeline from the application layer.

## 🏗️ Architecture
```mermaid
graph LR
    A[PDF Documents] -->|Ingestion Pipeline| B(ChromaDB Vector Store)
    C[User Query] -->|Streamlit UI| D[RAG Engine]
    D -->|Semantic Search| B
    B -->|Context Chunks| D
    D -->|Context + Query| E[Gemini 2.5 LLM]
    E -->|Answer| C

🚀 Quick Start
1. Clone the Repository

git clone [https://github.com/YOUR_USERNAME/fmcsa_assistant.git](https://github.com/YOUR_USERNAME/fmcsa_assistant.git)
cd fmcsa_assistant
2. Setup Environment

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\Activate.ps1 on Windows

# Install dependencies
pip install -r requirements.txt

3. Configure Secrets
Create a .env file in the root directory:

Code snippet

GOOGLE_API_KEY=your_api_key_here

4. Run the App

streamlit run app.py

📂 Project Structure
src/rag_engine.py: The core RAG logic (Class-based).
app.py: The Streamlit frontend interface.
notebooks/:
01_ingestion.ipynb: Data exploration, chunking, and vector database creation.
02_demo.ipynb: Headless testing of the engine.
data/chroma_db/: The pre-computed vector store.

🛠️ Technical Decisions & Trade-offs
- ChromaDB vs. Pinecone: Used local ChromaDB for zero-latency local development and simplicity. For production scaling, this can be swapped for a cloud vector store.
- Gemini 2.5 Flash: Chosen for its high context window and speed/cost ratio compared to GPT-4.
- Ingestion Strategy: Decoupled the ingestion (expensive) from inference (cheap) to ensure sub-second query response times in the app.