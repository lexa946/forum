from typing import Annotated

from fastapi import APIRouter, Path, Request, HTTPException, Form
from fastapi.templating import Jinja2Templates
from starlette import status
from aiohttp import ClientSession
from starlette.responses import RedirectResponse


from schemas.main import SThreadAdd

router = APIRouter(prefix="/forum", tags=["Комментарии"])
templates = Jinja2Templates(directory='templates')


@router.get('/', name='index')
async def index(request: Request):
    async with ClientSession() as session:
        # async with session.get(f"{request.base_url}/forum/api/v1/thread/all") as response:
        async with session.get(f"http://127.0.0.1:8083/forum/api/v1/thread/all") as response:

            if response.ok:
                json_ = await response.json()

                return templates.TemplateResponse("index.html", {
                    "request": request, 'threads': json_['threads'],
                })
            else:
                raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                                    detail="Что-то с серваком! Уже чиню!")


@router.get('/{id:int}', name='thread')
async def thread(request: Request, id: Annotated[int, Path(ge=1)]):
    async with ClientSession() as session:
        async with session.get(f"http://127.0.0.1:8083/forum/api/v1/thread/{id}") as response:
            if response.ok:
                json_ = await response.json()
                return templates.TemplateResponse("thread.html", {
                    "request": request, "thread": json_['thread'],
                })

@router.get('/thread/create', name='thread_create')
async def thread_create(request: Request):
    return templates.TemplateResponse("create.html", {
        "request": request,
    })




@router.post('/thread/create', name='thread_create')
async def thread_create(request: Request, thread_add: Annotated[SThreadAdd, Form()]):
    async with ClientSession() as session:
        async with session.post(f"http://127.0.0.1:8083/forum/api/v1/thread/", json={
            "title": thread_add.title,
            "text": thread_add.text,
            "nick": thread_add.nick,
        }) as response:
            if response.ok:
                json_ = await response.json()
                return RedirectResponse(request.url_for('thread', id=json_['thread']['id']), status_code=status.HTTP_302_FOUND)
