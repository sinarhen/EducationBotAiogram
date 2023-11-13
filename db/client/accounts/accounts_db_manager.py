from db.general_db_manager import Database
from datetime import datetime


class AccountDB(Database):

    def __init__(self):
        super().__init__()
        self.create_table()

    def all_users(self):
        return self.get_data(select=('*',), _from='user')

    def create_table(self):
        sql_create_table_query = f"""
                    CREATE TABLE IF NOT EXISTS user(
                        id PRIMARY KEY NOT NULL,
                        datetime_joined TEXT,
                        superuser INTEGER DEFAULT 0
                        )
                """
        self.cur.execute(sql_create_table_query)
        self.commit()

    def check_if_user_in_db(self, user_id):
        res = self.get_data(select=('*',), _from='user', id=user_id)
        if res:
            return res
        return False

    def add_user_to_db(self, user_id, superuser=0):
        dt = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.add_data(table_name='user', id=user_id, datetime_joined=dt, superuser=superuser)

    def is_superuser(self, user_id):
        res = self.get_data(select=('superuser',), _from='user', id=user_id)
        if res[0][0] == 1 or res[0][0] == 'True':
            return True
        return False

    def is_creator(self, user_id):
        return str(user_id) == '679161628'
