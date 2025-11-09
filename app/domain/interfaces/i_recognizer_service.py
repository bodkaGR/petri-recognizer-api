from abc import ABC, abstractmethod
from app.domain.enums.petrinet_format import PetriNetExtension


class IRecognizerService(ABC):
    """Run recognition pipeline, return path to output file and media type"""

    @abstractmethod
    def recognize(self, image_path: str, config_path: str, file_extension: PetriNetExtension) -> tuple[str, str]: ...