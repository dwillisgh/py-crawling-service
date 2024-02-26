from fastapi import APIRouter

from app.api.routers import v1_crawljob

router = APIRouter()
router.include_router(
    v1_crawljob.router, tags=["jobs python crawling service"], prefix="/v1"
)