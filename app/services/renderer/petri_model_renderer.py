from typing import override

from app.domain.interfaces.i_renderer import IRenderer
from app.domain.models.petri_model import PetriModel

from graphviz import Digraph

from config.path_config import get_output_file_path


class PetriModelRenderer(IRenderer):

    @override
    def render(self, model: PetriModel) -> str:
        dot = Digraph()
        dot.attr(rankdir="LR")

        for place in model.places:
            dot.node(
                place.id,
                label=str(place.markers) if place.markers > 0 else "",
                xlabel=place.get_name() or "P",
                shape="circle",
                fixedsize="true"
            )

        for t in model.transitions:
            dot.node(
                t.id,
                label="",
                xlabel=t.get_name() or "T",
                shape="rect",
                width="0.3",
                height="0.7",
                fixedsize="true"
            )

        for arc in model.arcs:
            source_id = arc.source.id if hasattr(arc.source, "id") else arc.source
            target_id = arc.target.id if hasattr(arc.target, "id") else arc.target
            weight = arc.weight if arc.weight > 1 else ""
            dot.edge(source_id, target_id, label=str(weight))

        rendered_filename = "rendered_petri_net"
        output_path = get_output_file_path(rendered_filename)

        dot.render(filename=output_path, format="png", cleanup=True)
        return output_path