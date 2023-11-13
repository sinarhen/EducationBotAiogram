from aiogram import types
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from keyboards.keyboards import get_admin_functions_keyboard
from db.client.books.books_db_manager import BooksDB
from create_bot import bot
from utils.client.homework.utils import is_correct_date, is_uncorrect_date
from db.client.homework.homework_db_manager import HomeworkDB
from utils.client.homework.utils import get_compatible_with_sql_string_from_datetime_object, \
    get_datetime_object_from_string
from handlers.client.accounts.models import User


class FSMAdminFunctions(StatesGroup):
    _function = State()


async def process_admin_start(message: types.Message):
    user = User(message.from_user.id)

    if user.is_superuser():
        await FSMAdminFunctions._function.set()
        await bot.send_message(message.from_user.id, 'Адмін панель', reply_markup=get_admin_functions_keyboard())
        return
    await bot.send_message(message.from_user.id, 'У вас нема доступу до цієї функції')



async def process_admin_invalid_command(message: types.Message, state: FSMAdminFunctions._function):
    await bot.send_message(message.from_user.id, '❌')
    await bot.send_message(message.from_user.id, 'Такої функції не існує')

def register_message_handlers(dp: Dispatcher):
    dp.register_message_handler(process_admin_start, lambda x: "адмін панель" in x.text.casefold())
