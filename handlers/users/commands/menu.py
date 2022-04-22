from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from loader import dp, db, bot


@dp.callback_query_handler(text="main_menu", state="*")
async def get_main_menu(call: CallbackQuery, state: FSMContext):
    await state.finish()

    message_id = await db.get_message_id(call.message.chat.id)

    if message_id:
        try:
            await bot.delete_message(call.message.chat.id, message_id)
            await bot.delete_message(call.message.chat.id, message_id + 1)
        except:
            pass

        await db.del_message_id(call.message.chat.id)
    else:
        pass

    menuMarkup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton("✍️Добавить запчасти в продажу", callback_data="add_part")],
            [InlineKeyboardButton("🔍Посмотреть добавленные запчасти", callback_data="show_parts")],
            [InlineKeyboardButton("🗒Политика конфиденциальности", callback_data="privacy_policy")]
        ]
    )

    await call.message.edit_text("<b>Главное меню:</b>👇", reply_markup=menuMarkup, parse_mode="HTML")


