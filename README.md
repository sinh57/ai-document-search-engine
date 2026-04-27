
# AI Document Search Engine 📄

A powerful, end-to-end question-answering application that allows you to chat with your PDF documents. Built with Python, LangChain, FAISS, Groq (Llama-3), HuggingFace Embeddings, and Streamlit.

This app relies on local Sentence Transformers (`all-MiniLM-L6-v2`) for embeddings and a blazing fast LLM via the Groq API (`llama-3.3-70b-versatile`).

## Folder Structure
```text
ai-document-search-engine/
│
├── .streamlit/
│   └── secrets.toml    # API Keys (Local Only - do not commit!)
├── app.py              # Main Streamlit application
├── utils.py            # PDF processing and FAISS vector store logic
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation
```

## Setup Instructions (Local Development)

### 1. Requirements
- Python 3.9 - 3.12 (Python 3.12 recommended)
- A [Groq API Key](https://console.groq.com/keys)

### 2. Set up the Environment
1. Clone the repository and navigate to the project directory:
   ```bash
   git clone https://github.com/abrarkhatri/AI-document-search-engine.git
   cd AI-document-search-engine
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### 3. Add API Keys
1. Create a folder named `.streamlit` in the root directory.
2. Inside that folder, create a file named `secrets.toml`.
3. Add your Groq API key:
   ```toml
   GROQ_API_KEY = "your_actual_api_key_here"
   ```

### 4. Run the Application
Start the Streamlit app:
```bash
streamlit run app.py
```
Open the local URL displayed in your browser. Upload your PDFs via the sidebar, click Process, and ask your questions!

---

## Deployment (Streamlit Community Cloud)

This app is production-ready for deployment on **Streamlit Community Cloud**.

1. Push your code to your GitHub repository.
2. Go to [share.streamlit.io](https://share.streamlit.io/) and select **New App**.
3. Point it to this repository (`abrarkhatri/AI-document-search-engine`) and select `app.py` as the main file path.
4. **Important**: Before clicking Deploy, open **Advanced settings**.
   - Select **Python 3.12** as the Python version.
   - In the **Secrets** section, paste the contents of your `secrets.toml`:
     ```toml
     GROQ_API_KEY = "your_actual_api_key_here"
     ```
5. Click **Deploy**. The app will install the `requirements.txt` dependencies (automatically pulling PyTorch for `sentence-transformers`), download the HuggingFace models upon the first PDF upload, and run seamlessly!
