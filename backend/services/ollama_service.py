import requests
from backend.config import settings


def generate(prompt: str, model: str):
    payload = {
        "model": model or settings.DEFAULT_MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {
            "num_predict": settings.NUM_PREDICT,
            "temperature": settings.TEMPERATURE
        }
    }

    response = requests.post(
        f"{settings.OLLAMA_URL}/api/generate",
        json=payload,
        timeout=60
    )

    data = response.json()

    return data.get("response")