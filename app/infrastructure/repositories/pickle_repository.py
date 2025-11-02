import pickle
import os
from typing import override

from app.domain.interfaces.i_repository import IRepository
from app.domain.models.petri_model import PetriModel
from config.path_config import PLACES_PKL_PATH, TRANSITIONS_PKL_PATH, ARCS_PKL_PATH, ensure_directories_exist

class PickleRepository(IRepository):
    """Handles serialization and deserialization"""

    @override
    def save(self, model: PetriModel):
        ensure_directories_exist()
        with open(PLACES_PKL_PATH, "wb") as f:
            pickle.dump(model.places, f)
        with open(TRANSITIONS_PKL_PATH, "wb") as f:
            pickle.dump(model.transitions, f)
        with open(ARCS_PKL_PATH, "wb") as f:
            pickle.dump(model.arcs, f)

    @override
    def load(self) -> PetriModel:
        with open(PLACES_PKL_PATH, "rb") as f:
            places = pickle.load(f)
        with open(TRANSITIONS_PKL_PATH, "rb") as f:
            transitions = pickle.load(f)
        with open(ARCS_PKL_PATH, "rb") as f:
            arcs = pickle.load(f)
        return PetriModel(places, transitions, arcs)