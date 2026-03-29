import sys
import traceback

def test_embeddings():
    print("Testing HuggingFace Embeddings initialization and download...")
    from langchain_community.embeddings import HuggingFaceEmbeddings
    from langchain_community.vectorstores import FAISS
    # This downloads the model to cache if not already there
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = FAISS.from_texts(texts=["Test context"], embedding=embeddings)
    print("Embeddings and FAISS OK!")

def test_ollama():
    print("Testing Ollama service mapping...")
    import requests
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json().get("models", [])
            names = [m["name"] for m in models]
            if not any("llama3" in n for n in names):
                print("Ollama is running but llama3 model is missing.")
                sys.exit(2)
            else:
                print("Ollama and llama3 are both running correctly!")
        else:
            print("Ollama is returning an unexpected response scale.")
            sys.exit(1)
    except requests.exceptions.ConnectionError:
        print("Ollama is completely offline/not running.")
        sys.exit(1)
    except Exception as e:
        print("Unknown error connecting to Ollama:", e)
        sys.exit(1)

if __name__ == "__main__":
    try:
        test_embeddings()
        test_ollama()
    except Exception as e:
        traceback.print_exc()
        sys.exit(3)
