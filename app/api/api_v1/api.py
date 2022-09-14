from fastapi import APIRouter

from app.api.api_v1.endpoints import demo

router = APIRouter()
router.include_router(
    demo.router, prefix="/demo", tags=["demo"], include_in_schema=False
)
