from app.domain.enums.petrinet_format import PetriNetExtension
from app.domain.interfaces.i_parser import IParser
from app.infrastructure.exceptions.petri_exceptions import InvalidFileExtensionError
from app.infrastructure.parsers.java_parser import JavaParser
from app.infrastructure.parsers.pnml_parser import PNMLParser


class ParserFactory:
    @staticmethod
    def create(file_extension: PetriNetExtension) -> IParser:
        match file_extension:
            case PetriNetExtension.PNML:
                return PNMLParser()
            case PetriNetExtension.JAVA_METHOD:
                return JavaParser()
            case _:
                raise InvalidFileExtensionError(f"Unsupported file type for factory: {file_extension.value}")