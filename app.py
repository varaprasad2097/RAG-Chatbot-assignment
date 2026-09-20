import streamlit as st

from rag_backend import ask_rag



st.set_page_config(
    page_title="RAG Chatbot",
    page_icon="📚",
    layout="wide"
)



st.markdown(
    """
    <style>

    /* Main page */
    .block-container {
        max-width: 1100px;
        padding-top: 2rem;
        padding-bottom: 5rem;
    }

    /* Title */
    .app-title {
        font-size: 2.4rem;
        font-weight: 700;
        margin-bottom: 0.2rem;
    }

    .app-subtitle {
        font-size: 1rem;
        color: #8b8b8b;
        margin-bottom: 2rem;
    }

    /* Source text */
    .source-text {
        font-size: 0.9rem;
        line-height: 1.6;
    }

    /* Sidebar */
    .sidebar-title {
        font-size: 1.2rem;
        font-weight: 700;
    }

    </style>
    """,
    unsafe_allow_html=True
)




st.markdown(
    '<div class="app-title">📚 Research Paper RAG Chatbot</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="app-subtitle">'
    'Ask questions about the <b>Agent-as-a-Judge</b> research paper.'
    '</div>',
    unsafe_allow_html=True
)



if "messages" not in st.session_state:
    st.session_state.messages = []


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        '<div class="sidebar-title">About</div>',
        unsafe_allow_html=True
    )

    st.write(
        """
        This chatbot uses **Retrieval-Augmented Generation (RAG)**
        to answer questions from the research paper.
        """
    )

    st.divider()

    st.subheader("RAG Pipeline")

    st.write(
        """
        PDF  
        ↓  
        PyPDFLoader  
        ↓  
        Text Chunking  
        ↓  
        BGE Embeddings  
        ↓  
        FAISS  
        ↓  
        Retrieval  
        ↓  
        Groq LLM  
        ↓  
        Answer
        """
    )

    st.divider()

    st.subheader("Models")

    st.markdown("**Embedding Model**")
    st.code("BAAI/bge-base-en-v1.5")

    st.markdown("**Vector Database**")
    st.code("FAISS")

    st.markdown("**LLM**")
    st.code("openai/gpt-oss-120b")

    st.divider()

    st.subheader("Retrieval")

    st.write("Top-K retrieved chunks")

    st.code("k = 4")

    st.divider()

    if st.button(
        "🗑️ Clear Conversation",
        use_container_width=True
    ):
        st.session_state.messages = []
        st.rerun()


# ============================================================
# DISPLAY CHAT HISTORY
# ============================================================

for message in st.session_state.messages:

    role = message["role"]

    with st.chat_message(role):

        st.markdown(message["content"])

        # Display sources for assistant messages
        if (
            role == "assistant"
            and message.get("sources")
        ):

            with st.expander(
                f"📚 View Retrieved Sources "
                f"({len(message['sources'])})"
            ):

                for i, source in enumerate(
                    message["sources"],
                    start=1
                ):

                    page = source.get("page", "Unknown")
                    content = source.get("content", "")

                    st.markdown(
                        f"### Source {i}"
                    )

                    st.caption(
                        f"📄 Page {page}"
                    )


                    st.text(content)

                    if i < len(message["sources"]):
                        st.divider()




question = st.chat_input(
    "Ask a question about the research paper..."
)




if question:

    

    with st.chat_message("user"):
        st.markdown(question)

    # Save user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )



    with st.chat_message("assistant"):

        try:

            with st.spinner(
                "🔎 Searching the paper and generating an answer..."
            ):

                answer, retrieved_docs = ask_rag(question)


          

            st.markdown(answer)


           

            sources = []

            for doc in retrieved_docs:

                page = doc.metadata.get(
                    "page",
                    None
                )

                
                if page is not None:
                    page = page + 1

                sources.append(
                    {
                        "page": page,
                        "content": doc.page_content
                    }
                )



            if sources:

                with st.expander(
                    f"📚 View Retrieved Sources "
                    f"({len(sources)})"
                ):

                    for i, source in enumerate(
                        sources,
                        start=1
                    ):

                        st.markdown(
                            f"### Source {i}"
                        )

                        st.caption(
                            f"📄 Page {source['page']}"
                        )

                        st.text(
                            source["content"]
                        )

                        if i < len(sources):
                            st.divider()



            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": answer,
                    "sources": sources
                }
            )


        except Exception as e:

            error_message = str(e)

            st.error(
                "Something went wrong while processing "
                "your question."
            )

            with st.expander("Show error details"):
                st.code(error_message)