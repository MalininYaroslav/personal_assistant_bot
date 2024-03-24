from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from lexicon import lexicon


async def start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(text=lexicon['start'].format(message.from_user.first_name), parse_mode=ParseMode.HTML)
