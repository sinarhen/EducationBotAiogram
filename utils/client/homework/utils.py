import datetime
from dateutil.parser import parse
import emoji

INVALID_DATE_MESSAGE = 'Дата є невалідною. Переконайтесь що:\n1) Вжито наступний формат: <рік>/<місяць>/<рік>\n2) Дата може існувати'


def is_correct_date(message):
    try:
        parse(message.text)
    except Exception as ex:
        return False

    return True


def is_uncorrect_date(message):
    return False if is_correct_date(message) else True


def get_datetime_object_from_string(string):
    return parse(string)


def get_compatible_with_sql_string_from_datetime_object(dt_obj):
    return datetime.datetime.strftime(dt_obj, '%Y-%m-%d')
