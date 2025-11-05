from fastapi import UploadFile

from app.domain.enums.file_format import FileFormat
from app.domain.interfaces.i_recognizer_service import IRecognizerService
from app.infrastructure.handlers.file_handler import FileHandler


class RecognitionFacade:
    """Orchestrates recognition workflow"""

    def __init__(self, recognizer_service: IRecognizerService):
        self.recognizer_service = recognizer_service

    async def recognize_from_uploads(self, image: UploadFile, config: UploadFile, requested_file_type: str):
        # Get file format from requested file type
        file_format = FileFormat.from_string(requested_file_type)

        # Saving uploaded temporary files
        image_path = FileHandler.save_upload_tmp(image, ".png") # TODO: add support of different image formats
        config_path = FileHandler.save_upload_tmp(config, ".yaml")

        try:
            output_path, media_type = self.recognizer_service.recognize(image_path, config_path, file_format)
            return output_path, media_type
        finally:
            # Deleting temporary files
            for path in [image_path, config_path]:
                FileHandler.delete_upload_tmp(path)