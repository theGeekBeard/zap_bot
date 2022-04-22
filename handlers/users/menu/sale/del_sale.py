from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from handlers.users.menu.sale.show_sales import show_sale
from keyboards.inline.callback_data import numbers_cd
from loader import dp, db


@dp.callback_query_handler(numbers_cd.filter(), state="*")
async def del_sale(call: CallbackQuery, callback_data: dict):
    sales = await db.get_sales(call.message.chat.id)

    if len(sales[0]) == 1:
        await db.delete_sale(call.message.chat.id)
    else:
        sales[0].remove(callback_data["number"])

        await db.update_sales(call.message.chat.id, number=sales[0])

    await call.answer("Каталожный номер удален")

    await show_sale(call)
