import os
from datetime import datetime
from aiogram import Router, F
from aiogram.types import Message, BufferedInputFile
from aiogram.filters import CommandStart, Command
from config import ADMIN_ID, MAX_RESULTS, EXPORT_DIR
from services.search import search_businesses
from services.export import make_xlsx, make_csv

router = Router()

WELCOME = (
    "<b>Kasbokarr Bot</b>\n\n"
    "Send me a search query to find businesses.\n\n"
    "<b>Examples:</b>\n"
    "  Restaurants in Tehran\n"
    "  Dentists in Tabriz\n"
    "  Car repair in Mashhad\n\n"
    "<b>Commands:</b>\n"
    "/start - Welcome\n"
    "/help  - Help\n"
    "/status - Status"
)

@router.message(CommandStart())
async def cmd_start(msg: Message):
    await msg.answer(WELCOME)

@router.message(Command("help"))
async def cmd_help(msg: Message):
    await msg.answer(WELCOME)

@router.message(Command("status"))
async def cmd_status(msg: Message):
    await msg.answer("<b>Status:</b> Bot is running OK.")

@router.message(F.text & ~F.text.startswith("/"))
async def handle_query(msg: Message):
    if msg.from_user.id != ADMIN_ID:
        await msg.answer("Access denied.")
        return
    query = msg.text.strip()
    await msg.answer(f"Searching: <b>{query}</b> ...")
    results = await search_businesses(query, MAX_RESULTS)
    if not results:
        await msg.answer("No results found.")
        return
    await msg.answer(f"Found <b>{len(results)}</b> results. Generating files...")
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    os.makedirs(EXPORT_DIR, exist_ok=True)
    xlsx_data = make_xlsx(results)
    csv_data = make_csv(results)
    await msg.answer_document(
        BufferedInputFile(xlsx_data, filename=f"kasbokarr_{ts}.xlsx"),
        caption=f"Query: {query} | Records: {len(results)}"
    )
    await msg.answer_document(
        BufferedInputFile(csv_data, filename=f"kasbokarr_{ts}.csv")
    )
