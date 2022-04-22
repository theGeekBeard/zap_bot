from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from funcy import chunks

import states.states
from keyboards.inline.callback_data import numbers_cd, pass_cd
from loader import dp, db, bot


@dp.callback_query_handler(text=["show_parts", "BACK", "PREV"], state="*")
async def show_sale(call: CallbackQuery):
    print(call.data)
    await states.states.SearchSale.number.set()

    message_id = await db.get_message_id(call.message.chat.id)

    if message_id:
        try:
            if call.data == "show_parts":
                print(34324)
                await bot.delete_message(call.message.chat.id, message_id)
                await bot.delete_message(call.message.chat.id, message_id + 1)
                await db.del_message_id(call.message.chat.id)
        except:
            if call.data == "show_parts":
                print(232243)
                await bot.delete_message(call.message.chat.id, message_id - 1)
                await db.del_message_id(call.message.chat.id)
    else:
        pass

    if call.data == "show_parts":
        await db.add_index(call.message.chat.id, 0)

    salesKeyboards = []

    sales = await db.get_sales(call.message.chat.id)

    if sales:
        sales[0].sort()
        for i in chunks(10, sales[0]):
            markup = InlineKeyboardMarkup()
            for j in i:
                try:
                    markup.add(InlineKeyboardButton(j.replace(" ", ""), callback_data=pass_cd.new(number=j)),
                               InlineKeyboardButton("👈Удалить 🚮", callback_data=numbers_cd.new(number=j)))
                except AttributeError:
                    continue
            else:
                if len(sales[0]) > 10:
                    markup.add(InlineKeyboardButton("<<<", callback_data="BACK"),
                               InlineKeyboardButton(">>>", callback_data="PREV"))
                markup.row(InlineKeyboardButton("🔙Назад в главное меню", callback_data="main_menu"))
                salesKeyboards.append(markup)
    else:

        markup = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton("🔙Назад в главное меню", callback_data="main_menu")]
            ]
        )

        return await call.message.edit_text("<b>Найдено номеров</b>: 0", reply_markup=markup,
                                            parse_mode="HTML")

    index = await db.get_index(types.User.get_current().id)

    if call.data == "PREV":
        index += 1
    elif call.data == "BACK":
        index -= 1

    try:
        markup = salesKeyboards[index]
    except IndexError:
        index = 0
        markup = salesKeyboards[index]

    await call.message.edit_text(f"<b>Найдено номеров</b>: {len(sales[0])}\n"
                                 f"<b>Страница:</b> {index + 1 if index >= 0 else len(list(chunks(10, sales[0]))) + index + 1}",
                                 reply_markup=markup, parse_mode="HTML")
    await db.add_index(call.message.chat.id, index)


@dp.message_handler(state=states.states.SearchSale.number)
async def search_sale(message: types.Message, state: FSMContext):
    await db.add_message_id(message.chat.id, message.message_id)

    sale = await db.get_sale(message.chat.id, message.text)

    if sale:
        markup = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(sale, callback_data=pass_cd.new(number=sale)),
                 InlineKeyboardButton("👈Удалить 🚮", callback_data=numbers_cd.new(number=sale))],
                [InlineKeyboardButton("🔙Назад", callback_data="show_parts")]
            ]
        )

        await message.answer(text=f"Найдено: 1\n\n" + "\n", reply_markup=markup)

        await state.finish()
    else:

        markup = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton("🔙Назад", callback_data="show_parts")]
            ]
        )

        await message.answer("В базе данных нет такого номера", reply_markup=markup)

        await state.finish()
