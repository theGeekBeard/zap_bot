from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from loader import dp, db


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    menuMarkup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton("✍️Добавить запчасти в продажу", callback_data="add_part")],
            [InlineKeyboardButton("🔍Посмотреть добавленные запчасти", callback_data="show_parts")],
            [InlineKeyboardButton("🗒Политика конфиденциальности", callback_data="privacy_policy")]
        ]
    )

    text = """✔️ Приветствуем Вас в первом автоматизированном сервисе по продажам запчастей для спецтехники, грузовиков и различных спецмашин: <b>ПродамЗапчасти.РФ</b>

✔️ Структура бота выполнена на простом интуитивном уровне,
и Вам не потребуется каких-либо особенных знаний что бы его использовать!

✔️ Так же просим отнестись с пониманием, так-как сейчас бот запущен в тестовом режиме. 
А его алгоритмы будут постоянно усовершенствоваться!

✔️ Более подробную информацию о данном сервисе и условия сотрудничества Вы можете узнать нажав кнопку в главном МЕНЮ: <b>Политика конфиденциальности</b>

<i>Продолжая работу с данным ботом это означает, что Вы принимаете все эти условия!</i>

✔️ Желаем успешных сделок! И как говорил Ю.А.Гагарин "поехали" 🙂

✔️ Ниже в главном МЕНЮ выберите интересующий Вас раздел"""

    await db.add_new_user(message.chat.id, message.chat.username)

    await message.answer(text, parse_mode="HTML")

    await message.answer("<b>Главное меню:</b>👇", reply_markup=menuMarkup, parse_mode="HTML")
