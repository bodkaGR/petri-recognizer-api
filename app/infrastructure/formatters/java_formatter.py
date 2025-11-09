from typing import override

import jinja2

from app.domain.enums.file_format import FileExtension
from app.domain.enums.petrinet_format import PetriNetExtension
from app.domain.interfaces.i_formatter import IFormatter
from app.domain.models.petri_model import PetriModel
from config.path_config import TEMPLATES_DIR


class JavaFormatter(IFormatter):
    @property
    @override
    def media_type(self) -> str:
        return "text/x-java-source"

    @override
    def format(self, model: PetriModel) -> str:
        # Loading templates
        template_loader = jinja2.FileSystemLoader(searchpath=TEMPLATES_DIR)
        template_env = jinja2.Environment(loader=template_loader)

        template = template_env.get_template(f"template.{PetriNetExtension.JAVA_METHOD}.jinja")

        # Rendering model into petriobj
        rendered_model_petriobj = template.render(model.to_petriobj_dict())
        return rendered_model_petriobj
