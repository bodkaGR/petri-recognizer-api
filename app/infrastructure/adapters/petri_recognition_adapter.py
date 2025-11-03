from app.domain.models.petri_model import PetriModel
from app.infrastructure.providers.api_key_provider import ApiKeyProvider
from app.pipeline.workflow import recognize_graph


class PetriRecognitionAdapter:
    """Adapter for integrating sketch2pnml library"""

    def __init__(self, api_key_provider: ApiKeyProvider):
        self.api_key_provider = api_key_provider

    def get_petri_net(self, image_path: str, config_path: str) -> PetriModel:
        api_key = self.api_key_provider.api_key
        result = recognize_graph(image_path, config_path, api_key)

        return PetriModel(
            places=result["places"],
            transitions=result["transitions"],
            arcs=result["arcs"],
        )