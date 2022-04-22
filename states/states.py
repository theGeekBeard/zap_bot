from aiogram.dispatcher.filters.state import StatesGroup, State


class Sale(StatesGroup):
    number = State()


class SearchSale(StatesGroup):
    number = State()
