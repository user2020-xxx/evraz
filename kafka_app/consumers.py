from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json


class KafkaConsumer(WebsocketConsumer):
    def connect(self):
        self.calc_name = "kafka"
        self.calc_group_name = 'group_%s' % self.calc_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.calc_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.calc_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        print(text_data)
        message = text_data_json['expression']

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.calc_group_name,
            {
                'type': 'kafka_message',
                'message': message
            }
        )

    # Receive message from room group
    def kafka_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))