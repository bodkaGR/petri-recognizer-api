import os

from fastapi import APIRouter, UploadFile, File, HTTPException, Query
from fastapi.responses import FileResponse

from app.infrastructure.handlers.file_handler import FileHandler
from app.domain.enums.file_format import FileFormat
from app.infrastructure.adapters.petri_recognition_adapter import PetriRecognitionAdapter
from app.services.recognizer.recognition_facade import RecognitionFacade
from app.services.recognizer.recognizer_service import RecognizerService
from app.infrastructure.repositories.pickle_repository import PickleRepository

router = APIRouter()

@router.post("/recognize")
async def recognize(
        image: UploadFile = File(...),
        config: UploadFile = File(...),
        requested_file_type: str = Query(default=..., description="Output file type: pnml, json, or petriobj")
):
    """
    Recognize a Petri net from an uploaded image and configuration file
    Returns generated Petri net file in the requested format
    """

    try:
        # Dependency initialization
        file_handler = FileHandler()
        adapter = PetriRecognitionAdapter()
        repository = PickleRepository()

        recognizer = RecognizerService(adapter, repository, file_handler)
        facade = RecognitionFacade(recognizer, file_handler)

        output_path, media_type = await facade.recognize_from_uploads(image, config, requested_file_type)

        return FileResponse(
            output_path,
            media_type=media_type,
            filename=f"recognized_model.{requested_file_type}"
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Recognition failed: {str(e)}")