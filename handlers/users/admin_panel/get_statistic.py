from typing import Union

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

from loader import dp, bot, db


@dp.callback_query_handler(text="statistic")
async def get_statistic(call: CallbackQuery):
    users = await db.get_users()

    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton("Назад", callback_data="main_admin_menu")]
    ])

    await call.message.edit_text(f"Кол-во пользователей: {len(users)}", reply_markup=markup)