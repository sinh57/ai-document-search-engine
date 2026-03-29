# AI Document Search Engine

A simple, local end-to-end question-answering application using Python, LangChain, FAISS, Ollama, and Streamlit.

## Folder Structure
```text
ai-document-search-engine/
│
├── app.py              # Main Streamlit application
├── utils.py            # PDF processing and vector store logic
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation
```

## Setup Instructions

### 1. Install Ollama & llama3
1. Download and install Ollama from [https://ollama.com/](https://ollama.com/).
2. Open your terminal or powershell and run:
   ```bash
   ollama run llama3
   ```
   *(Keep Ollama running in the background).*

### 2. Set up the Python Environment
1. Open terminal inside the `ai-document-search-engine` folder.
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### 3. Run the Application
1. Start the Streamlit app:
   ```bash
   streamlit run app.py
   ```
2. Open the displayed local URL in your browser. Upload PDFs via the sidebar, click Process, and ask your questions!
