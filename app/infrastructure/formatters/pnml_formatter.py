import jinja2
from typing_extensions import override

from app.domain.enums.petrinet_format import PetriNetExtension
from app.domain.interfaces.i_formatter import IFormatter
from app.domain.models.petri_model import PetriModel
from app.domain.enums.file_format import FileExtension
from config.path_config import TEMPLATES_DIR


class PNMLFormatter(IFormatter):
    """Format the PetriModel into a pnml"""

    @property
    @override
    def media_type(self) -> str:
        return "application/xml"

    @override
    def format(self, model: PetriModel) -> str:
        # Loading templates
        template_loader = jinja2.FileSystemLoader(searchpath=TEMPLATES_DIR)
        template_env = jinja2.Environment(loader=template_loader)
        template = template_env.get_template(f"template.{PetriNetExtension.PNML}.jinja")

        # Rendering model into PNML
        rendered_model_pnml = template.render(model.to_pnml_dict())
        return rendered_model_pnml