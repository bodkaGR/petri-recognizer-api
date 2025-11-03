from fastapi import FastAPI
from app.controllers.recognize_controller import router as recognize_router
from app.infrastructure.handlers.exception_handlers import register_exception_handlers

app = FastAPI(title="Petri nets recognizer FastAPI", version="0.1")

# API routes
app.include_router(recognize_router, prefix="/api")

# Exception handlers register
register_exception_handlers(app)