from fastapi import UploadFile

from app.domain.enums.image_format import ImageExtension
from app.domain.enums.petrinet_format import PetriNetExtension
from app.domain.interfaces.i_recognizer_service import IRecognizerService
from app.infrastructure.handlers.file_handler import FileHandler


class RecognitionFacade:
    """Orchestrates recognition workflow"""

    def __init__(self, recognizer_service: IRecognizerService):
        self.recognizer_service = recognizer_service

    async def recognize_from_uploads(self, image: UploadFile, config: UploadFile, requested_file_type: str):
        # Get file extension from requested file type
        requested_file_extension = PetriNetExtension.from_string(requested_file_type)

        # Get extension from input image file
        image_file_extension = ImageExtension.from_file_path(image.filename)

        # Saving uploaded temporary files
        image_path = FileHandler.save_upload_tmp(image, f".{image_file_extension.value}")
        config_path = FileHandler.save_upload_tmp(config, ".yaml") # TODO: add support of different config formats

        try:
            output_path, media_type = self.recognizer_service.recognize(image_path, config_path, requested_file_extension)
            return output_path, media_type
        finally:
            # Deleting temporary files
            for path in [image_path, config_path]:
                FileHandler.delete_upload_tmp(path)