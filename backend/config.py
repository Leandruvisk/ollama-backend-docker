import os

class Settings:
    OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
    DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "llama3")

    NUM_PREDICT = int(os.getenv("NUM_PREDICT", 100))
    TEMPERATURE = float(os.getenv("TEMPERATURE", 0.2))

    SYSTEM_PROMPT = (
        "Você é um assistente técnico.\n"
        "Responda sempre em português do Brasil.\n"
        "Seja direto e objetivo.\n"
        "NÃO invente contexto.\n"
        "NÃO faça suposições.\n"
        "Responda apenas com base no histórico fornecido.\n"
        "Se não souber, diga que não sabe.\n"
        "NÃO faça comentários extras.\n"
    )

settings = Settings()