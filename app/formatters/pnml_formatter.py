import jinja2
from typing_extensions import override

from app.domain.interfaces.i_formatter import IFormatter
from app.domain.models.petri_model import PetriModel
from config.path_config import TEMPLATES_DIR, get_output_file_path


class PNMLFormatter(IFormatter):
    """
    Format the PetriModel into a pnml file and return the path to the output file
    """

    def __init__(self):
        self.file_type = "pnml"

    @property
    @override
    def media_type(self) -> str:
        return "application/xml"

    @override
    def format(self, model: PetriModel) -> str:
        # Loading templates
        template_loader = jinja2.FileSystemLoader(searchpath=TEMPLATES_DIR)
        template_env = jinja2.Environment(loader=template_loader)
        template = template_env.get_template(f"template.{self.file_type}.jinja")

        # Rendering PNML text
        output_text = template.render(
            {"places": model.places, "transitions": model.transitions, "arcs": model.arcs}
        )

        # Get path to output file
        output_file_path = get_output_file_path(f"output.{self.file_type}")

        # Write to file
        with open(output_file_path, "w", encoding="utf-8") as f:
            f.write(output_text)

        return output_file_path