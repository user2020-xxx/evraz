import json
import timeit

from kafka import KafkaConsumer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from kafka_app import models
from kafka_app.parser import parsing_data_from_kafka

def kafka_get_data():
    try:
        host = 'rc1a-b5e65f36lm3an1d5.mdb.yandexcloud.net:9091'
        topic = 'zsmk-9433-dev-01'
        username = '9433_reader'
        password = 'eUIpgWu0PWTJaTrjhjQD3.hoyhntiK'
        group_name = 'intruder'

        SASL_MECHANISM = 'SCRAM-SHA-512'
        SASL_SSL = 'SASL_SSL'

        consumer = KafkaConsumer(topic,
                                 bootstrap_servers=host,
                                 api_version=(0, 10),
                                 security_protocol=SASL_SSL,
                                 ssl_check_hostname=True,
                                 ssl_cafile='cert.pem',
                                 sasl_mechanism=SASL_MECHANISM,
                                 sasl_plain_username=username,
                                 sasl_plain_password=password,
                                 value_deserializer=lambda m: json.loads(m.decode('utf-8')),
                                 group_id=group_name,)

        for msg in consumer:
            result = json.dumps(msg.value)
            layer = get_channel_layer()
            async_to_sync(layer.group_send)('group_kafka', {
                'type': 'kafka_message',
                'message': result,
            })
            parsing_data_from_kafka(msg.value)

    except Exception as e:
        print(e)