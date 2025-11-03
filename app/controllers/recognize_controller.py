from fastapi import APIRouter, UploadFile, File, HTTPException, Query, Header
from fastapi.params import Depends
from fastapi.responses import FileResponse

from app.infrastructure.exceptions.petri_exceptions import MissingApiKeyError
from app.infrastructure.handlers.file_handler import FileHandler
from app.infrastructure.adapters.petri_recognition_adapter import PetriRecognitionAdapter
from app.infrastructure.providers.api_key_provider import ApiKeyProvider
from app.services.recognizer.recognition_facade import RecognitionFacade
from app.services.recognizer.recognizer_service import RecognizerService
from app.infrastructure.repositories.pickle_repository import PickleRepository

router = APIRouter()

def get_api_key_provider(api_key: str = Header(..., alias="X-Roboflow-API-Key")) -> ApiKeyProvider:
    if not api_key:
        raise MissingApiKeyError("Missing Roboflow API Key")
    return ApiKeyProvider(api_key)

def get_recognition_facade(api_key_provider: ApiKeyProvider = Depends(get_api_key_provider)) -> RecognitionFacade:
    # Dependency initialization
    repository = PickleRepository()
    adapter = PetriRecognitionAdapter(api_key_provider)
    recognizer = RecognizerService(adapter, repository)
    return RecognitionFacade(recognizer)

@router.post("/recognize")
async def recognize(
        image: UploadFile = File(...),
        config: UploadFile = File(...),
        requested_file_type: str = Query(default=..., description="Output file type: pnml or petriobj"),
        facade: RecognitionFacade = Depends(get_recognition_facade),
):
    """
    Recognize a Petri net from an uploaded image and configuration file
    Returns generated Petri net file in the requested format
    """

    output_path, media_type = await facade.recognize_from_uploads(
        image, config, requested_file_type
    )

    return FileResponse(
        output_path,
        media_type=media_type,
        filename=f"recognized_model.{requested_file_type}"
    )
