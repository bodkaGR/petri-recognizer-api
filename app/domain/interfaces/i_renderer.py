from abc import ABC, abstractmethod

from app.domain.models.petri_model import PetriModel


class IRenderer(ABC):
    @abstractmethod
    def render(self, model: PetriModel, output_path: str) -> str:
        """Render model as an image and return path to file"""
        pass