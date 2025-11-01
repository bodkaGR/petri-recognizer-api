from fastapi import FastAPI
from app.controllers.recognize_controller import router as recognize_router

app = FastAPI(title="Petri nets recognizer FastAPI", version="0.1")

app.include_router(recognize_router, prefix="/api")