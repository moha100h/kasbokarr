from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from config import config

router = Router()

WELCOME = (
    "<b>Kasbokarr Bot</b>\n\n"
    "Search public business info from OpenStreetMap.\n\n"
    "<b>Usage:</b> send city + category\n"
    "<b>Examples:</b>\n"
    "  Restaurants in Tehran\n"
    "  Dentists in Tabriz\n"
    "  Car repair in Mashhad\n\n"
    "<b>Commands:</b>\n"
    "/start - Welcome\n"
    "/help  - Help\n"
    "/status - System status"
)

@router.message(Command("start"))
async def cmd_start(message: Message):
    if message.from_user.id != config.ADMIN_ID:
        await message.answer("Access denied.")
        return
    await message.answer(WELCOME)

@router.message(Command("help"))
async def cmd_help(message: Message):
    if message.from_user.id != config.ADMIN_ID:
        return
    await message.answer(WELCOME)

@router.message(Command("status"))
async def cmd_status(message: Message):
    if message.from_user.id != config.ADMIN_ID:
        return
    await message.answer("<b>Status:</b> Bot is running OK")
