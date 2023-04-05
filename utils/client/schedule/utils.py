import json
from handlers.client.schedule.settings import JSON_ROOT_DIRECTORY


def schedule_json_to_list(file_dest=JSON_ROOT_DIRECTORY, with_autoincrement_id: bool=None, lesson_ids=None) -> list:
    data = []
    with open(f'{file_dest}', 'r', encoding='UTF-8') as js:
        js = js.read()
        dict_from_json = json.loads(js)
        for i in range(1, len(dict_from_json)+1):
            day = dict_from_json[str(i)]

            day_of_week = i
            for id in range(1, len(day)+1):
                num_of_lessons = len(day.keys())
                day[str(id)]['day'] = day_of_week
                
                if with_autoincrement_id:
                    day[str(id)]['id'] = id + num_of_lessons * (day_of_week - 1)

                values = day[str(id)].values()
                data.append(tuple(values))

    return data


