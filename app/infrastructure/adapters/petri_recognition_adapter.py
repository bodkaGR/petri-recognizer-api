from app.domain.models.petri_model import PetriModel
from app.pipeline.workflow import recognize_graph


class PetriRecognitionAdapter:
    """Adapter for integrating sketch2pnml library"""

    def get_petri_net(self, image_path: str, config_path: str) -> PetriModel:
        result = recognize_graph(image_path, config_path)

        return PetriModel(
            places=result["places"],
            transitions=result["transitions"],
            arcs=result["arcs"],
        )