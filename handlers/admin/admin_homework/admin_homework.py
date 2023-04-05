from aiogram import types
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from keyboards.keyboards import get_custom_keyboard, get_yes_no_keyboard, get_menu_keyboard
from db.client.books.books_db_manager import BooksDB
from create_bot import bot
from utils.client.homework.utils import is_correct_date, is_uncorrect_date
from db.client.homework.homework_db_manager import HomeworkDB
from utils.client.homework.utils import get_compatible_with_sql_string_from_datetime_object, \
    get_datetime_object_from_string, INVALID_DATE_MESSAGE
from handlers.admin.admin import FSMAdminFunctions


class FSMAddHomework(StatesGroup):
    lesson = State()
    date_from = State()
    date_to = State()
    task = State()
    return_to_main_menu = State()


books_db = BooksDB()
lessons = books_db.get_all_lessons()

hw_db = HomeworkDB()


async def process_homework_start(message: types.Message, state: FSMAdminFunctions._function):
    await state.finish()
    await FSMAddHomework.lesson.set()
    await bot.send_message(message.from_user.id, 'Оберіть предмет', reply_markup=get_custom_keyboard(lessons))


async def process_homework_pick_lesson(message: types.Message, state: FSMAddHomework.lesson):
    async with state.proxy() as data:
        data['lesson'] = message.text
    await FSMAddHomework.date_from.set()
    await bot.send_message(message.from_user.id,
                           "Коли задано?\nВведіть дату у такому форматі: <день>/<місяць>/<рік>\nПриклад: 12/03/2023",
                           reply_markup=get_custom_keyboard())


async def process_homework_pick_date_from_valid(message: types.Message, state: FSMAddHomework.date_from):
    msg = message.text
    dt_msg = get_datetime_object_from_string(msg)
    sql_format = get_compatible_with_sql_string_from_datetime_object(dt_msg)
    async with state.proxy() as data:
        data['date_from'] = sql_format
    await FSMAddHomework.date_to.set()
    await bot.send_message(message.from_user.id,
                           "Виконати до\nВведіть дату у такому форматі: <день>/<місяць>/<рік>\nПриклад: 12/03/2023",
                           reply_markup=get_custom_keyboard())


async def process_homework_pick_date_to_valid(message: types.Message, state: FSMAddHomework.date_to):
    msg = message.text
    dt_msg = get_datetime_object_from_string(msg)
    sql_format = get_compatible_with_sql_string_from_datetime_object(dt_msg)
    async with state.proxy() as data:
        condition = hw_db.check_if_task_already_exists(date_to=sql_format,
                                                       lesson_id=books_db.get_lesson_id_by_lesson_name(data['lesson'])[
                                                           0])
        if not condition:
            data['date_to'] = sql_format
            await FSMAddHomework.task.set()
            await bot.send_message(message.from_user.id,
                                   "Що задали?",
                                   reply_markup=get_custom_keyboard())
            return
        else:
            await bot.send_message(message.from_user.id, '❌')
            await bot.send_message(message.from_user.id, 'Завдання на цей день для цього предмету вже є!')


async def process_homework_enter_task(message: types.Message, state: FSMAddHomework.task):
    async with state.proxy() as data:
        data['task'] = message.text
    await FSMAddHomework.return_to_main_menu.set()
    data = await state.get_data()
    _id = hw_db.get_data(select=('id',), _from='lesson', name=data['lesson'])[0][0]
    hw_db.add_data(table_name='homework', date_from=data['date_from'], date_to=data['date_to'], task=data['task'],
                   lesson_id=_id)
    await bot.send_message(message.from_user.id, '✅')
    await bot.send_message(message.from_user.id, 'Дз додано')
    await bot.send_message(message.from_user.id, 'Повернутись до головного меню ', reply_markup=get_yes_no_keyboard())


async def process_homework_return_to_main_menu(message: types.Message, state: FSMAddHomework.return_to_main_menu):
    await state.finish()
    await bot.send_message(message.from_user.id, "Дякую що зкористались ботом❤️",
                           reply_markup=get_menu_keyboard(message.from_user.id))


async def process_homework_pick_date_invalid(message: types.Message, state: FSMAddHomework.date_from):
    await bot.send_message(message.from_user.id, '❌')
    await bot.send_message(message.from_user.id,
                           INVALID_DATE_MESSAGE,
                           reply_markup=get_custom_keyboard(None))


async def process_homework_retry_process(message: types.Message, state: FSMAddHomework.return_to_main_menu):
    await FSMAddHomework.lesson.set()
    await bot.send_message(message.from_user.id, "Оберіть предмет", reply_markup=get_custom_keyboard(lessons))


async def process_homework_enter_task_is_empty(message: types.Message, state: FSMAddHomework.task):
    await bot.send_message(message.from_user.id, "Завдання не може бути пустим", reply_markup=get_custom_keyboard())


def register_message_handlers(dp: Dispatcher):
    dp.register_message_handler(process_homework_start, lambda x: x.text.casefold() == "домашнє завдання",
                                state=FSMAdminFunctions._function)

    # LESSON
    dp.register_message_handler(process_homework_pick_lesson, lambda x: x.text in lessons, state=FSMAddHomework.lesson)
    dp.register_message_handler(process_homework_pick_date_from_valid, lambda x: is_correct_date(x),
                                state=FSMAddHomework.date_from)

    # DATE_FROM
    for func, _filter in {process_homework_pick_date_from_valid: is_correct_date,
                          process_homework_pick_date_invalid: is_uncorrect_date}.items():
        dp.register_message_handler(func, _filter,
                                    state=FSMAddHomework.date_from)

    dp.register_message_handler(process_homework_pick_date_invalid, is_uncorrect_date,
                                state=FSMAddHomework.date_from)

    # DATE TO
    for func, _filter in {process_homework_pick_date_to_valid: is_correct_date,
                          process_homework_pick_date_invalid: is_uncorrect_date}.items():
        dp.register_message_handler(func, _filter,
                                    state=FSMAddHomework.date_to)

    # TASK
    dp.register_message_handler(process_homework_enter_task, lambda x: x.text, state=FSMAddHomework.task)
    dp.register_message_handler(process_homework_enter_task_is_empty, lambda x: not x.text, state=FSMAddHomework.task)

    # RETURN TO MAIN MENU
    dp.register_message_handler(process_homework_return_to_main_menu, lambda x: 'так' in x.text.casefold(),
                                state=FSMAddHomework.return_to_main_menu)
    dp.register_message_handler(process_homework_retry_process, lambda x: 'ні' in x.text.casefold(),
                                state=FSMAddHomework.return_to_main_menu)
