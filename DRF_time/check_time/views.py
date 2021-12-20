import datetime

from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status, exceptions
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.reverse import reverse
from .serializers import CheckTimeSerializer, CheckTimePlusDeltaSerializer
from django.utils import timezone
from datetime import timedelta


@csrf_exempt
def time_is_right(request):
    if request.method == 'POST':
        try:
            data = JSONParser().parse(request)
            serializer = CheckTimeSerializer(data=data)
            if serializer.is_valid():
                if serializer.data.get('time') == timezone.localtime().strftime("%H:%M"):
                    return JsonResponse({'result': 'True'})
                else:
                    return JsonResponse({'result': 'False'})
            return JsonResponse(serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)
        except exceptions.APIException:
            return HttpResponseBadRequest("The server could not understand the request due to invalid syntax.")
    elif request.method == 'GET':
        return HttpResponseBadRequest('The server only provides post-requests in json format. '
                                      'Example: { "time": "12:00" }')


@csrf_exempt
def time_plus_delta_is_right(request):
    if request.method == 'POST':
        try:
            data = JSONParser().parse(request)
            serializer = CheckTimePlusDeltaSerializer(data=data)
            if serializer.is_valid():
                delta = timedelta(hours=int(serializer.data.get('delta').split(':')[0]),
                                  minutes=int(serializer.data.get('delta').split(':')[1]))
                input_time = datetime.datetime(year=timezone.datetime.now().year, month=timezone.datetime.now().month,
                                               day=timezone.datetime.now().day,
                                               hour=int(serializer.data.get('time').split(':')[0]),
                                               minute=int(serializer.data.get('time').split(':')[1]))
                if timezone.datetime.now() - delta <= input_time <= timezone.datetime.now() + delta:
                    return JsonResponse({'result': 'True'})
                else:
                    return JsonResponse({'result': 'False'})
            return JsonResponse(serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)
        except exceptions.APIException:
            return HttpResponseBadRequest("The server could not understand the request due to invalid syntax.")
    elif request.method == 'GET':
        return HttpResponseBadRequest('The server only provides post-requests in json format. '
                                      'Example: { "delta": "01:30", "time": "12:00" }')


@api_view(['GET'])
def api_root(request):
    return Response({
        'Checking time': reverse('time-is-right', request=request),
        'Checking time in delta': reverse('time-plus-delta-is-right', request=request)
    })
