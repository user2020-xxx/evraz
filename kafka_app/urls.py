from django.urls import path
from kafka_app import views

app_name = 'kafka'

urlpatterns = [
    path('data/', views.get_data),
    path('get_exhauster/<int:pk>', views.get_exhauster),
    path('get_graphics_data/', views.get_graphic),
    ]