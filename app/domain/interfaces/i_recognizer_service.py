from abc import ABC, abstractmethod

from starlette.responses import FileResponse


class IRecognizerService(ABC):
    """Run recognition pipeline and return PetriModel"""

    @abstractmethod
    def recognize(self, image_path: str, config_path: str, file_type: str) -> FileResponse: ...