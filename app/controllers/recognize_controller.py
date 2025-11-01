import os
import shutil
import tempfile

from fastapi import APIRouter, UploadFile, File, HTTPException, Query

from app.services.recognizer.formatter_factory import FormatterFactory
from app.services.recognizer.pipeline_adapter import PetriRecognitionAdapter
from app.services.recognizer.recognizer_service import RecognizerService
from app.services.recognizer.repository import PickleRepository

router = APIRouter()

@router.post("/recognize")
async def recognize(
        image: UploadFile = File(...),
        config: UploadFile = File(...),
        file_type: str = Query(default=..., description="Output file type: pnml, json, or petriobj")
):
    """
    Recognize a Petri net from an uploaded image and configuration file
    Returns generated Petri net file in the requested format
    """

    # Saving temporary files
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_img:
        shutil.copyfileobj(image.file, tmp_img)
        image_path = tmp_img.name

    with tempfile.NamedTemporaryFile(delete=False, suffix=".yaml") as tmp_cfg:
        shutil.copyfileobj(config.file, tmp_cfg)
        config_path = tmp_cfg.name

    try:
        service = RecognizerService(
            adapter=PetriRecognitionAdapter(),
            repository=PickleRepository(),
            formatter_factory=FormatterFactory()
        )

        file_response = service.recognize(image_path, config_path, file_type)
        return file_response
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Recognition failed: {str(e)}")
    finally:
        # Deleting temporary files
        for path in [image_path, config_path]:
            try:
                if path and os.path.exists(path):
                    os.remove(path)
            except Exception:
                pass