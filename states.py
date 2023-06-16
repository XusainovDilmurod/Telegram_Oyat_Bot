from aiogram.dispatcher.filters.state import StatesGroup, State

class SuralarInfo(StatesGroup):
    sura = State()
    oyat = State()

class SearchSura(StatesGroup):
    sura_name = State()
    oyat = State()

class Botqw(StatesGroup):
    fikir = State()