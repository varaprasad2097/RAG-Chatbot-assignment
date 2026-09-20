import os
from pathlib import Path

from dotenv import load_dotenv

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate


BASE_DIR = Path(__file__).resolve().parent

FAISS_DIR = BASE_DIR / "faiss_index"



load_dotenv(BASE_DIR / ".env")



embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-base-en-v1.5"
)




if not FAISS_DIR.exists():

    raise FileNotFoundError(
        f"""
FAISS index not found.

Expected location:
{FAISS_DIR}

Create it from the notebook using:

vectorstore.save_local("faiss_index")
"""
    )


vectorstore = FAISS.load_local(
    str(FAISS_DIR),
    embeddings,
    allow_dangerous_deserialization=True
)




retriever = vectorstore.as_retriever(
    search_kwargs={
        "k": 4
    }
)



llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)




prompt = ChatPromptTemplate.from_template(
    """
You are a document question-answering assistant.

Answer the question using ONLY the provided context.

Rules:

1. Do not use outside knowledge.
2. Do not invent information.
3. If the answer cannot be found in the context,
   say:

   "I could not find the answer in the provided document."

4. Give a concise and informative answer.

Context:
{context}

Question:
{question}

Answer:
"""
)



def ask_rag(question):

    # Retrieve relevant documents
    retrieved_docs = retriever.invoke(question)

    # Combine retrieved content
    context = "\n\n".join(
        doc.page_content
        for doc in retrieved_docs
    )

    # Build prompt
    messages = prompt.invoke(
        {
            "context": context,
            "question": question
        }
    )

    # Generate answer
    response = llm.invoke(messages)

    return response.content, retrieved_docs