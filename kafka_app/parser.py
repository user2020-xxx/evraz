from django.db import connection
from kafka_app.dict_relashion import KEYS_OF_FIELD


def parsing_data_from_kafka(value_dict):
    key_list = []
    value_list = []
    for key, value in value_dict.items():
        if value is None:
            value = 0
        if key == 'moment':
            key_list.append(key)
            value_list.append(f'\'{value}\'')
        else:
            key_list.append(KEYS_OF_FIELD[key])
            value_list.append(str(value))
    key_string = ', '.join(key_list)
    value_string = ', '.join(value_list)

    template_sql_raw = f'''INSERT INTO kafka_app_kafkadatamodel ({key_string})\
                VALUES ({value_string})'''

    with connection.cursor() as cursor:
        cursor.execute(template_sql_raw)
