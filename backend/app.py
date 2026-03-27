from fastapi import FastAPI
import requests

app = FastAPI()

OLLAMA_API_URL = "http://localhost:11434"  # ou onde seu Ollama estiver rodando

@app.get("/ask")
def ask(question: str):
    payload = {"model": "llama2", "prompt": question}
    response = requests.post(f"{OLLAMA_API_URL}/api/generate", json=payload)
    return {"answer": response.json()}