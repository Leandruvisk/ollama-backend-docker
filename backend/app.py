# app.py

from fastapi import FastAPI
from pydantic import BaseModel
import requests
import os

app = FastAPI()

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")


class ChatRequest(BaseModel):
    message: str
    model: str = "llama3"
    session_id: str


# memória
conversations = {}


# monta contexto
def build_prompt(session_id, user_message):
    history = conversations.get(session_id, [])

    prompt = (
        "Você é um assistente técnico.\n"
        "Responda sempre em português do Brasil.\n"
        "Seja direto e objetivo.\n"
        "NÃO invente contexto.\n"
        "NÃO continue a conversa após responder.\n"
        "Responda apenas o necessário.\n\n"
    )

    for msg in history[-30:]:
        prompt += f"<user>{msg['user']}</user>\n"
        prompt += f"<assistant>{msg['bot']}</assistant>\n"

    prompt += f"<user>{user_message}</user>\n<assistant>"

    return prompt


# endpoint principal
@app.post("/chat")
def chat(req: ChatRequest):

    print("Recebido:", req)

    prompt = build_prompt(req.session_id, req.message)
    print("Prompt:", prompt)

    payload = {
        "model": req.model,
        "prompt": prompt,
        "stream": False,
        "options": {
            "num_predict": 100,   # limita tamanho
            "temperature": 0.2    # menos criatividade
        }
    }

    response = requests.post(
        f"{OLLAMA_URL}/api/generate",
        json=payload,
        timeout=60
    )

    data = response.json()
    print("Resposta completa:", data)

    answer = data.get("response")

    # salva histórico
    conversations.setdefault(req.session_id, []).append({
        "user": req.message,
        "bot": answer
    })

    return {"response": answer}


# limpar memória
@app.delete("/chat/{session_id}")
def clear_session(session_id: str):
    conversations.pop(session_id, None)
    return {"status": "cleared"}