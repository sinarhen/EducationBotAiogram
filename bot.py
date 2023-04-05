from aiogram.utils import executor
from create_bot import dp, bot


async def on_startup(_):
    print('POLLING STARTED')


from handlers.client.schedule import schedule
from handlers.client.books import books
from handlers.client import client
from handlers.client.homework import homework
from handlers.admin.admin_homework import admin_homework
from handlers.admin import admin
from handlers.admin.admin_accounts import admin_accounts

client.register_handlers_client(dp)
schedule.register_handlers_schedule(dp)
books.register_handlers_books(dp)
homework.register_handlers_homework(dp)
admin_homework.register_message_handlers(dp)
admin.register_message_handlers(dp)
admin_accounts.register_message_handlers(dp)


executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
