from typing import override

from app.domain.interfaces.i_formatter import IFormatter
from app.domain.models.petri_model import PetriModel


class JavaFormatter(IFormatter):
    @property
    @override
    def media_type(self) -> str:
        # TODO: add media type for Java method file type
        pass

    @override
    def format(self, model: PetriModel) -> str:
        # TODO: implement formatting Java method
        pass
