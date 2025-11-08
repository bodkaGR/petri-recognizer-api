from contourpy.util import renderer
from typing_extensions import override

from app.domain.enums.file_format import FileFormat
from app.domain.interfaces.i_parser import IParser
from app.domain.interfaces.i_renderer import IRenderer
from app.domain.interfaces.i_renderer_service import IRendererService
from app.domain.interfaces.i_repository import IRepository
from app.domain.models.petri_model import PetriModel
from app.services.recognizer.formatter_factory import FormatterFactory
from app.services.renderer.parser_factory import ParserFactory


class RendererService(IRendererService):

    def __init__(self, renderer: IRenderer, repository: IRepository):
        self.renderer = renderer
        self.repository = repository

    @override
    def render_to_image(self, file_path: str, file_format: FileFormat) -> str:
        # 1. Parse received file to PetriModel
        parser = ParserFactory.create(file_format)
        model = parser.parse(file_path)

        # 2. Render model to image
        rendered_model_output_path = self.renderer.render(model)
        return rendered_model_output_path