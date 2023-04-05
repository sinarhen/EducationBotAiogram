from aiogram.dispatcher import FSMContext, Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types
from create_bot import bot
from aiogram.utils.exceptions import NetworkError
from keyboards.keyboards import get_yes_no_keyboard, get_menu_keyboard, \
    get_custom_keyboard
from db.client.books.books_db_manager import BooksDB

initializer = BooksDB()
lessons = initializer.get_all_lessons()
authors = initializer.get_all_authors()


class FSMBook(StatesGroup):
    choosing_lesson = State()
    choosing_author = State()
    return_to_main_menu = State()


async def process_start(message: types.Message):
    await message.reply('Оберіть предмет', reply_markup=get_custom_keyboard(lessons))
    await FSMBook.choosing_lesson.set()


async def process_pick_lesson(message: types.Message, state: FSMContext):
    ids = initializer.get_lesson_authors(message.text)
    if ids:
        await FSMBook.choosing_author.set()
        async with state.proxy() as data:
            data['lesson'] = message.text
            data['book_id_list'] = ids
        await message.reply('Оберіть автора',
                            reply_markup=get_custom_keyboard(initializer.get_authors_list_by_ids(ids)))
        return
    await bot.send_message(message.from_user.id, 'Для цього предмету немає книг')


async def process_get_book(message: types.Message, state: FSMContext):
    await FSMBook.return_to_main_menu.set()
    async with state.proxy() as data:
        lst = data['book_id_list']
        book_id_by_author = map(str, initializer.get_book_id_by_author(message.text))
        intersect_id = list(set(lst) & set(book_id_by_author))[0]
        print(intersect_id)
        book_cover = initializer.get_data(select=('cover',), _from='book', id=intersect_id)[0]
        book_pdf = initializer.get_data(select=('pdf_file',), _from='book', id=intersect_id)[0]

        try:
            await bot.send_photo(message.from_user.id, photo=book_cover, caption=f'АВТОР - {message.text}', )
            await bot.send_message(message.from_user.id, 'Зачекайте будь ласка...', reply_markup=None)
            await bot.send_document(message.from_user.id, (f'{data["lesson"]} {message.text}.pdf', book_pdf))
        except NetworkError as ex:
            await bot.send_message(message.from_user.id, 'Книга наразі не доступна. Вибачте за незручності')
        finally:
            await message.reply('Повернутись до головного меню?', reply_markup=get_yes_no_keyboard())


async def process_get_book_unknown_book(message: types.Message, state: FSMBook.choosing_author):
    await bot.send_message(message.from_user.id, '❌')
    await bot.send_message(message.from_user.id, 'Невідомий автор, спробуйте ще раз або зверніться до адміна')


async def process_return_to_main_menu(message: types.Message, state: FSMContext):
    await message.reply('Дякую, що зкористались ботом',
                        reply_markup=get_menu_keyboard(user_id=message.from_user.id))
    await state.finish()


async def process_retry(message: types.Message, state: FSMContext):
    await FSMBook.choosing_lesson.set()
    await message.reply("Оберіть предмет", reply_markup=get_custom_keyboard(lessons))


async def process_pick_lesson_unknown_lesson(mesage: types.Message, state: FSMBook.choosing_lesson):
    await bot.send_message(mesage.from_user.id,
                           '❌')
    await bot.send_message(mesage.from_user.id,
                           'Предмет не знайдено у базі даних, спробуйте обрати інший, або зверніться до адміна',
                           reply_markup=get_custom_keyboard(lessons))


def register_handlers_books(dp: Dispatcher):
    # START FSM
    dp.register_message_handler(
        process_start,
        lambda x: 'книги' in x.text.casefold()
    )

    # LESSON
    dp.register_message_handler(
        process_pick_lesson,
        lambda x: x.text in lessons,
        state=FSMBook.choosing_lesson
    )
    dp.register_message_handler(
        process_pick_lesson_unknown_lesson,
        lambda x: x.text not in lessons,
        state=FSMBook.choosing_lesson
    )

    # AUTHOR
    dp.register_message_handler(
        process_get_book,
        lambda x: x.text in authors,
        state=FSMBook.choosing_author
    )
    dp.register_message_handler(
        process_get_book_unknown_book,
        lambda x: x.text not in authors,
        state=FSMBook.choosing_author
    )

    # RETURN TO MAIN MENU
    dp.register_message_handler(
        process_return_to_main_menu,
        lambda x: 'так' in x.text.casefold(),
        state=FSMBook.return_to_main_menu
    )
    dp.register_message_handler(
        process_retry,
        lambda x: 'ні' in x.text.casefold(),
        state=FSMBook.return_to_main_menu
    )
