from fastapi import FastAPI

from routers.main import router

app = FastAPI()

app.include_router(router)
