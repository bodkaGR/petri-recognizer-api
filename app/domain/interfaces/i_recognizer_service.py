from abc import ABC, abstractmethod

from starlette.responses import FileResponse


class IRecognizerService(ABC):
    """Run recognition pipeline, return path to output file and media type"""

    @abstractmethod
    def recognize(self, image_path: str, config_path: str, file_type: str) -> tuple[str, str]: ...