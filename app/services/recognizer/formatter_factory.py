from app.domain.enums.petrinet_format import PetriNetExtension
from app.domain.interfaces.i_formatter import IFormatter
from app.domain.enums.file_format import FileExtension
from app.infrastructure.exceptions.petri_exceptions import InvalidFileExtensionError
from app.infrastructure.formatters.java_formatter import JavaFormatter
from app.infrastructure.formatters.pnml_formatter import PNMLFormatter


class FormatterFactory:
    """Factory Method for creating formatter strategy"""

    @staticmethod
    def create(file_extension: PetriNetExtension) -> IFormatter:
        match file_extension:
            case PetriNetExtension.PNML:
                return PNMLFormatter()
            case PetriNetExtension.JAVA_METHOD:
                return JavaFormatter()
            case _:
                raise InvalidFileExtensionError(f"Unsupported file type for factory: {file_extension.value}")