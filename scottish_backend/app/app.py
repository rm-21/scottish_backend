import time
from typing import Any, Awaitable, Callable

from fastapi import FastAPI, Request, Response
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException

from ..api import api_router
from ..core import settings
from .exceptions import http_exception_handler, validation_exception_handler

app = FastAPI(title=settings.PROJECT_NAME)
app.include_router(api_router)


origins = [
    "127.0.0.1:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)


@app.middleware("http")
async def add_process_time_header(
    request: Request, call_next: Callable[[Request], Awaitable[Any]]
) -> Response:
    start_time: float = time.time()
    response: Response = await call_next(request)
    process_time: float = (time.time() - start_time) * 100
    response.headers["X-Process-Time"] = str(process_time) + " ms"
    return response


@app.get("/ping")
async def ping() -> dict[str, bool]:
    return {"ok": True}
