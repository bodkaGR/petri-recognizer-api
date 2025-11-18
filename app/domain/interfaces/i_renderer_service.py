from abc import abstractmethod, ABC

from app.domain.enums.petrinet_format import PetriNetExtension


class IRendererService(ABC):

    @abstractmethod
    def render_to_image(self, file_path: str, file_extension: PetriNetExtension) -> str: ...