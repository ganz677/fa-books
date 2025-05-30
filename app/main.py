import uvicorn

from app.api import router as api_router
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

app = FastAPI(default_response_class=ORJSONResponse)

app.include_router(api_router)

@app.get('/')
async def greetings():
    return {
        'message': 'hello!'
    }

