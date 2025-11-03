from enum import StrEnum, unique
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
    def is_valid(cls, value: str) -> bool:
        return value.lower().strip() in [f.value for f in cls]