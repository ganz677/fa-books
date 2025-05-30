import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from app.api import router as api_router

app = FastAPI(default_response_class=ORJSONResponse)

app.include_router(api_router)

@app.get('/')
async def greetings():
    return {
        'message': 'hello!'
    }
