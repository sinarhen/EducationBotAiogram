from db.general_db_manager import Database


class HomeworkDB(Database):

    def __init__(self):
        super().__init__()
        self.create_table()

    def create_table(self):
        sql_query_create_table = """
            CREATE TABLE IF NOT EXISTS homework (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date_from TEXT (20),
                date_to TEXT (20),
                task TEXT (500),
                lesson_id REFERENCES lesson (id) ON DELETE CASCADE
            )
            """
        self.cur.execute(sql_query_create_table)

    def get_lesson_name(self, lesson_id: int | str):
        data = self.get_data(select=('name',), _from='lesson', id=lesson_id, distinct=True)
        return data

    def get_homework_data(self, date_to):
        sql_query = f"""
        SELECT 
            lesson.name,
            task,
            date_from,
            date_to
        FROM 
            homework
            LEFT JOIN
            lesson ON homework.lesson_id = lesson.id
        WHERE date_to = '{date_to}'

 """
        self.cur.execute(sql_query)
        return self.cur.fetchall()

    def check_if_task_already_exists(self, date_to, lesson_id):
        res = self.get_data(select=('id', ), _from='homework', date_to=date_to, lesson_id=lesson_id)
        return len(res) > 0


