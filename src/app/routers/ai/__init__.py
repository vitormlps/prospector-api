from fastapi import APIRouter

from . import (
    analyses,
    annotations,
)


router = APIRouter(prefix="/ai")

router.include_router(analyses.router)
router.include_router(annotations.router)
