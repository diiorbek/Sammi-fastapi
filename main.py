from fastapi import FastAPI
from src.api import main_router as main_api
import uvicorn

main_app = FastAPI()

main_app.include_router(main_api)

if __name__ == "__main__":
    uvicorn.run("main:main_app" , reload=True)