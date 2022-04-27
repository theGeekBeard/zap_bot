import json
from collections import Counter

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

import states.states
from loader import dp, db, bot
from utils.convert_to_json import convert_to_json


@dp.callback_query_handler(text="add_part")
async def add_sale(call: CallbackQuery):
    message_id = await db.get_message_id(call.message.chat.id)

    if message_id:
        try:
            await bot.delete_message(call.message.chat.id, message_id)
            await bot.delete_message(call.message.chat.id, message_id + 1)
        except:
            await bot.delete_message(call.message.chat.id, message_id - 1)

        await db.del_message_id(call.message.chat.id)
    else:
        pass

    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton("🔙Назад в главное меню", callback_data="main_menu")]
        ]
    )

    text = """Внесите ниже в строке для сообщений👇
<b>КАТАЛОЖНЫЙ НОМЕР</b> запчасти 
и нажмите кнопку отправить▶️

❗️ Не пишите марку техники, ни какую-либо другую информацию! 
Пишите только <b>КАТАЛОЖНЫЙ НОМЕР</b> запчасти!
<i>❗️ Если номеров несколько, то внесите их списком, разделяя Запятой!
❗️ Строго в одну строчку весь список!
❗️ В конце не нужно ставить запятую!</i>"""

    try:
        await call.message.edit_text(text, reply_markup=markup, parse_mode="HTML")
    except:
        pass

    await states.states.Sale.number.set()


@dp.message_handler(state=states.states.Sale.number)
async def set_number(message: types.Message, state: FSMContext):
    await db.add_message_id(message.chat.id, message.message_id)

    new_numbers = message.text.replace(" ", "").split(",")
    for i in new_numbers:
        if len(i) > 15:
            new_numbers.remove(i)
        elif "/n" in i:
            new_numbers.remove(i)

    old_numbers = await db.get_sales(message.chat.id)

    counter = 0

    count_new_numbers = 0

    if old_numbers:
        res = new_numbers + old_numbers

        for key, value in Counter(res).items():
            if value > 1:
                counter += value
            else:
                if key in new_numbers:
                    count_new_numbers += 1

        res_json = await convert_to_json(list(set(res)))

        await db.update_sales(message.chat.id, res_json)
    else:
        res = new_numbers

        for key, value in Counter(res).items():
            if value > 1:
                counter += value
            else:
                if key in new_numbers:
                    count_new_numbers += 1

        res_json = await convert_to_json(list(set(res)))

        await db.add_new_sale(message.chat.id, res_json)

    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton("🔙Назад", callback_data="add_part")]
        ]
    )

    text = f"👉Добавлено в продажу: <b>{count_new_numbers}</b>\n"

    if counter > 0:
        if counter % 2 == 0 and counter != 2:
            counter /= 2
        else:
            counter -= 1

    await message.answer(
        text=text + f"""👉Повторений: <b>{int(counter)}</b>\n
✅Вы всё сделали правильно! 
Теперь ожидайте когда <b>бот</b> найдет потенциального покупатея для ваших запчастей!
Согласно тех каталожных номеров которые Вы указали при добавлении в продажу!

<i>Если необходимо добавить еще запчасти в продажу, то вернитесь на 1 шаг назад, и добавьте еще каталожные номера тех запчастей которые Вы хотите продать!</i>""",
        reply_markup=markup, parse_mode="HTML")

    await state.finish()
