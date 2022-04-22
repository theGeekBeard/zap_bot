from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from keyboards.inline.callback_data import pass_cd
from loader import dp, bot, db


@dp.callback_query_handler(text="privacy_policy")
async def get_privacy_policy(call: CallbackQuery):

    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton("🔙Назад в главное меню", callback_data="main_menu")]
        ]
    )
    text = """Политика конфиденциальности и условия Пользовательского соглашения.

1. Телеграм бот: @p_zap_bot (ПродамЗапчасти.РФ) представляет собой автоматизированный сервис по поиску потенциальных покупателей запчастей для спецтехники, грузовиков и различных спецмашин.
Целью бота является помочь его участникам выйти на более близкое общение с клиентами, для совершения сделки купли-продажи пользователей бота и участников группы в телеграм: @k_zap (КуплюЗапчасти.РФ)

2. Сам бот (ПродамЗапчасти.РФ) не является участником, организатором сделки, покупателем, продавцом, работодателем, посредником, агентом, представителем какого-либо пользователя, выгодоприобретателем или иным заинтересованным лицом в отношении сделок между пользователями. 
Пользователи используют полученную информацию от бота, чтобы заключать сделки на свой страх и риск, без прямого или косвенного участия или контроля со стороны бота.

3. Ни сам бот, ни его создатели не могут гарантировать, что вся информация, которую пользователи получают, указывают и используют соответствует действительности и что каждый пользователь действительно является тем, кем представляется. 
Будьте осмотрительны при совершении сделок! Используйте видео звонки, знакомьтесь ближе, просите показать все в прямом эфире, непосредственно в моменте общения.  

4. Ни сам бот, ни его создатели не несут ответственности за ущерб, убытки или расходы, возникшие в связи с использованием бота или невозможностью его использования!

5. Используя бот (ПродамЗапчасти.РФ) нажимая кнопку СТАРТ пользователь дает свое согласие на получение информационных рассылок от бота с любой периодичностью.

6. У данного бота (ПродамЗапчасти.РФ) есть бесплатный тест-период!
По окончании тест-периода бот для пользователя становится платным, за символическую оплату: 100 руб. - 1 месяц. 

7. Все предложения, замечания или вопросы по поводу работы данного бота пользователь может направить админу бота: @p_zap_admin"""

    await call.message.edit_text(text, reply_markup=markup)


@dp.callback_query_handler(pass_cd.filter())
async def pass_press(call: CallbackQuery):
    await call.answer(cache_time=1)


@dp.message_handler()
async def handle_other_message(message: types.Message):
    await bot.delete_message(message.chat.id, message.message_id)


@dp.message_handler(content_types=types.ContentType.DOCUMENT, state="*")
async def handle_other_message(message: types.Message):
    await bot.delete_message(message.chat.id, message.message_id)


@dp.message_handler(content_types=types.ContentType.STICKER, state="*")
async def handle_other_message(message: types.Message):
    await bot.delete_message(message.chat.id, message.message_id)


@dp.message_handler(content_types=types.ContentType.ANIMATION, state="*")
async def handle_other_message(message: types.Message):
    await bot.delete_message(message.chat.id, message.message_id)


@dp.message_handler(content_types=types.ContentType.VIDEO, state="*")
async def handle_other_message(message: types.Message):
    await bot.delete_message(message.chat.id, message.message_id)


@dp.message_handler(content_types=types.ContentType.PHOTO, state="*")
async def handle_other_message(message: types.Message):
    await bot.delete_message(message.chat.id, message.message_id)


@dp.message_handler(content_types=types.ContentType.VOICE, state="*")
async def handle_other_message(message: types.Message):
    await bot.delete_message(message.chat.id, message.message_id)


@dp.message_handler(content_types=types.ContentType.VIDEO_NOTE, state="*")
async def handle_other_message(message: types.Message):
    await bot.delete_message(message.chat.id, message.message_id)
