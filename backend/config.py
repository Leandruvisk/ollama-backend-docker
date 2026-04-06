import os

class Settings:
    OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
    # DATABASE_URL = os.getenv(
    #     "DATABASE_URL",
    #     "postgresql://postgres:postgres@localhost:5432/chatdb"
    # )
    DATABASE_URL = "postgresql://chatuser:chatpass@localhost:5432/chatdb"
    NUM_PREDICT: int = 100
    TEMPERATURE: float = 0.2

settings = Settings()