from typing import Union

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

from loader import dp, bot


async def show_admin_menu(call: Union[CallbackQuery, types.Message]):

    markup = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton("Админ. панель"), KeyboardButton("Пользовательское меню")]
        ],
        resize_keyboard=True
    )

    if isinstance(call, CallbackQuery):
        await call.message.delete()
        chat_id = call.message.chat.id
    else:
        message = call
        chat_id = message.chat.id
    await bot.send_message(chat_id, "Ваше меню:", reply_markup=markup)


@dp.callback_query_handler(text="main_admin_menu", state="*")
@dp.message_handler(text="Админ. панель")
async def show_admin_panel(message: Union[types.Message, CallbackQuery], state: FSMContext):
    await state.finish()

    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton("Добавить новый язык", callback_data="add_new_lang")],
        [InlineKeyboardButton("Добавить/Удалить блок меню", callback_data="change_menu_item")],
        [InlineKeyboardButton("Добавить/Заменить текст", callback_data="change_text")],
        [InlineKeyboardButton("Добавить/Заменить контент", callback_data="change_file")],
        [InlineKeyboardButton("Установить рассылку", callback_data="set_mailing")],
        [InlineKeyboardButton("Статистика по боту", callback_data="statistic")],
    ])

    if isinstance(message, types.Message):
        await message.answer("Выберите действие:", reply_markup=markup)
    else:
        call = message
        await call.message.edit_text("Выберите действие:", reply_markup=markup)


