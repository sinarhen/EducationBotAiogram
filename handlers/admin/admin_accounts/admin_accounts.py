from aiogram import types
from aiogram.dispatcher import Dispatcher
from keyboards.keyboards import get_custom_keyboard, get_yes_no_keyboard, get_menu_keyboard
from create_bot import bot
from handlers.admin.admin import FSMAdminFunctions
from handlers.client.accounts.models import User
from utils.client.utils import get_pd_dataframe, get_image_bytecode, export_image


async def process_accounts_check(message: types.Message, state: FSMAdminFunctions):
    user = User(message.from_user.id)
    if user.is_creator():
        users = user.objects.all()
        file_name = 'all_users.png'
        df = get_pd_dataframe(users, columns=['ID', 'DATE_JOINED', 'SUPERUSER'])
        export_image(df=df, filename=file_name)
        img = get_image_bytecode(filename=file_name)
        await bot.send_photo(message.from_user.id, img)
        return
    await bot.send_message(message.from_user.id, 'Access Restricted')


def register_message_handlers(dp: Dispatcher):
    dp.register_message_handler(process_accounts_check, commands=['superadmin_users'],
                                state=FSMAdminFunctions._function)
