from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from app.api.router import router as api_router
from app.front.routers import router as front_router


app = FastAPI()

app.include_router(api_router)
app.include_router(front_router)

origins = [
    'http://localhost:8000', 'http://0.0.0.0', 'http://alex.pozharsite.ru',
    "http://db.pozharsite.ru", "http://127.0.0.1:8000"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["POST", "GET", "PUT", "DELETE"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="app/front/static"), name="static")



