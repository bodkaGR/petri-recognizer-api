from fastapi import Request
from fastapi.responses import JSONResponse
from app.infrastructure.exceptions.petri_exceptions import InvalidFileExtensionError


def register_exception_handlers(app):

    @app.exception_handler(InvalidFileExtensionError)
    async def invalid_file_format_handler(request: Request, exc: InvalidFileExtensionError) -> JSONResponse:
        return JSONResponse(
            status_code=400,
            content={
                "error": exc.__class__.__name__,
                "message": str(exc),
                "details": exc.details,
            },
        )