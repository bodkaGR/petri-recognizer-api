from abc import ABC, abstractmethod
from app.domain.enums.file_format import FileFormat


class IRecognizerService(ABC):
    """Run recognition pipeline, return path to output file and media type"""

    @abstractmethod
    def recognize(self, image_path: str, config_path: str, file_format: FileFormat) -> tuple[str, str]: ...