from datetime import datetime

from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from db import database
from lexicon import lexicon
from states import DeleteStates


async def delete_1(message: Message, state: FSMContext):
    await state.set_state(DeleteStates.delete_2)
    await message.answer(text=lexicon['delete_1'], parse_mode=ParseMode.HTML)


async def delete_2(message: Message, state: FSMContext):
    try:
        assert datetime.strptime(message.text, "%d.%m.%Y %H:%M")

        plan = await database.get_plan(message.chat.id, message.text.rsplit(" ")[0], message.text.rsplit(" ")[1])
        if not plan:
            await message.answer(text=lexicon['not_exist'], parse_mode=ParseMode.HTML)
            return

        await state.clear()
        await database.delete_plan(message.chat.id, message.text.rsplit(" ")[0], message.text.rsplit(" ")[1])
        await message.answer(text=lexicon['delete_2'].format(plan[3], plan[4]), parse_mode=ParseMode.HTML)

    except ValueError:
        await message.answer(text=lexicon['not_time'], parse_mode=ParseMode.HTML)
