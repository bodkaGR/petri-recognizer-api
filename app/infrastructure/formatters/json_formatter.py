from typing_extensions import override

from app.domain.interfaces.i_formatter import IFormatter
from app.domain.models.petri_model import PetriModel


class JSONFormatter(IFormatter):
    @property
    @override
    def media_type(self) -> str:
        # TODO: add media type for json file type
        pass

    @override
    def format(self, model: PetriModel) -> str:
        # TODO: implement formatting in json
        pass