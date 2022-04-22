import asyncio
from datetime import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

import states.states
from loader import dp
from utils.mailing import mailing


@dp.callback_query_handler(text="set_mailing")
async def set_mailing(call: CallbackQuery):
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton("Назад", callback_data="main_admin_menu")]
    ])

    await call.message.edit_text("Введите дату в формате 'гггг-мм-дд'", reply_markup=markup)

    await states.states.Mailing.date.set()


@dp.message_handler(state=states.states.Mailing.date)
async def set_date(message: types.Message, state: FSMContext):
    try:
        datetime.strptime(message.text, '%Y-%m-%d')
    except:
        await message.answer("Не правильный формат даты! Формат: гггг-мм-дд")
        return

    async with state.proxy() as data:
        data["date"] = message.text

    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton("Назад", callback_data="main_admin_menu")]
    ])

    await message.answer("Введите время в формате 'ЧЧ:ММ'", reply_markup=markup)

    await states.states.Mailing.time.set()


@dp.message_handler(state=states.states.Mailing.time)
async def set_time(message: types.Message, state: FSMContext):
    try:
        datetime.strptime(message.text, '%H:%M')
    except:
        await message.answer("Не правильный формат времени! Формат: ЧЧ:ММ")
        return

    async with state.proxy() as data:
        data["time"] = message.text

    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton("Назад", callback_data="main_admin_menu")]
    ])

    await message.answer("Введите текст для рассылки", reply_markup=markup)

    await states.states.Mailing.text.set()


@dp.message_handler(state=states.states.Mailing.text)
async def set_time(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        date = data["date"]
        time = data["time"]

    await state.finish()

    await message.answer("Рассылка добавлена")

    asyncio.create_task(mailing(date=date, time=time, text=message.text))


