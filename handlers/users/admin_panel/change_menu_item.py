from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

import states.states
from keyboards.inline.callback_data import edit_menu_item_cd
from loader import dp, db


@dp.callback_query_handler(text="change_menu_item")
async def change_menu_item(call: CallbackQuery):
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton("Добавить", callback_data="add_menu_item")],
        [InlineKeyboardButton("Удалить", callback_data="del_menu_item")],
        [InlineKeyboardButton("Назад", callback_data="main_admin_menu")]
    ])

    await call.message.edit_text("Выберите",
                                 reply_markup=markup)


@dp.callback_query_handler(text="add_menu_item")
async def add_new_menu_item(call: CallbackQuery):
    await call.message.edit_text("Введите название вкладки")

    await states.states.MenuItem.title.set()


@dp.message_handler(state=states.states.MenuItem.title)
async def set_title(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["title"] = message.text

    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton("Назад", callback_data="main_admin_menu")]
    ])

    await message.answer("Введите текст для вкладки", reply_markup=markup)

    await states.states.MenuItem.description.set()


@dp.message_handler(state=states.states.MenuItem.description)
async def set_title(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["text"] = message.text

    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton("Назад", callback_data="main_admin_menu")]
    ])

    await message.answer("Введите короткое имя для вкладки на английском (пример для вкладки 'Поддержка': support)",
                         reply_markup=markup)

    await states.states.MenuItem.callback_data.set()


@dp.message_handler(state=states.states.MenuItem.callback_data)
async def set_title(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        title = data["title"]
        text = data["text"]

    await message.answer("Вкладка добавлена")

    await db.add_new_item(title, text, message.text)

    await state.finish()


@dp.callback_query_handler(text="del_menu_item")
async def del_menu_item(call: CallbackQuery):
    markup = InlineKeyboardMarkup()

    menu_items = await db.get_menu_items()

    for item in menu_items:
        button = InlineKeyboardButton(
            text=item[1],
            callback_data=edit_menu_item_cd.new(name=item[0])
        )

        markup.row(button)
    markup.row(InlineKeyboardButton("Назад", callback_data="main_admin_menu"))

    await call.message.edit_text("Выберите вкладку", reply_markup=markup)


@dp.callback_query_handler(edit_menu_item_cd.filter())
async def del_menu_item(call: CallbackQuery, callback_data: dict):
    await db.delete_menu_item(callback_data["name"])

    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton("Назад", callback_data="main_admin_menu")]
    ])

    await call.message.edit_text("Вкладка удалена", reply_markup=markup)
