from rest_framework import serializers
from .models import *


class SignalModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = SignalModel
        fields = '__all__'


class MachineModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = MachineModel
        fields = '__all__'


class SensorModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensorModel
        fields = '__all__'


class KafkaDataModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = KafkaDataModel
        fields = '__all__'

