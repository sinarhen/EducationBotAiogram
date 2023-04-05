from aiogram import types, Dispatcher
from create_bot import bot
from keyboards.keyboards import get_menu_keyboard
from handlers.client.accounts.models import User
from emoji import emojize


async def start_command_handler(message: types.Message):
    user = User(message.from_user.id, superuser=True)
    user.save_user()
    await bot.send_message(message.from_user.id, '👋')
    await bot.send_message(message.from_user.id,
                           f'Привіт {message.from_user.first_name}! Скористайся меню та обери функцію',
                           reply_markup=get_menu_keyboard(user_id=message.from_user.id))


async def process_return_to_main_menu(message: types.Message, state=None):
    if state:
        await state.finish()
    await bot.send_message(message.from_user.id, emojize('Дякую що зкористались ботом :red_heart:'),
                           reply_markup=get_menu_keyboard(message.from_user.id))


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(start_command_handler, commands=['start'])
    dp.register_message_handler(process_return_to_main_menu, lambda x: x.text.casefold() == "до головного меню",
                                state='*')
