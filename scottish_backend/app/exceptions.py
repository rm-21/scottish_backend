from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from ..api import Response


async def http_exception_handler(
    request: Request, exc: StarletteHTTPException
) -> JSONResponse:
    return JSONResponse(
        content=Response(
            status_code=exc.status_code,
            error=True,
            msg={"error": exc.detail},
        ).model_dump(),
        status_code=exc.status_code,
    )


async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    errors: dict[int | str, str] = {}
    for error in exc.errors():
        field = error["loc"][1]  # get field name
        message = error["msg"]  # get error message
        errors[field] = message
    return JSONResponse(
        content=Response(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            msg=errors,
            error=True,
        ).model_dump(),
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    )
