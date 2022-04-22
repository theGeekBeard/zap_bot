from typing import Union

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from loader import dp


@dp.message_handler(text="Хочу продать запчасти")
@dp.callback_query_handler(text="back_to_sale_menu", state="*")
@dp.message_handler(commands=["sale"])
async def get_sale_menu(message: Union[types.Message, CallbackQuery], state: FSMContext):
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton("Добавить в продажу", callback_data="add_sale")],
            [InlineKeyboardButton("Удалить из продажи", callback_data="del_sale")],
            [InlineKeyboardButton("Посмотреть добавленные", callback_data="show_sale")],
            [InlineKeyboardButton("Назад", callback_data="back_to_main")],
        ]
    )

    if isinstance(message, types.Message):
        await message.answer("Выберите:", reply_markup=markup)
    else:
        call = message

        await call.message.edit_text("Выберите:", reply_markup=markup)

    await state.finish()
