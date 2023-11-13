import os
from db.general_db_manager import Database
from utils.client.schedule.utils import schedule_json_to_list


class ScheduleDB(Database):

    def __init__(self):
        super().__init__()
        self.create_table()
        if self.is_empty('schedule'):
            self._insert_initial_data_to_schedule()

    def drop_database(self, db_root):
        os.remove(db_root)

    def get_day_of_week_data(self, weekday):
        self.cur.execute(f"""
            SELECT lesson.name, time, teacher from schedule JOIN lesson on schedule.lesson_id=lesson.id WHERE day={weekday};
        """)
        fetch = self.cur.fetchall()
        return fetch

    def create_table(self) -> None:
        cursor = self.cur
        cursor.execute("""CREATE TABLE IF NOT EXISTS schedule (
                            id        INTEGER PRIMARY KEY AUTOINCREMENT,
                            lesson_id INTEGER REFERENCES lesson (id),
                            time      TEXT,
                            teacher   TEXT,
                            day       INTEGER
                        );
                    """)

    def _insert_initial_data_to_schedule(self) -> None:
        insert_query = f"""
            INSERT INTO schedule (lesson_id, time, teacher, day) VALUES (?, ?, ?, ?)
        """
        _data = schedule_json_to_list()
        self.cur.executemany(insert_query, _data)
        self.commit()

    def get_schedule_by_day(self, weekday):
        print(weekday)
        sql_query = f"""
            SELECT name, time, teacher FROM schedule LEFT JOIN lesson ON schedule.lesson_id=lesson.id WHERE schedule.day={weekday}
        """
        self.cur.execute(sql_query)
        fetch = self.cur.fetchall()
        return fetch
