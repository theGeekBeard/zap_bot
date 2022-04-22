from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

import states.states
from loader import dp, db


@dp.callback_query_handler(text="add_new_lang")
async def ask_language_full_name(call: CallbackQuery):
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton("Назад", callback_data="main_admin_menu")]
    ])

    await call.message.edit_text("Введите название нового языка на этом же языке (пример: Русский, English, عرب)", reply_markup=markup)

    await states.states.Language.full_name.set()


@dp.message_handler(state=states.states.Language.full_name)
async def ask_language_short_name(message: types.Message, state: FSMContext):
    language_full_name = message.text

    async with state.proxy() as data:
        data["language_full_name"] = language_full_name

    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton("Назад", callback_data="main_admin_menu")]
    ])

    await message.answer("Введите аббревиатуру языка (пример: ru)", reply_markup=markup)

    await states.states.Language.short_name.set()


@dp.message_handler(state=states.states.Language.short_name)
async def set_language(message: types.Message, state: FSMContext):
    language_short_name = message.text

    async with state.proxy() as data:
        language_full_name = data["language_full_name"]

    await db.add_new_language(language_full_name, language_short_name)

    await message.answer(f"{language_full_name} язык добавлен!")

    await state.finish()
