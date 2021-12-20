import datetime

from django.http import JsonResponse, HttpResponseBadRequest
from django.utils.datastructures import MultiValueDictKeyError
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from .serializers import CheckTimeSerializer, CheckTimePlusDeltaSerializer
from django.utils import timezone
from datetime import timedelta


@csrf_exempt
def time_is_right(request):
    if request.method == 'POST':
        try:
            data = {"time": request.GET['time']}
            serializer = CheckTimeSerializer(data=data)
            if serializer.is_valid():
                if serializer.data.get('time') == timezone.localtime().strftime("%H:%M"):
                    return JsonResponse({'result': 'True'})
                else:
                    return JsonResponse({'result': 'False'})
            return JsonResponse(serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)
        except MultiValueDictKeyError:
            return HttpResponseBadRequest('The server could not understand the request due to invalid syntax. '
                                          'Check the spelling of the "time" parameter.')
    else:
        return HttpResponseBadRequest('The server only provides post-requests with parameter "time".')


@csrf_exempt
def time_plus_delta_is_right(request):
    if request.method == 'POST':
        try:
            data = {"time": request.GET['time'], "delta": request.GET['delta']}
            serializer = CheckTimePlusDeltaSerializer(data=data)
            if serializer.is_valid():
                delta = timedelta(hours=int(serializer.data.get('delta').split(':')[0]),
                                  minutes=int(serializer.data.get('delta').split(':')[1]),
                                  seconds=int(serializer.data.get('delta').split(':')[2]))
                input_time = datetime.datetime(year=timezone.datetime.now().year, month=timezone.datetime.now().month,
                                               day=timezone.datetime.now().day,
                                               hour=int(serializer.data.get('time').split(':')[0]),
                                               minute=int(serializer.data.get('time').split(':')[1]),
                                               second=int(serializer.data.get('time').split(':')[2]))
                if timezone.datetime.now() - delta <= input_time <= timezone.datetime.now() + delta:
                    return JsonResponse({'result': 'True'})
                else:
                    return JsonResponse({'result': 'False'})
            return JsonResponse(serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)
        except MultiValueDictKeyError:
            return HttpResponseBadRequest('The server could not understand the request due to invalid syntax. '
                                          'Check the spelling of the "time", "delta" parameters.')
    else:
        return HttpResponseBadRequest('The server only provides post-requests with parameters "time", "delta".')


@api_view(['GET'])
def api_root(request):
    return Response({
        'Checking time': reverse('time-is-right', request=request),
        'Checking time in delta': reverse('time-plus-delta-is-right', request=request)
    })
