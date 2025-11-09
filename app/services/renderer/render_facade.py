from fastapi import UploadFile

from app.domain.enums.file_format import FileExtension
from app.domain.enums.petrinet_format import PetriNetExtension
from app.domain.interfaces.i_renderer_service import IRendererService
from app.infrastructure.handlers.file_handler import FileHandler


class RenderFacade:

    def __init__(self, renderer_service: IRendererService):
        self.renderer_service = renderer_service

    async def render_from_upload(self, file: UploadFile):
        # 1. Get file extension enum value of received file
        file_extension = PetriNetExtension.from_file_path(file.filename)

        # 2. Save received file to temporary location
        file_path = FileHandler.save_upload_tmp(file, ".".join(file_extension.value))

        try:
            # 3. Render uploaded file to image
            output_path = self.renderer_service.render_to_image(file_path, file_extension)
            return output_path
        finally:
            FileHandler.delete_upload_tmp(file_path)