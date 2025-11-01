from abc import ABC, abstractmethod

from app.domain.models.petri_model import PetriModel


class IFormatter(ABC):
    @property
    @abstractmethod
    def media_type(self) -> str:
        pass

    @abstractmethod
    def format(self, model: PetriModel) -> str:
        """Convert model into chosen format file and return its path"""
        pass