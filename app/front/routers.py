from typing import Annotated

from fastapi import APIRouter, Path, Request, HTTPException, Form, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates



from app.front.filters import iso_str_date_to_format
from app.threads.routers import get_threads, get_thread, add_thread
from app.comments.routers import get_thread_comments
from app.schemas.base import SPaginator
from app.threads.schemas import SThreadAdd

router = APIRouter(prefix="/forum", tags=["Комментарии"])
templates = Jinja2Templates(directory='app/front/templates')
templates.env.filters['iso_str_date_to_format'] = iso_str_date_to_format



@router.get('/', name='index')
async def index(request: Request):
    response = await get_threads(SPaginator(limit=20, offset=0))
    if response.status_code == status.HTTP_200_OK:
        threads = response.threads
    else:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                            detail="Что-то с серваком! Уже чиню!")
    return templates.TemplateResponse("index.html", {
        "request": request, 'threads': threads,
    })



@router.get('/{thread_id:int}', name='thread')
async def thread(request: Request, thread_id: Annotated[int, Path(ge=1)]):

    response = await get_thread(thread_id)
    if response.status_code == status.HTTP_200_OK:
        thread = response.thread
    else:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                            detail="Что-то с серваком! Уже чиню!")

    response = await get_thread_comments(thread_id=thread_id, paginator=SPaginator(limit=0, offset=0))
    if response.status_code == status.HTTP_200_OK:
        comments = response.comments
    else:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                            detail="Что-то с серваком! Уже чиню!")

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
    response = await add_thread(thread_add)
    if response.status_code == status.HTTP_201_CREATED:
        thread = response.thread
    else:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                            detail="Что-то с серваком! Уже чиню!")
    return RedirectResponse(f"/forum/{thread.id}", status_code=status.HTTP_302_FOUND)