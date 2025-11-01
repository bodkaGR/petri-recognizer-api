from abc import ABC, abstractmethod

from app.domain.models.petri_model import PetriModel


class IRepository(ABC):
    @abstractmethod
    def save(self, model: PetriModel): ...
    @abstractmethod
    def load(self) -> PetriModel: ...
