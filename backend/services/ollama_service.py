import requests
from backend.config import settings


def generate(prompt: str, model: str):
    model = model or "llama3:latest"

    # 🔥 normaliza
    if model == "llama3":
        model = "llama3:latest"

    payload = {
        "model": model,
        "prompt": prompt,
        "stream": True,
        "options": {
            "num_predict": settings.NUM_PREDICT,
            "temperature": settings.TEMPERATURE
        }
    }


    response = requests.post(
        "http://ollama:11434/api/generate",
        json=payload,
        timeout=60
    )

    data = response.json()

    print("DEBUG:", data)

    return data.get("response")