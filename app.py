# app.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import os

from backend.db.database import Base, engine, SessionLocal
from backend.db.models import Conversation
from fastapi.responses import StreamingResponse
import json

# cria tabelas
Base.metadata.create_all(bind=engine)

app = FastAPI()

# IMPORTANTE: dentro do docker é o nome do serviço
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://ollama:11434")


# =========================
# SCHEMA
# =========================
class ChatRequest(BaseModel):
    message: str
    model: str = "llama3"
    session_id: str


# =========================
# DATABASE HELPERS
# =========================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_history(db, session_id: str):
    return (
        db.query(Conversation)
        .filter(Conversation.session_id == session_id)
        .order_by(Conversation.id)
        .all()
    )


def save_message(db, session_id: str, user_msg: str, bot_msg: str):
    conv = Conversation(
        session_id=session_id,
        user_message=user_msg,
        bot_response=bot_msg
    )
    db.add(conv)
    db.commit()


def clear_history(db, session_id: str):
    db.query(Conversation)\
      .filter(Conversation.session_id == session_id)\
      .delete()
    db.commit()


# =========================
# PROMPT BUILDER
# =========================
def build_prompt(history, user_message):
    prompt = "Responda sempre em português do Brasil.\n"

    for msg in history[-20:]:
        prompt += f"<user>{msg.user_message}</user>\n"
        prompt += f"<assistant>{msg.bot_response}</assistant>\n"

    prompt += f"<user>{user_message}</user>\n<assistant>"

    return prompt


# =========================
# ENDPOINTS
# =========================


@app.post("/chat")
def chat(req: ChatRequest):

    def generate():
        db = SessionLocal()

        try:
            history = get_history(db, req.session_id)
            prompt = build_prompt(history, req.message)

            payload = {
                "model": req.model,
                "prompt": prompt,
                "stream": True,
                "options": {
                    "num_predict": 200,
                    "temperature": 0.2
                }
            }

            with requests.post(
                f"{OLLAMA_URL}/api/generate",
                json=payload,
                stream=True,
                timeout=120
            ) as r:

                full_response = ""

                for line in r.iter_lines():
                    if line:
                        data = json.loads(line.decode("utf-8"))

                        token = data.get("response", "")
                        full_response += token

                        # envia token pro cliente
                        yield token

                        if data.get("done", False):
                            break

                # salva no banco só no final
                save_message(db, req.session_id, req.message, full_response)

        except Exception as e:
            yield f"\n[ERRO]: {str(e)}"

        finally:
            db.close()

    return StreamingResponse(generate(), media_type="text/plain")

@app.delete("/chat/{session_id}")
def clear_session(session_id: str):
    db = SessionLocal()

    try:
        clear_history(db, session_id)
        return {"status": "cleared"}
    finally:
        db.close()