from dataclasses import dataclass
from typing import List, Any

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
        """Convert model to a serializable dictionary for JSON or templating"""
        return {
            "places": [p.__dict__ for p in self.places],
            "transitions": [t.__dict__ for t in self.transitions],
            "arcs": [a.__dict__ for a in self.arcs],
        }