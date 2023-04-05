from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardButton
from handlers.client.accounts.models import User

from emoji import emojize


def emojize_list(iterable):
    return list(map(lambda x: emojize(x), iterable))


date_names = 'Понеділок', "Вівторок", "Середа", "Четверг", "П'ятниця"

user_menu = emojize_list(['Розклад :notebook:', "Книги :books:", "Домашнє завдання :house:"])

admin_menu = emojize_list(
    ['Розклад :notebook:', "Книги :books:", "Домашнє завдання :pencil:", "Адмін панель :briefcase:"])

yes_no = emojize_list(['Так :check_mark_button:', "Ні :cross_mark:"])

admin_functions = 'Домашнє завдання',
homework_search_by = {"За датою": 'date_to'}


def add_mainmenu_button(func):
    def wrapped(*args):
        kb = func(*args)
        kb.add(InlineKeyboardButton(text='До головного меню'))
        return kb

    return wrapped


@add_mainmenu_button
def get_homework_keyboard():
    btns = (InlineKeyboardButton(text=i) for i in homework_search_by.keys())

    kb = ReplyKeyboardMarkup(resize_keyboard=True, input_field_placeholder='Оберіть тип пошуку')
    for btn in btns:
        kb.add(btn)
    return kb


@add_mainmenu_button
def get_admin_functions_keyboard():
    btns = (InlineKeyboardButton(text=i) for i in admin_functions)

    kb = ReplyKeyboardMarkup(resize_keyboard=True, input_field_placeholder='Оберіть тип пошуку')
    for btn in btns:
        kb.add(btn)
    return kb


@add_mainmenu_button
def get_custom_keyboard(list_of_args=None):
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    if list_of_args:
        btns = (InlineKeyboardButton(text=i) for i in list_of_args)
        for btn in btns:
            kb.add(btn)
    return kb

@add_mainmenu_button
def get_schedule_options_keyboard():
    btns = (InlineKeyboardButton(text=i) for i in date_names)

    kb = ReplyKeyboardMarkup(resize_keyboard=True, input_field_placeholder="Оберіть день тижня")
    for i in btns:
        kb.add(i)
    return kb

@add_mainmenu_button
def get_authorized_keyboard():
    btns = [InlineKeyboardButton(text=i) for i in admin_menu]
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, input_field_placeholder='Що вас цікавить?')
    for i in btns:
        kb.add(i)
    return kb

@add_mainmenu_button
def get_unauthorized_keyboard():
    btns = [InlineKeyboardButton(text=i) for i in user_menu]
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, input_field_placeholder='Що вас цікавить?')
    for i in btns:
        kb.add(i)
    return kb


def get_menu_keyboard(user_id):
    if User(user_id).is_superuser():
        return get_authorized_keyboard()
    return get_unauthorized_keyboard()


def get_yes_no_keyboard():
    btns = [InlineKeyboardButton(text=i) for i in yes_no]

    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True,
                             input_field_placeholder='Напишіть "так" або "ні"')
    for i in btns:
        kb.add(i)
    return kb
