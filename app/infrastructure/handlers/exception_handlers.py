from fastapi import Request
from fastapi.responses import JSONResponse
from app.infrastructure.exceptions.petri_exceptions import MissingApiKeyError, InvalidFileFormatError


def register_exception_handlers(app):

    @app.exception_handler(MissingApiKeyError)
    async def missing_api_key_handler(request: Request, exc: MissingApiKeyError) -> JSONResponse:
        return JSONResponse(
            status_code=400,
            content={
                "error": exc.__class__.__name__,
                "message": str(exc),
            },
        )

    @app.exception_handler(InvalidFileFormatError)
    async def invalid_file_format_handler(request: Request, exc: InvalidFileFormatError) -> JSONResponse:
        return JSONResponse(
            status_code=400,
            content={
                "error": exc.__class__.__name__,
                "message": str(exc),
                "details": exc.details,
            },
        )