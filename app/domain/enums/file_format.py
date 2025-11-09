import os
from enum import StrEnum

from app.infrastructure.exceptions.petri_exceptions import InvalidFileExtensionError


class FileExtension(StrEnum):

    @classmethod
    def from_string(cls, value: str) -> "FileExtension":
        normalized = value.lower().strip()
        for fmt in cls:
            if fmt.value == normalized:
                return fmt
        raise InvalidFileExtensionError(f"Unsupported file extension: {value}", details={"allowed": [e.value for e in cls]})

    @classmethod
    def from_file_path(cls, file_path: str) -> "FileExtension":
        _, ext = os.path.splitext(file_path)
        extension = ext.lstrip(".").lower()
        for fmt in cls:
            if fmt.value == extension:
                return fmt
        raise InvalidFileExtensionError(f"Unsupported file extension: {file_path}", details={"allowed": [e.value for e in cls]})

    @classmethod
    def is_valid_extension(cls, filename: str) -> bool:
        _, ext = os.path.splitext(filename)
        extension = ext.lstrip(".").lower()
        return extension in [f.value for f in cls]