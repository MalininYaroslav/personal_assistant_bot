import asyncio
from datetime import datetime

from aiogram.types import BotCommand
from config import config
from handlers import register_handlers
from send_plan import send_plan


async def main():
    bot_commands = (
        ("start", "Начало работы с ботом"),
        ("add", "Добавить напоминание"),
        ("delete", "Удалить напоминание"),
    )

    commands_for_bot = []
    for cmd in bot_commands:
        commands_for_bot.append(BotCommand(command=cmd[0], description=cmd[1]))
    await config.bot.set_my_commands(commands=commands_for_bot)

    register_handlers(config.dp)

    await config.bot.delete_webhook(drop_pending_updates=True)
    await config.dp.start_polling(config.bot)


async def scheduler():
    while True:
        await asyncio.sleep(1)
        current_time = datetime.now(tz=config.tz).strftime("%H:%M:%S")
        if current_time == '16:49:01':
            await send_plan()


if __name__ == "__main__":
    try:
        loop = asyncio.get_event_loop()
        tasks = [loop.create_task(main()), loop.create_task(scheduler())]
        loop.run_until_complete(asyncio.wait(tasks))
    except (KeyboardInterrupt, SystemExit):
        print("Bot stopped")
