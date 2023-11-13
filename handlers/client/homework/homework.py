from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types
from create_bot import bot
from keyboards.keyboards import get_yes_no_keyboard, get_custom_keyboard, get_homework_keyboard, homework_search_by, \
    get_menu_keyboard
from db.client.homework.homework_db_manager import HomeworkDB
from utils.client.utils import get_pd_dataframe, get_image_bytecode, export_image
from utils.client.homework.utils import is_correct_date, is_uncorrect_date, normalize_datetime_to_sqlite, \
    INVALID_DATE_MESSAGE


class FSMHomework(StatesGroup):
    search_by = State()
    type_date = State()
    return_to_main_menu = State()


async def process_homework_start(message: types.Message):
    await FSMHomework.search_by.set()
    await bot.send_message(message.from_user.id, '📆')
    await bot.send_message(message.from_user.id, 'Оберіть тип пошуку Д/З', reply_markup=get_homework_keyboard())


async def process_input_date(message: types.Message, state: FSMHomework.search_by):
    await FSMHomework.type_date.set()
    await bot.send_message(message.from_user.id, 'Оберіть дату яка вас цікавить у форматі <день>/<місяць>/<рік>',
                           reply_markup=get_custom_keyboard())


async def process_type_date_is_valid(message: types.Message, state: FSMHomework.type_date):
    await FSMHomework.return_to_main_menu.set()

    initializer = HomeworkDB()
    dt = normalize_datetime_to_sqlite(message.text)

    inner = initializer.get_homework_data(date_to=dt)
    if not inner:
        await bot.send_message(message.from_user.id, "Не знайдено дз на цей день")
    else:
        df = get_pd_dataframe(data=inner, columns=['Предмет', "Завдання", "Задано", "Виконати до"])
        file_name = 'homework.png'
        export_image(df, file_name)
        image = get_image_bytecode(filename=file_name)
        await bot.send_photo(message.from_user.id, image)
    await bot.send_message(message.from_user.id, 'Повернутись до головного меню?', reply_markup=get_yes_no_keyboard())


async def process_type_date_is_invalid(message: types.Message, state: FSMHomework.type_date):
    await bot.send_message(message.from_user.id, "❌")
    await bot.send_message(message.from_user.id,
                           INVALID_DATE_MESSAGE,
                           reply_markup=get_custom_keyboard(None))


async def process_not_return_to_main_menu(message: types.Message, state: FSMHomework.return_to_main_menu):
    await FSMHomework.search_by.set()
    await bot.send_message(message.from_user.id, 'Оберіть тип пошуку Д/З', reply_markup=get_homework_keyboard())


async def process_return_to_main_menu(message: types.Message, state: FSMHomework.return_to_main_menu):
    await state.finish()
    await bot.send_message(message.from_user.id, 'Дякую що зкористались ботом ❤️',
                           reply_markup=get_menu_keyboard(message.from_user.id))


def register_handlers_homework(dp: Dispatcher):
    # START FSM
    dp.register_message_handler(
        process_homework_start,
        lambda x: 'домашнє завдання' in x.text.casefold()
    )

    # SEARCH BY
    dp.register_message_handler(
        process_input_date,
        lambda x: x.text in homework_search_by.keys(),
        state=FSMHomework.search_by
    )

    # TYPE_DATE
    dp.register_message_handler(
        process_type_date_is_valid,
        is_correct_date,
        state=FSMHomework.type_date
    )
    dp.register_message_handler(
        process_type_date_is_invalid,
        is_uncorrect_date,
        state=FSMHomework.type_date
    )

    # RETURN TO MAIN MENU
    dp.register_message_handler(
        process_not_return_to_main_menu,
        lambda x: 'ні' in x.text.casefold(),
        state=FSMHomework.return_to_main_menu
    )
    dp.register_message_handler(
        process_return_to_main_menu,
        lambda x: 'так' in x.text.casefold(),
        state=FSMHomework.return_to_main_menu
    )
