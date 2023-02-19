from django.urls import path, include, re_path
from kafka_app.consumers import KafkaConsumer

# Here, "" is routing to the URL ChatConsumer which
# will handle the chat functionality.
websocket_urlpatterns = [re_path(r'^ws/kafka/$', KafkaConsumer.as_asgi()),]