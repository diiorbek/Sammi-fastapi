from fastapi import FastAPI
from api import main_router as main_api


def create_app():
    app = FastAPI()

    app.include_router(
        router=main_api,
        prefix="/api",
    )

    return app
