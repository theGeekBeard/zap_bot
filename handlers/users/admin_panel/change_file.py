from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

import states.states
from keyboards.inline.callback_data import edit_content_cd
from loader import dp, db


@dp.callback_query_handler(text="change_file")
async def change_text(call: CallbackQuery):
    markup = InlineKeyboardMarkup()

    menu_items = await db.get_menu_items()

    for item in menu_items:
        if ":" in item[-3]:
            continue
        button = InlineKeyboardButton(
            text=item[1],
            callback_data=edit_content_cd.new(callback_data=item[-3])
        )

        markup.row(button)
    markup.row(InlineKeyboardButton("Назад", callback_data="main_admin_menu"))

    await call.message.edit_text("Выберите вкладку, где хотите заменить контент или добавить", reply_markup=markup)


@dp.callback_query_handler(edit_content_cd.filter())
async def edit_text(call: CallbackQuery, state: FSMContext, callback_data: dict):
    async with state.proxy() as data:
        data["callback_data"] = callback_data["callback_data"]

    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton("Удалить контент", callback_data="del_content")],
        [InlineKeyboardButton("Назад", callback_data="main_admin_menu")]
    ])

    await call.message.edit_text("Отправьте новый контент или нажмите 'Удалить контент'", reply_markup=markup)

    await states.states.File.file.set()


@dp.callback_query_handler(text="del_content", state="*")
async def del_content(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        call_data = data["callback_data"]

    await db.del_content(call_data)

    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton("Назад", callback_data="main_admin_menu")]
    ])

    await call.message.edit_text("Контент удален", reply_markup=markup)


@dp.message_handler(content_types=types.ContentType.PHOTO)
async def add_new_text(message: types.Message, state: FSMContext):
    file = message.photo[-1].file_id
    print(file)

    # await add_new_content(message, file, state)

    await state.reset_state(with_data=False)


@dp.message_handler(content_types=types.ContentType.VIDEO, state=states.states.File.file)
async def add_new_text(message: types.Message, state: FSMContext):
    file = message.video.file_id

    await add_new_content(message, file, state)

    await state.reset_state(with_data=False)


@dp.message_handler(content_types=types.ContentType.DOCUMENT, state=states.states.File.file)
async def add_new_text(message: types.Message, state: FSMContext):
    file = message.document.file_id

    await add_new_content(message, file, state)

    await state.reset_state(with_data=False)


async def add_new_content(message: types.Message, file_id, state: FSMContext):
    async with state.proxy() as data:
        data["file"] = file_id

    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton("Добавить", callback_data="add")],
        [InlineKeyboardButton("Заменить", callback_data="replace")],
        [InlineKeyboardButton("Назад", callback_data="main_admin_menu")]
    ])

    await message.answer("Выберите",
                         reply_markup=markup)


@dp.callback_query_handler(text="add")
async def set_new_content(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        call_data = data["callback_data"]
        file_id = data["file"]

    await db.add_new_content(call_data, file_id)

    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton("Назад", callback_data="main_admin_menu")]
    ])

    await call.message.edit_text("Контент добавлен", reply_markup=markup)


@dp.callback_query_handler(text="replace")
async def set_new_content(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        call_data = data["callback_data"]
        file_id = data["file"]

    await db.update_content(call_data, file_id)

    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton("Назад", callback_data="main_admin_menu")]
    ])

    await call.message.edit_text("Контент заменен", reply_markup=markup)
