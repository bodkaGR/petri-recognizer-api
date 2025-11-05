from abc import ABC, abstractmethod

from app.domain.models.petri_model import PetriModel


class IRenderer(ABC):

    @abstractmethod
    def render(self, model: PetriModel) -> str: ...