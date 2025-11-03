from app.domain.interfaces.i_formatter import IFormatter
from app.domain.enums.file_format import FileFormat
from app.infrastructure.exceptions.petri_exceptions import InvalidFileFormatError
from app.infrastructure.formatters.java_formatter import JavaFormatter
from app.infrastructure.formatters.pnml_formatter import PNMLFormatter


class FormatterFactory:
    """Factory Method for creating formatter strategy"""

    @staticmethod
    def create(file_format: FileFormat) -> IFormatter:
        match file_format:
            case FileFormat.PNML:
                return PNMLFormatter()
            case FileFormat.JAVA_METHOD:
                return JavaFormatter()
            case _:
                raise InvalidFileFormatError(f"Unsupported file type for factory: {file_format.value}")