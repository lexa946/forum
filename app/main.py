from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from app.threads.routers import router as thread_router
from app.comments.routers import router as comment_router
from app.front.routers import router as front_router


app = FastAPI()

app.include_router(thread_router)
app.include_router(comment_router)
app.include_router(front_router)

origins = [
    'http://localhost:8000', 'http://0.0.0.0', 'http://alex.pozharsite.ru',
    "http://db.pozharsite.ru"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["POST", "GET", "PUT", "DELETE"],
    allow_headers=["*"],
)

app.mount("/forum/static", StaticFiles(directory="app/front/static"), name="static")



