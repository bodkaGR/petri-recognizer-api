from datetime import datetime

import httpx
from fastapi import APIRouter, UploadFile, File, Query, Header, HTTPException
from fastapi.params import Depends
from fastapi.responses import FileResponse

from app.infrastructure.exceptions.petri_exceptions import MissingApiKeyError
from app.infrastructure.adapters.petri_recognition_adapter import PetriRecognitionAdapter
from app.infrastructure.providers.api_key_provider import ApiKeyProvider
from app.services.recognizer.recognition_facade import RecognitionFacade
from app.services.recognizer.recognizer_service import RecognizerService
from app.infrastructure.repositories.pickle_repository import PickleRepository
from app.services.renderer.petri_model_renderer import PetriModelRenderer
from app.services.renderer.render_facade import RenderFacade
from app.services.renderer.renderer_service import RendererService

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

def get_render_facade() -> RenderFacade:
    renderer = PetriModelRenderer()
    pickle_repository = PickleRepository()
    renderer_service = RendererService(renderer, pickle_repository)
    return RenderFacade(renderer_service)

@router.post("/recognize")
async def recognize(
        image: UploadFile = File(...),
        config: UploadFile = File(...),
        requested_file_type: str = Query(default=..., description="Output file type: pnml or petriobj"),
        facade: RecognitionFacade = Depends(get_recognition_facade),
) -> FileResponse:
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

@router.post("/render")
async def render(
        file: UploadFile = File(...),
        facade: RenderFacade = Depends(get_render_facade),
) -> FileResponse:

    output_path = await facade.render_from_upload(file)

    return FileResponse(
        f"{output_path}.png",
        media_type="image/png",
        filename="rendered_petri_net.png"
    )

@router.get("/health")
async def health(api_key: str = Header(..., alias="X-Roboflow-API-Key")):
    url = f"https://api.roboflow.com/account?api_key={api_key}"

    async with httpx.AsyncClient(timeout=5) as client:
        try:
            response = await client.get(url)
            if response.status_code != 200:
                raise HTTPException(status_code=401, detail="Invalid Roboflow API key")
        except httpx.RequestError:
            raise HTTPException(status_code=503, detail="Cannot reach Roboflow API")

    return {
        "status": "ok",
        "roboflow_key_valid": True
    }