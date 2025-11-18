from dataclasses import dataclass
from typing import List

from app.domain.models.models import Place, Transition, Arc


@dataclass
class PetriModel:
    """
    Domain entity representing a recognized Petri net model
    Encapsulates recognized structural elements
    """
    places: List[Place]
    transitions: List[Transition]
    arcs: List[Arc]

    def summary(self) -> str:
        """Return a short summary of the model"""
        return (
            f"PetriModel("
            f"places={len(self.places)}, "
            f"transitions={len(self.transitions)}, "
            f"arcs={len(self.arcs)})"
        )

    def to_dict(self) -> dict:
        """Convert model to a serializable dictionary"""
        return {
            "places": [p.to_dict() for p in self.places],
            "transitions": [t.to_dict() for t in self.transitions],
            "arcs": [a.to_dict() for a in self.arcs],
        }

    def to_pnml_dict(self) -> dict:
        return {
            "places": self.places,
            "transitions": self.transitions,
            "arcs": self.arcs
        }

    def to_petriobj_dict(self) -> dict:
        """Convert model to a dictionary for petriobj template"""
        place_to_index = {p.id: i for i, p in enumerate(self.places)}
        transition_to_index = {t.id: i for i, t in enumerate(self.transitions)}
        return {
            "places": self.places,
            "transitions": self.transitions,
            "arcs": self.arcs,
            "place_to_index": place_to_index,
            "transition_to_index": transition_to_index,
        }