import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).parent.resolve()


class Database:
    """CONNECTING"""

    def __init__(self) -> None:
        self.db_root = BASE_DIR / 'education.sqlite3'
        self.conn, self.cur = self.setUp()
        self.row_factory_default = None

    def __str__(self) -> str:
        return f'connected to db {self.db_root}'

    def __call__(self, *args, **kwargs):
        self.conn.row_factory = self.row_factory_default
        self.cursor = self.conn.cursor()

    def _row_factory_for_singe_values_in_fetchall(self):
        self.conn.row_factory = lambda cursor, row: row[0]
        new_cursor = self.conn.cursor()
        self.cur = new_cursor

    def setUp(self) -> (sqlite3.Connection, sqlite3.Cursor):
        con = sqlite3.connect(self.db_root)  # Connection
        cursor = con.cursor()
        return con, cursor

    def commit(self):
        return self.conn.commit()

    def get_data(self, select: tuple | list, _from, distinct: bool = None, **filters) -> list:
        select_keywords = ', '.join(select)
        custom_filters = []
        if filters:
            for key, value in filters.items():
                custom_filters.append(f'{key}="{value}"')

            custom_filters = ' AND '.join(custom_filters)
        select_options = f"{'DISTINCT' if distinct else ''}"
        sql_query = f"""
                SELECT {select_options} {select_keywords} FROM {_from} {f'WHERE {custom_filters}' if custom_filters else ''}
            """
        try:
            self.cur.execute(sql_query)
        except sqlite3.OperationalError as ex:
            print(f'Your query: {sql_query}')
            print(f'Avalaible columns are: {self.get_table_columns(_from)}')
            raise ex
        res = self.cur.fetchall()
        return res

    def add_data(self, table_name: str, commit=True, **values) -> str:
        columns_str = ""
        values_str = ""
        for key, value in values.items():
            columns_str += f"{key},"
            values_str += f"'{value}',"
        columns_str = columns_str[:-1]
        values_str = values_str[:-1]
        sql_query = f"""
            INSERT INTO {table_name}({columns_str}) VALUES ({values_str})
        """
        print(sql_query[:200])
        self.cur.execute(sql_query)
        self.commit()

        return sql_query

    def update_data(self, table_name: str, commit=True, **values) -> str:
        set_values = ''
        for key, value in values.items():
            set_values += f"{key}='{value}',"
        set_values = set_values[:-1]
        sql_query = f"""
            UPDATE {table_name} SET {set_values}
            """
        self.cur.execute(sql_query)
        if commit:
            self.commit()
        return sql_query

    def get_table_columns(self, table_name) -> set:
        self.cur.execute(f'SELECT * FROM {table_name}')
        names = set(map(lambda x: x[0], self.cur.description))
        return names

    def is_empty(self, table_name):
        fetch = self.get_data(select=('*',), _from=table_name)
        if fetch:
            return False
        return True
