import logging
from typing import Awaitable, Callable

from api import router as api_router
from core.settings import settings
from fastapi import FastAPI, Request, Response
from fastapi.responses import ORJSONResponse


app = FastAPI(default_response_class=ORJSONResponse)

app.include_router(api_router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )
