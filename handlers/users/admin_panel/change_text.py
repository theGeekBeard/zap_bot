from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

import states.states
from keyboards.inline.callback_data import edit_text_cd
from loader import dp, db


@dp.callback_query_handler(text="change_text")
async def change_text(call: CallbackQuery):
    markup = InlineKeyboardMarkup()

    menu_items = await db.get_menu_items()

    for item in menu_items:
        button = InlineKeyboardButton(
            text=item[1],
            callback_data=edit_text_cd.new(id=item[0])
        )

        markup.row(button)
    markup.row(InlineKeyboardButton("Назад", callback_data="main_admin_menu"))

    await call.message.edit_text("Выберите вкладку, где хотите заменить текст или добавить", reply_markup=markup)


@dp.callback_query_handler(edit_text_cd.filter())
async def edit_text(call: CallbackQuery, state: FSMContext, callback_data: dict):
    async with state.proxy() as data:
        data["id"] = callback_data["id"]

    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton("Назад", callback_data="main_admin_menu")]
    ])

    await call.message.edit_text("Введите новый текст", reply_markup=markup)

    await states.states.Text.text.set()


@dp.message_handler(state=states.states.Text.text)
async def add_new_text(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        item_id = data["id"]

    text = message.text

    await db.add_new_text(item_id, text)

    await message.answer("Новый текст добавлен")

    await state.finish()



