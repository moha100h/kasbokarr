from aiogram import Bot, types
from app.utils.logger import logger
from app.services.n8n_service import N8nService
from app.services.export_service import ExportService

WELCOME = (
    "<b>Kasbokar Bot</b>\n\n"
    "Extract public business info from legal sources.\n\n"
    "<b>Usage:</b> send city + category\n"
    "<b>Examples:</b>\n"
    "  Restaurants in Tehran\n"
    "  Dentists in Tabriz\n"
    "  Car repair shops in Mashhad\n\n"
    "<b>Commands:</b>\n"
    "/start  - Welcome\n"
    "/help   - Help\n"
    "/status - System status"
)

HELP = (
    "<b>How to use Kasbokar Bot:</b>\n\n"
    "1. Type: <i>category</i> in <i>city</i>\n"
    "2. Bot searches legal public directories\n"
    "3. You receive XLSX + CSV files\n\n"
    "<b>Data collected:</b>\n"
    "- Business name, category, address\n"
    "- City, province, website\n"
    "- Phone (normalized +98), rating\n"
    "- Latitude, longitude, source\n\n"
    "<b>Limits:</b> max 100 results, admin-only"
)


class BotService:
    def __init__(self, bot: Bot, admin_id: int):
        self.bot = bot
        self.admin_id = admin_id
        self.n8n = N8nService()
        self.export = ExportService()

    async def send_welcome(self, message: types.Message):
        await message.answer(WELCOME)

    async def send_help(self, message: types.Message):
        await message.answer(HELP)

    async def send_status(self, message: types.Message):
        n8n_ok = bool(self.n8n.webhook_url)
        status = (
            "<b>System Status</b>\n"
            f"Bot: OK\n"
            f"n8n: {'Connected' if n8n_ok else 'NOT configured'}\n"
            f"Export: XLSX + CSV"
        )
        await message.answer(status)

    async def handle_user_request(self, message: types.Message):
        query = (message.text or "").strip()
        if not query or query.startswith("/"):
            return
        await message.answer(f"Searching: <b>{query}</b> ...")
        result = await self.n8n.search_businesses(query)
        if result["success"]:
            data = result["data"]
            await message.answer(f"Found <b>{len(data)}</b> results. Generating files...")
            await self.export.send_to_admin(self.bot, self.admin_id, data, query)
        else:
            await message.answer(f"Error: {result['error']}")
