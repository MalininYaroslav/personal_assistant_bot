from datetime import datetime

from aiogram.enums import ParseMode

from db import database
from config import config


async def send_plan():
    users = await database.get_user_ids()
    date = datetime.now(tz=config.tz).strftime("%d.%m.%Y")

    for user in users:
        plans = await database.get_plans_on_day(user, date)
        print(plans)
        if len(plans) > 0:
            template = f"<b>{plans[0][0]}</b>, у вас на <b>{date}</b> такие планы:\n\n"
            for plan in plans:
                template += f"в <b>{plan[1]}</b> <b>{plan[2]}</b>\n\n"
            template += "Хорошего дня 😊"
            await config.bot.send_message(chat_id=user, text=template, parse_mode=ParseMode.HTML)
        else:
            await config.bot.send_message(chat_id=user, text="У вас ничего не запланировано на сегодня\n\n"
                                                             "Не забудьте записать свои планы на завтра\n"
                                                             "/add - добавить напоминание")
    return
