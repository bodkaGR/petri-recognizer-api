import json

from typing_extensions import override

from app.domain.interfaces.i_formatter import IFormatter
from app.domain.models.petri_model import PetriModel


class JSONFormatter(IFormatter):
    @property
    @override
    def media_type(self) -> str:
        return "application/json"

    @override
    def format(self, model: PetriModel) -> str:
        # Get dictionary representation of the model
        model_dict = model.to_dict()

        # Convert model to JSON string
        json_model = json.dumps(model_dict, indent=4, ensure_ascii=False)
        return json_model