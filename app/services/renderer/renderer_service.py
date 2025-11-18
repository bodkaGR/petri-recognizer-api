from typing_extensions import override

from app.domain.enums.petrinet_format import PetriNetExtension
from app.domain.interfaces.i_renderer import IRenderer
from app.domain.interfaces.i_renderer_service import IRendererService
from app.domain.interfaces.i_repository import IRepository
from app.pipeline.converter import fix_petri_net
from app.services.renderer.parser_factory import ParserFactory


class RendererService(IRendererService):

    def __init__(self, renderer: IRenderer, repository: IRepository):
        self.renderer = renderer
        self.repository = repository

    @override
    def render_to_image(self, file_path: str, file_extension: PetriNetExtension) -> str:
        # 1. Parse received file to PetriModel
        parser = ParserFactory.create(file_extension)
        model = parser.parse(file_path)

        # 2. Fix errors in Petri Net if present
        fixed_model = fix_petri_net(model.places, model.transitions, model.arcs)

        # 2. Render model to image
        rendered_model_output_path = self.renderer.render(fixed_model)
        return rendered_model_output_path