RAG Chatbot — Agent-as-a-Judge Research Paper

A Retrieval-Augmented Generation (RAG) chatbot that answers questions from the Agent-as-a-Judge: Evaluate Agents with Agents research paper.

The project uses LangChain for the RAG pipeline, BAAI/bge-base-en-v1.5 for semantic embeddings, FAISS for vector search, Groq for answer generation, and Streamlit for the frontend. RAGAS is used to evaluate retrieval and generation quality.

Features

PDF ingestion with PyPDFLoader

Recursive text chunking

Semantic embeddings with BAAI/bge-base-en-v1.5

FAISS vector database

Top-4 semantic retrieval

Groq-powered grounded answer generation

Retrieved source/page display

Interactive Streamlit chatbot

RAGAS evaluation

Notebook for experimentation and evaluation

Architecture

Research Paper PDF
       |
       v
PyPDFLoader
       |
       v
RecursiveCharacterTextSplitter
(chunk_size=700, overlap=100)
       |
       v
BGE-base-en-v1.5 Embeddings
       |
       v
FAISS Vector Store
       |
   User Question
       |
       v
Retriever (Top K = 4)
       |
       v
Retrieved Context
       |
       v
RAG Prompt
       |
       v
Groq GPT-OSS-120B
       |
       v
Answer + Retrieved Sources

Tech Stack

Component

Technology

Language

Python

RAG Framework

LangChain

PDF Loader

PyPDFLoader

Text Splitter

RecursiveCharacterTextSplitter

Embeddings

BAAI/bge-base-en-v1.5

Vector Database

FAISS

LLM

Groq openai/gpt-oss-120b

Frontend

Streamlit

Evaluation

RAGAS

Project Structure

RAG-Chatbot-assignment/
├── app.py                  # Streamlit frontend
├── rag_backend.py         # RAG backend
├── rag.ipynb              # RAG experiments and evaluation
├── requirements.txt        # Dependencies
├── .env                    # Local API key; not committed
├── .gitignore
├── README.md
├── faiss_index/            # Generated locally; ignored by Git
│   ├── index.faiss
│   └── index.pkl
└── 2410.10934v2_7033 1.pdf # Local source document

Setup

1. Clone

git clone <YOUR_GITHUB_REPOSITORY_URL>
cd RAG-Chatbot-assignment

2. Create a virtual environment

Windows:

python -m venv venv
venv\Scripts\activate

macOS/Linux:

python3 -m venv venv
source venv/bin/activate

3. Install dependencies

pip install -r requirements.txt

Or install the main packages directly:

pip install -U langchain langchain-community langchain-text-splitters langchain-groq langchain-huggingface sentence-transformers faiss-cpu streamlit ragas python-dotenv

Environment Variables

Create .env in the project root:

GROQ_API_KEY=your_groq_api_key

Never commit your API key.

Create the FAISS Index

Run the relevant cells in rag.ipynb to load the PDF, split it into chunks, generate embeddings, and create the FAISS vector store.

After creating vectorstore, save it once:

vectorstore.save_local("faiss_index")

This creates:

faiss_index/
├── index.faiss
└── index.pkl

The Streamlit application loads this saved index instead of recomputing all document embeddings on every startup.

Run the Chatbot

streamlit run app.py

The UI provides:

Chat-based question answering

Conversation history

Retrieved source chunks

Source page numbers

Clear conversation button

RAG pipeline information

Example

Question:

What is Agent-as-a-Judge?

The system:

Embeds the question.

Searches FAISS.

Retrieves the four most relevant chunks.

Builds a grounded RAG prompt.

Sends the context and question to Groq.

Displays the answer.

Displays the retrieved source chunks and page numbers.

RAG Prompt

The model is instructed to use only retrieved document context and not invent information.

If the answer cannot be found in the retrieved context, it is instructed to respond:

I could not find the answer in the provided document.

RAGAS Evaluation

RAGAS is integrated into rag.ipynb for evaluating the RAG pipeline.

The project evaluates metrics including:

Faithfulness — whether the generated answer is supported by retrieved context.

Context Precision — whether retrieved context is relevant to the question.

Context Recall — whether the required information was retrieved.

Response Relevancy — whether the generated answer addresses the question.

An individual test sample produced:

Faithfulness:      0.8571
Context Precision: 1.0000

These values are from a single evaluation sample and should not be presented as overall system performance. Aggregate evaluation should be performed over the complete question set.

Notebook Workflow

PDF Loading
    ↓
Document Inspection
    ↓
Chunking
    ↓
Embedding
    ↓
FAISS
    ↓
Retriever Testing
    ↓
Groq Generation
    ↓
RAG Answer
    ↓
RAGAS Evaluation

Design Decisions

Why FAISS?

FAISS provides efficient local vector similarity search and is simple to integrate with LangChain.

Why BGE-base?

BAAI/bge-base-en-v1.5 provides a practical balance between semantic retrieval quality and local inference cost for this relatively small research-paper corpus.

Why save the FAISS index?

Embedding the complete document corpus is the most time-consuming initialization step. Saving the vector store avoids recomputing embeddings every time the Streamlit application starts.

Why separate frontend and backend?

app.py handles the Streamlit interface while rag_backend.py contains retrieval, prompting, and generation logic. This keeps the application easier to test and maintain.

Future Improvements

Automatically evaluate the complete question bank.

Add a RAGAS evaluation dashboard.

Add document upload support.

Support multiple documents.

Add source highlighting.

Generate automated evaluation reports.

Add persistent vector-store management.

Deploy the chatbot.

Author

Chennareddy Devi Vara Prasada Reddy

Built as a RAG/LLM application demonstrating semantic retrieval, vector databases, grounded generation, RAG evaluation, and Streamlit application development.