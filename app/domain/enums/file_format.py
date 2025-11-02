from enum import StrEnum, unique


@unique
class FileFormat(StrEnum):
    PNML = "pnml"
    JSON = "json"
    JAVA_METHOD = "petriobj"

    @classmethod
    def from_string(cls, value: str) -> "FileFormat":
        normalized = value.lower().strip()
        for fmt in cls:
            if fmt.value == normalized:
                return fmt
        raise ValueError(f"Unsupported file format: {value}. Allowed: {[f.value for f in cls]}")

    @classmethod
    def is_valid(cls, value: str) -> bool:
        return value.lower().strip() in [f.value for f in cls]