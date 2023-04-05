from utils.client.books.utils import *
from handlers.client.books.settings import BASE_DIR
from db.general_db_manager import Database


class BooksDB(Database):
    _data = {}

    def __init__(self) -> None:
        super().__init__()
        self.FILES_DIR = BASE_DIR / 'books_files'
        self.create_table()
        if self.is_empty('lesson') or self.is_empty('book'):
            self._get_initial_data()

        if self.is_empty(table_name='lesson'):
            self._insert_initial_data_to_table_lesson()
        if self.is_empty(table_name='book'):
            self._insert_initial_data_to_table_book()

    def create_table(self) -> None:
        sql_query1 = f"""CREATE TABLE IF NOT EXISTS book (
                id       INTEGER   PRIMARY KEY AUTOINCREMENT,
                author   TEXT (55),
                cover    BLOB,
                pdf_file BLOB
            );
        """
        self.cur.execute(sql_query1)
        sql_query2 = """CREATE TABLE IF NOT EXISTS lesson (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT (55),
                book_id REFERENCES book (id) 
            )"""
        self.cur.execute(sql_query2)
        self.commit()

    def _get_initial_data(self) -> None:
        get_data_dict(BASE_DIR / 'books_files', self._data, with_id=True)

    def _insert_initial_data_to_table_book(self) -> None:
        _data1 = get_data_in_tuples(self._data)
        for i in _data1:
            cover = i[1]
            pdf = i[2]
            self.insert_data_to_table_book_of_db(i[0], cover, pdf)
        self.commit()

    def _insert_initial_data_to_table_lesson(self) -> None:
        for i in self._data:
            for author in self._data[i]['authors']:
                lesson = i
                for author_info in author:
                    _id = author[author_info]['id']
                    self.add_data(table_name='lesson', name=lesson, book_id=_id)
        self.add_data(table_name='lesson', name='Фізична культура')
        self.commit()

    def insert_data_to_table_book_of_db(self, author: str, cover_path, pdf_file_path):
        cover = file_into_bytecode(cover_path)
        pdf_file = file_into_bytecode(pdf_file_path)
        sql_query = f"""
            INSERT INTO book(author, cover, pdf_file) VALUES (?, ?, ?)
            """
        data_tuple = (author, cover, pdf_file)
        self.cur.execute(sql_query, data_tuple)

    def get_lesson_authors(self, lesson):
        self._row_factory_for_singe_values_in_fetchall()
        sql_query = f"""
            SELECT book_id FROM lesson WHERE name="{lesson}"
        """
        self.cur.execute(sql_query)
        res = self.cur.fetchall()
        print(res)
        return res if res[0] else None

    def get_all_lessons(self):
        self._row_factory_for_singe_values_in_fetchall()
        sql_query = f"""
                SELECT DISTINCT name FROM lesson
            """
        self.cur.execute(sql_query)
        res = self.cur.fetchall()
        return res

    def get_all_authors(self):
        self._row_factory_for_singe_values_in_fetchall()
        sql_query = f"""
            SELECT DISTINCT author from book
        """
        self.cur.execute(sql_query)
        res = self.cur.fetchall()
        return res

    def get_authors_list_by_ids(self, data):
        s = set()
        if data[0]:
            for i in data:
                res = self.get_data(select=('author',), _from='book', id=i)
                s.add(res[0])
        return s if len(s) > 0 else None

    def get_lesson_id_by_lesson_name(self, lesson_name):
        res = self.get_data(select=('id',), _from='lesson', name=lesson_name)
        return res

    def get_book_id_by_author(self, author_name):
        self._row_factory_for_singe_values_in_fetchall()
        return self.get_data(select=('id', ), _from='book', author=author_name)