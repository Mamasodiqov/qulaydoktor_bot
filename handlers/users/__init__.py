from . import start
from . import help
from . import echo

from aiogram import Router
from aiogram.filters import CommandStart, StateFilter, Command

import states
from . import start
def prepare_router() -> Router:
    user_router = Router()

    user_router.message.register(start.id, StateFilter(states.id.UserMainMenu.id))


    return user_router
