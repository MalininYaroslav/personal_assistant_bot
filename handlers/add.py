from datetime import datetime

from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from db import database
from lexicon import lexicon
from states import AddStates
from config import config


async def add_1(message: Message, state: FSMContext):
    await state.update_data(user_id=message.chat.id, username=message.from_user.first_name)
    await state.set_state(AddStates.add_2)
    await message.answer(text=lexicon['add_1'], parse_mode=ParseMode.HTML)


async def add_2(message: Message, state: FSMContext):
    try:
        assert datetime.strptime(message.text, "%d.%m.%Y %H:%M")

        plan = await database.get_plan(message.chat.id, message.text.rsplit(" ")[0], message.text.rsplit(" ")[1])
        if plan:
            await message.answer(text=lexicon['exist'].format(plan[5]), parse_mode=ParseMode.HTML)
            return

        if datetime.strptime(message.text, "%d.%m.%Y %H:%M").timestamp() > datetime.now(tz=config.tz).timestamp():
            await state.update_data(date=message.text.rsplit(" ")[0], time=message.text.rsplit(" ")[1])
            await state.set_state(AddStates.add_3)
            await message.answer(text=lexicon['add_2'], parse_mode=ParseMode.HTML)
        else:
            await message.answer(text=lexicon['not_date'], parse_mode=ParseMode.HTML)
            return
    except ValueError:
        await message.answer(text=lexicon['not_time'], parse_mode=ParseMode.HTML)


async def add_3(message: Message, state: FSMContext):
    await state.update_data(event=message.text)

    data = await state.get_data()
    await database.add_plan(**data)
    await message.answer(text=lexicon['add_3'].format(data['date'], data['time'], data['event']),
                         parse_mode=ParseMode.HTML)
    await state.clear()
