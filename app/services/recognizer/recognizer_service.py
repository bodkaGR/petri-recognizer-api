from typing import override
from starlette.responses import FileResponse
from app.domain.interfaces.i_recognizer_service import IRecognizerService
from app.domain.interfaces.i_repository import IRepository
from app.services.recognizer.formatter_factory import FormatterFactory
from app.services.recognizer.pipeline_adapter import PetriRecognitionAdapter


class RecognizerService(IRecognizerService):

    def __init__(self, adapter: PetriRecognitionAdapter, repository: IRepository, formatter_factory: FormatterFactory):
        self.adapter = adapter
        self.repository = repository
        self.formatter_factory = formatter_factory

    @override
    def recognize(self, image_path: str, config_path: str, file_type: str) -> FileResponse:
        # 1. Calling adapter for recognition
        model = self.adapter.getPetriNet(image_path, config_path)

        # 2. Saving model
        self.repository.save(model)

        # 3. Formatting in requested file type
        formatter = self.formatter_factory.create(file_type)
        output_path = formatter.format(model)

        # 4. Return file of requested type with Petri net
        return FileResponse(
            output_path,
            media_type=formatter.media_type,
            filename=f"recognized_model.{file_type}"
        )