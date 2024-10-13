import asyncio
import logging
import sys
from os import getenv

from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, BotCommand

from utils import extract_earnings_info

load_dotenv('.env')
TOKEN = getenv("BOT_TOKEN")
dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(msg: Message) -> None:
    bot_start = BotCommand(command='start', description='Start the bot')
    await msg.bot.set_my_commands([bot_start])
    await msg.answer(f"Hello, {html.bold(msg.from_user.full_name)}!")


@dp.message()
async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())

# <a href="{stock['stockLink']}">{stock['title']}</a>
