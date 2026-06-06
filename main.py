import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.client.default import DefaultBotProperties
from app.services.bot_service import BotService
from app.utils.logger import setup_logger
from config import config

logger = setup_logger(__name__)

bot = Bot(token=config.BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher()
bot_service = BotService(bot, config.ADMIN_ID)

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await bot_service.send_welcome(message)

@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    await bot_service.send_help(message)

@dp.message(Command("status"))
async def cmd_status(message: types.Message):
    await bot_service.send_status(message)

@dp.message()
async def handle_message(message: types.Message):
    if message.from_user and message.from_user.id == config.ADMIN_ID:
        await bot_service.handle_user_request(message)
    else:
        await message.answer("Access denied.")

async def main():
    logger.info("Kasbokar Bot starting...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped")
