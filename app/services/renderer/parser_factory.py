from app.domain.enums.file_format import FileFormat
from app.domain.interfaces.i_parser import IParser
from app.infrastructure.exceptions.petri_exceptions import InvalidFileFormatError
from app.infrastructure.parsers.java_parser import JavaParser
from app.infrastructure.parsers.pnml_parser import PNMLParser


class ParserFactory:
    @staticmethod
    def create(file_format: FileFormat) -> IParser:
        match file_format:
            case FileFormat.PNML:
                return PNMLParser()
            case FileFormat.JAVA_METHOD:
                return JavaParser()
            case _:
                raise InvalidFileFormatError(f"Unsupported file type for factory: {file_format.value}")