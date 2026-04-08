import os

class Settings:
    DEFAULT_MODEL = "llama3:latest"
    OLLAMA_URL = "http://ollama:11434"
    # DATABASE_URL = os.getenv(
    #     "DATABASE_URL",
    #     "postgresql://postgres:postgres@localhost:5432/chatdb"
    # )
    # DATABASE_URL = "postgresql://chatuser:chatpass@localhost:5432/chatdb"
    DATABASE_URL = "postgresql://chatuser:chatpass@postgres-chat:5432/chatdb"
    NUM_PREDICT: int = 100
    TEMPERATURE: float = 0.2

settings = Settings()


