from abc import abstractmethod, ABC

from app.domain.enums.file_format import FileFormat
from app.domain.models.petri_model import PetriModel


class IRendererService(ABC):

    @abstractmethod
    def render_to_image(self, file_path: str, file_format: FileFormat) -> str: ...