import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, BotCommand
from dotenv import load_dotenv

from utils import extract_earnings_info

load_dotenv('.env')
TOKEN = getenv("BOT_TOKEN")
dp = Dispatcher()


# Statement
class StockState(StatesGroup):
    stocks = State()


@dp.message(CommandStart())
async def command_start_handler(msg: Message) -> None:
    bot_start = BotCommand(command='start', description='Start the bot')
    stock_info = BotCommand(command='info', description='Stocks information')
    await msg.bot.set_my_commands([bot_start, stock_info])
    await msg.answer(f"Hello, {html.bold(msg.from_user.full_name)}!")


@dp.message(Command('info'))
async def example_handler(msg: Message, state: FSMContext):
    data = extract_earnings_info()[0]
    main_text = f"""
📅Date: {data['date']}
🧮Quantity: {data['quantity']}
"""
    await state.set_data(data)
    await state.set_state(StockState.stocks)
    await msg.answer(main_text)

    # second part
    for stock in data['stocks'][:10]:
        stock_text = f"""
🌐Country:   {stock['country']}
🟢Title:     {stock['title']}
🔗Link:      {stock['stockLink']}
📈EPS:       {stock['stockEPS']}
📉REV:       {stock['stockREV']}
📊MarketCap: {stock['stockMarketCap']}
"""
        await msg.answer(stock_text)


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())

# <a href="{stock['stockLink']}">{stock['title']}</a>
