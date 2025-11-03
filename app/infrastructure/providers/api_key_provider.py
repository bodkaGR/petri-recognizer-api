
class ApiKeyProvider:
    """
    Centralized provider for managing per-request Roboflow API keys
    """

    def __init__(self, api_key: str):
        self.__api_key = api_key

    @property
    def api_key(self) -> str:
        return self.__api_key