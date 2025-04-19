from api import router as api_router
from fastapi import FastAPI
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