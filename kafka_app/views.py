import json
import threading

from django.shortcuts import render
from rest_framework.decorators import api_view
from kafka_app.kafka_cons import kafka_get_data
from django.http import HttpResponse, JsonResponse
from kafka_app.models import *
from kafka_app.dict_relashion import KEYS_OF_FIELD


def get_data(request):
    t = threading.Thread(target=kafka_get_data, args=())
    t.setDaemon(True)
    t.start()
    return HttpResponse('Succes')


@api_view(['GET'])
def get_exhauster(request, pk):
    parameters_list = []
    data_set = SignalModel.objects.values('signal_name', 'id_sensor__name', 'id_sensor__unit').filter(id_exhauster=pk)
    for data in data_set:
        parameter_dict = {'signal_name': data['signal_name'], 'sensor_name': data['id_sensor__name'],
                          'unit': data['id_sensor__unit']}
        parameters_list.append(parameter_dict)

    data_dict = {'id': pk, 'params': parameters_list}
    response_data = {'exhauster': data_dict}

    return HttpResponse(json.dumps(response_data), content_type="application/json")


@api_view(['POST'])
def get_graphic(request):
    signal_list = request.data.get('signals')
    result_data = {}
    time_list = []
    time_values = KafkaDataModel.objects.values_list('moment')[:10]
    for time in time_values:
        time_list.append(time[0])
    result_data['moment'] = time_list

    for signal in signal_list:
        param = KEYS_OF_FIELD[signal]
        signal_values = KafkaDataModel.objects.values_list(f'{param}')[:10]
        value_list = []
        for value in signal_values:
            value_list.append(value[0])

        result_data[signal] = value_list

    return HttpResponse(json.dumps(result_data), content_type='application/json')
