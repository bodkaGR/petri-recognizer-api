from abc import abstractmethod, ABC

from app.domain.models.petri_model import PetriModel


class IParser(ABC):

    @abstractmethod
    def parse(self, file_path: str) -> PetriModel: ...