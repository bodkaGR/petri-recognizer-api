from typing_extensions import override

from app.domain.interfaces.i_parser import IParser
from app.domain.models.petri_model import PetriModel


class JavaParser(IParser):

    @override
    def parse(self, file_path: str) -> PetriModel:
        # TODO: implement java method parser
        pass