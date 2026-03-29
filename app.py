import streamlit as st
from utils import get_pdf_text, get_text_chunks, get_vectorstore
from langchain_groq import ChatGroq
from langchain_classic.chains import ConversationalRetrievalChain

def init_session_state():
    """Initialize session state variables."""
    if "vectorstore" not in st.session_state:
        st.session_state.vectorstore = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "qa_chain" not in st.session_state:
        st.session_state.qa_chain = None

def main():
    # Improved page configuration
    st.set_page_config(page_title="AI Document Search Engine", page_icon="📄", layout="wide")
    
    init_session_state()

    st.header("AI Document Search Engine 📄")
    st.markdown("Upload your PDF documents and ask questions! The AI remembers the context of your conversation.")

    with st.sidebar:
        st.subheader("📁 Your Documents")
        pdf_docs = st.file_uploader(
            "Upload PDFs here and click 'Process'", 
            accept_multiple_files=True, type=["pdf"]
        )
        
        if st.button("Process Documents", type="primary"):
            if pdf_docs:
                with st.spinner("Processing documents into vector space..."):
                    # 1. Extract text and Split
                    raw_text = get_pdf_text(pdf_docs)
                    text_chunks = get_text_chunks(raw_text)
                    
                    # 2. Embed into FAISS
                    st.session_state.vectorstore = get_vectorstore(text_chunks)
                    
                    # 3. Initialize memory-enabled Conversational Chain with Groq
                    groq_api_key = st.secrets["GROQ_API_KEY"]
                    llm = ChatGroq(
                        groq_api_key=groq_api_key,
                        model_name="llama-3.3-70b-versatile"
                    )
                    st.session_state.qa_chain = ConversationalRetrievalChain.from_llm(
                        llm=llm,
                        retriever=st.session_state.vectorstore.as_retriever(search_kwargs={"k": 3}),
                        return_source_documents=True
                    )
                    
                    st.success("Documents processed successfully!")
            else:
                st.warning("Please upload at least one PDF file.")
                
        st.divider()
        if st.button("🗑️ Clear Chat History"):
            st.session_state.chat_history = []
            st.rerun()

    # --- MAIN CHAT INTERFACE ---
    
    # Display existing chat history
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # UI Chat input element
    if prompt := st.chat_input("Ask a question about your documents..."):
        
        if st.session_state.qa_chain is None:
            st.warning("Please upload and process documents first from the sidebar.")
        else:
            # Display user message instantly
            with st.chat_message("user"):
                st.markdown(prompt)
                
            # Keep history for UI presentation
            st.session_state.chat_history.append({"role": "user", "content": prompt})
            
            # Formulate history tuples for Langchain: [(q1, a1), (q2, a2)]
            langchain_history = []
            for i in range(0, len(st.session_state.chat_history) - 1, 2):
                if (i + 1 < len(st.session_state.chat_history)
                        and st.session_state.chat_history[i]["role"] == "user"
                        and st.session_state.chat_history[i + 1]["role"] == "assistant"):
                    user_q = st.session_state.chat_history[i]["content"]
                    bot_a = st.session_state.chat_history[i + 1]["content"]
                    langchain_history.append((user_q, bot_a))

            # Display assistant response block
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    
                    # Invoke memory-enabled chain
                    response = st.session_state.qa_chain.invoke({
                        "question": prompt, 
                        "chat_history": langchain_history
                    })
                    
                    answer = response["answer"]
                    source_docs = response.get("source_documents", [])
                    
                    st.markdown(answer)
                    
                    # Show expandable sources block
                    if source_docs:
                        with st.expander("View Source Documents Used"):
                            for i, doc in enumerate(source_docs):
                                st.markdown(f"**Chunk {i+1}:**")
                                st.write(doc.page_content)
                                st.divider()
                                
            # Save assistant response to UI history
            st.session_state.chat_history.append({"role": "assistant", "content": answer})

if __name__ == '__main__':
    main()
