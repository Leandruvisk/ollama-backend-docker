from fastapi import FastAPI
from backend.db.database import engine, Base
from backend.db import models
from backend.routes.chat import router as chat_router

app = FastAPI()
Base.metadata.create_all(bind=engine)
app.include_router(chat_router)