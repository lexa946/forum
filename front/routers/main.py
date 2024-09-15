from typing import Annotated

from fastapi import APIRouter, Path, Request, HTTPException, Form
from fastapi.templating import Jinja2Templates
from starlette import status
from aiohttp import ClientSession
from starlette.responses import RedirectResponse

from filters import iso_str_date_to_format
from schemas.main import SThreadAdd, SCommentAdd

from jinja2 import Environment


router = APIRouter(prefix="/forum", tags=["Комментарии"])
templates = Jinja2Templates(directory='templates')
templates.env.filters['iso_str_date_to_format'] = iso_str_date_to_format



@router.get('/', name='index')
async def index(request: Request):
    async with ClientSession() as session:
        async with session.get(f"http://alex.pozharsite.ru/forum/api/v1/thread/all") as response:
        # async with session.get(f"http://127.0.0.1:8083/forum/api/v1/thread/all") as response:
        #     print(request.base_url)
        #     print(request.url)
        #     print(request.client.host)
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
        async with session.get(f"http://alex.pozharsite.ru/forum/api/v1/thread/{id}") as response:
        # async with session.get(f"http://127.0.0.1:8083/forum/api/v1/thread/{id}") as response:
            if response.ok:
                json_ = await response.json()
                thread = json_['thread']

        async with session.get(f"http://alex.pozharsite.ru/forum/api/v1/comment/thread", params={
        # async with session.get(f"http://127.0.0.1:8082/forum/api/v1/comment/thread", params={
            "thread_id": thread['id'],
        }) as response:
            if response.ok:
                json_ = await response.json()
                comments = json_['comments']

    return templates.TemplateResponse("thread.html", {
        "request": request, "thread": thread, "comments": comments
    })

@router.get('/thread/create', name='thread_create')
async def thread_create(request: Request):
    return templates.TemplateResponse("create.html", {
        "request": request,
    })




@router.post('/thread/create', name='thread_create')
async def thread_create(request: Request, thread_add: Annotated[SThreadAdd, Form()]):
    async with ClientSession() as session:
        # async with session.post(f"http://127.0.0.1:8083/forum/api/v1/thread/", json={
        async with session.post(f"http://{request.base_url}/forum/api/v1/thread/", json={
            "title": thread_add.title,
            "text": thread_add.text,
            "nick": thread_add.nick,
        }) as response:
            if response.ok:
                json_ = await response.json()
                return RedirectResponse(request.url_for('thread', id=json_['thread']['id']), status_code=status.HTTP_302_FOUND)



