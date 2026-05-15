from fastapi import FastAPI

from app.database import Base, engine

from app.routers import upload
from app.routers import chat
from app.routers import status

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(upload.router)
app.include_router(chat.router)
app.include_router(status.router)