from typing import override
from app.domain.interfaces.i_recognizer_service import IRecognizerService
from app.domain.interfaces.i_repository import IRepository
from app.infrastructure.handlers.file_handler import FileHandler
from app.services.recognizer.formatter_factory import FormatterFactory
from app.domain.enums.file_format import FileFormat
from app.infrastructure.adapters.petri_recognition_adapter import PetriRecognitionAdapter
from config.path_config import get_output_file_path


class RecognizerService(IRecognizerService):
    """Main service orchestrating recognition, formatting, and export"""

    def __init__(self, adapter: PetriRecognitionAdapter, repository: IRepository, file_handler: FileHandler):
        self.adapter = adapter
        self.repository = repository
        self.file_handler = file_handler

    @override
    def recognize(self, image_path: str, config_path: str, file_format: FileFormat) -> tuple[str, str]:
        # 1. Calling adapter for recognition
        model = self.adapter.getPetriNet(image_path, config_path)

        # 2. Serialize model to pickle files
        self.repository.save(model)

        # 3. Formatting in requested file type
        formatter = FormatterFactory.create(file_format)
        formatted_model = formatter.format(model)

        # 4. Saving file with model in requested type
        output_file_path = get_output_file_path(f"output.{file_format.value}")
        saved_file_path = self.file_handler.save(formatted_model, output_file_path)

        # 4. Return tuple[saved_file_path, media_type]
        return saved_file_path, formatter.media_type