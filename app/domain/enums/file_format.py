import os
from enum import StrEnum, unique

from sympy.physics.quantum.gate import normalized

from app.infrastructure.exceptions.petri_exceptions import InvalidFileFormatError


@unique
class FileFormat(StrEnum):
    PNML = "pnml"
    JAVA_METHOD = "petriobj"

    @classmethod
    def from_string(cls, value: str) -> "FileFormat":
        normalized = value.lower().strip()
        for fmt in cls:
            if fmt.value == normalized:
                return fmt
        raise InvalidFileFormatError(f"Unsupported file format: {value}", details={"allowed": [f.value for f in cls]})

    @classmethod
    def from_file_path(cls, file_path: str) -> "FileFormat":
        _, ext = os.path.splitext(file_path)
        extension = ext.lstrip(".").lower()
        for fmt in cls:
            if fmt.value == extension:
                return fmt
        raise InvalidFileFormatError(f"Unsupported file format: {file_path}", details={"allowed": [f.value for f in cls]})

    @classmethod
    def is_valid_extension(cls, filename: str) -> bool:
        _, ext = os.path.splitext(filename)
        extension = ext.lstrip(".").lower()
        return extension in [f.value for f in cls]