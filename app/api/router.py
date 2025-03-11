from fastapi import APIRouter

from .threads.routers import router as threads_router
from .comments.routers import router as comments_router


router = APIRouter(prefix="/api/v1")
router.include_router(threads_router)
router.include_router(comments_router)

