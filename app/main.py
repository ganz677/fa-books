import logging
from typing import Awaitable, Callable

from api import router as api_router
from core.settings import settings
from fastapi import FastAPI, Request, Response
from fastapi.responses import ORJSONResponse

logging.basicConfig(
    level=settings.logging.log_level_value,
    format=settings.logging.log_format,
)

log = logging.getLogger(__name__)

app = FastAPI(default_response_class=ORJSONResponse)

app.include_router(api_router)


@app.middleware("http")
async def log_new_request(
    request: Request, call_next: Callable[[Request], Awaitable[Response]]
) -> Response:
    log.info("Request %s to %s", request.method, request.url)
    return await call_next(request)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )
