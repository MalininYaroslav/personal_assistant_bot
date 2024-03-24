__all__ = ['register_handlers']

from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from states import AddStates, DeleteStates

from handlers.start import start
from handlers.add import add_1, add_2, add_3
from handlers.delete import delete_1, delete_2


def register_handlers(dp: Router):
    dp.message.register(start, CommandStart())
    dp.message.register(delete_1, Command("delete"))
    dp.message.register(add_1, Command("add"))

    dp.message.register(add_2, F.text, AddStates.add_2)
    dp.message.register(add_3, F.text, AddStates.add_3)
    dp.message.register(delete_2, F.text, DeleteStates.delete_2)
