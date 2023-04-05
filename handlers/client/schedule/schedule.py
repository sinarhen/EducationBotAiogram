import datetime
from aiogram import types
from aiogram.dispatcher import FSMContext, Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from keyboards.keyboards import get_schedule_options_keyboard, get_yes_no_keyboard, get_menu_keyboard, date_names
from db.client.schedule.schedule_db_manager import ScheduleDB
from utils.client.utils import get_pd_dataframe, export_image, get_image_bytecode
from create_bot import bot

DB = ScheduleDB()
TODAY = datetime.datetime.now().weekday()

date_convertor = dict(zip(date_names, range(1, 6)))


class FSMSchedule(StatesGroup):
    choosing_date_of_schedule = State()
    return_to_main_menu = State()


async def process_start(message: types.Message):
    await message.reply('Розклад на коли?', reply_markup=get_schedule_options_keyboard())
    await FSMSchedule.choosing_date_of_schedule.set()


async def process_choosing_date_of_schedule(message: types.Message, state: FSMContext):
    await FSMSchedule.return_to_main_menu.set()
    data = DB.get_schedule_by_day(weekday=date_convertor[message.text])
    df = get_pd_dataframe(data, columns=['Предмет', 'Час', 'Вчитель'])
    export_image(df, filename='schedule.png')
    photo = get_image_bytecode(filename="schedule.png")

    await bot.send_photo(message.from_user.id, photo=photo)
    await bot.send_message(message.from_user.id, "Повернутись до головного меню?", reply_markup=get_yes_no_keyboard())


async def process_choosing_date_of_schedule_unknown_weekday(message: types.Message, state: FSMContext):
    await bot.send_message(message.from_user.id, "❌")
    await bot.send_message(message.from_user.id, "Невідомий день тижня")


async def process_finish(message: types.Message, state: FSMContext):
    await bot.send_message(message.from_user.id, 'Дякую, що зкористались ботом', reply_markup=get_menu_keyboard(message.from_user.id))
    await state.finish()


async def process_retry(message: types.Message, state: FSMContext):
    await FSMSchedule.choosing_date_of_schedule.set()
    await message.reply("Розклад на коли", reply_markup=get_schedule_options_keyboard())


def register_handlers_schedule(dp: Dispatcher):
    # START FSM
    dp.register_message_handler(
        process_start,
        lambda x: 'розклад' in x.text.casefold(),
        state=None
    )

    # CHOOSING DATE OF SCHEDULE
    dp.register_message_handler(
        process_choosing_date_of_schedule,
        lambda x: x.text in date_names,
        state=FSMSchedule.choosing_date_of_schedule
    )
    dp.register_message_handler(
        process_choosing_date_of_schedule_unknown_weekday,
        lambda x: x.text not in date_names,
        state=FSMSchedule.choosing_date_of_schedule
    )

    # RETURN TO MAIN MENU
    dp.register_message_handler(
        process_finish,
        lambda x: 'так' in x.text.casefold(),
        state=FSMSchedule.return_to_main_menu,
    )
    dp.register_message_handler(
        process_retry,
        lambda x: 'ні' in x.text.casefold(),
        state=FSMSchedule.return_to_main_menu,
    )
