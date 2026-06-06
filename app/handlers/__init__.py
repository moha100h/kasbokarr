from aiogram import Router
from .commands import router as cmd_router
from .search import router as search_router

router = Router()
router.include_router(cmd_router)
router.include_router(search_router)
