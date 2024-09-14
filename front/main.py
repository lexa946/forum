from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from routers.main import router

app = FastAPI()

app.include_router(router)

app.mount('/forum/static/', StaticFiles(directory='static'), 'static')
