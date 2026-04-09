from fastapi import APIRouter
from backend.models.schemas import ChatRequest
from backend.utils.prompt_builder import build_prompt
from backend.services.ollama_service import generate
from backend.services.memory_service import save_message, clear_session

router = APIRouter()


@router.post("/chat")
def chat(req: ChatRequest):
    prompt = build_prompt(req.session_id, req.message)

    answer = generate(prompt, req.model)

    save_message(req.session_id, req.message, answer)

    return {"response": answer}


@router.delete("/chat/{session_id}")
def delete_session(session_id: str):
    clear_session(session_id)
    return {"status": "cleared"}