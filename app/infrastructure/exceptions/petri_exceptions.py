
class MissingApiKeyError(Exception):
    """Raised when the API key is missing or invalid"""

    def __init__(self, message: str, details: dict | None = None):
        super().__init__(message)
        self.details = details or {}

class InvalidFileExtensionError(ValueError):
    """Raised when provided file type or extension is invalid"""

    def __init__(self, message: str, details: dict | None = None):
        super().__init__(message)
        self.details = details or {}