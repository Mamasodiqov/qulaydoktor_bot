import aiohttp
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from loader import dp, db
from aiogram import types, F

from states.id import UserMainMenu


@dp.message(CommandStart())
async def start_bot(message: types.Message, state: FSMContext):
    await message.answer(f"Assalomu alaykum {message.from_user.full_name}!")
    await message.answer(f'Iltimos, ID kiriting:')
    await state.set_state(UserMainMenu.id)

@dp.message(F.text)
async def id(message: types.Message):
    telegram_id = message.from_user.id
    name = message.from_user.full_name
    request_id = int(message.text)
    if await db.select_user(telegram_id=telegram_id) is None:
        await db.add_user(telegram_id=telegram_id, name=name, request_id=request_id, file_path='')
    url = f'http://back.qulaydoktor.com/api/v1/appointment/analysis/{request_id}'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
            file_path = data['data']
            await db.update_request_id(telegram_id=telegram_id, request_id=request_id)
            await db.update_file_path(file_path=file_path, telegram_id=telegram_id)
            await message.answer(f'Quyidagi havola orqali faylni yuklab oling: {file_path}')
            # print(file_path)
