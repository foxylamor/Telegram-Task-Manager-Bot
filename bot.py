import os
import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import BotCommand
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.exceptions import TelegramAPIError
from dotenv import load_dotenv

from handlers.routes import router, reminder_worker
from db import init_db
from middleware.rate_limit import RateLimitMiddleware


# Load environment variables
load_dotenv()
TOKEN = os.getenv("TOKEN")


# Configure logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)


async def main() -> None:
    await init_db() # Initialize the database

    # Initialize bot and dispatcher
    bot = Bot(
        token=TOKEN,
        properties=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

    dp = Dispatcher(storage=MemoryStorage())

    dp.message.middleware(RateLimitMiddleware(2)) # Add rate limiting middleware to the dispatcher

    dp.include_router(router) # Register handlers

    reminder_task = asyncio.create_task(reminder_worker(bot))

    await bot.set_my_commands([
        BotCommand(command="start", description="Start the bot"),
        BotCommand(command="add", description="Add a new task"),
        BotCommand(command="tasks", description="List all tasks"),
        BotCommand(command="done", description="Mark a task as done"),
        BotCommand(command="delete", description="Delete a task")
    ])

    try:
        await dp.start_polling(bot) # Start polling
    except TelegramAPIError as e:
        logger.error(f"Error occurred while starting polling: {e}") # Log the error if polling fails
    finally:
        reminder_task.cancel()
        try:
            await reminder_task
        except asyncio.CancelledError:
            pass
        await bot.session.close() # Close the bot session on shutdown

if __name__ == "__main__":
    asyncio.run(main())
