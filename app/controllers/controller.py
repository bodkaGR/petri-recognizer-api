from functools import lru_cache
from typing import Literal

from fastapi import APIRouter, UploadFile, File, Query
from fastapi.params import Depends
from fastapi.responses import FileResponse

from app.infrastructure.adapters.petri_recognition_adapter import PetriRecognitionAdapter
from app.services.recognizer.recognition_facade import RecognitionFacade
from app.services.recognizer.recognizer_service import RecognizerService
from app.infrastructure.repositories.pickle_repository import PickleRepository
from app.services.renderer.petri_model_renderer import PetriModelRenderer
from app.services.renderer.render_facade import RenderFacade
from app.services.renderer.renderer_service import RendererService

router = APIRouter()

# =========================
# Dependency Injection
# =========================

@lru_cache
def get_recognition_facade() -> RecognitionFacade:
    # Dependency initialization
    repository = PickleRepository()
    adapter = PetriRecognitionAdapter()
    recognizer = RecognizerService(adapter, repository)
    return RecognitionFacade(recognizer)

@lru_cache
def get_render_facade() -> RenderFacade:
    renderer = PetriModelRenderer()
    pickle_repository = PickleRepository()
    renderer_service = RendererService(renderer, pickle_repository)
    return RenderFacade(renderer_service)

# =========================
# Endpoints
# =========================

@router.post("/recognize", summary="Recognize a Petri net from an uploaded image")
async def recognize(
        image: UploadFile = File(..., description="Petri net image (.png, .jpg)"),
        config: UploadFile = File(..., description="YAML configuration for recognition"),
        requested_file_type: Literal["pnml", "petriobj"] = Query(default=..., description="Output file type: pnml or petriobj"),
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

@router.post("/render", summary="Render a Petri net model to PNG")
async def render(
        file: UploadFile = File(..., description="PNML or PetriObj file"),
        facade: RenderFacade = Depends(get_render_facade),
) -> FileResponse:

    output_path = await facade.render_from_upload(file)

    return FileResponse(
        f"{output_path}.png",
        media_type="image/png",
        filename="rendered_petri_net.png"
    )

@router.get("/health", status_code=200, summary="Health check endpoint")
async def health():
    return {
        "status": "ok",
    }