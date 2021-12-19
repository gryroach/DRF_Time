from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status, exceptions
from rest_framework.parsers import JSONParser
from .serializers import CheckTimeSerializer, CheckTimePlusDeltaSerializer
from django.utils import timezone
from datetime import timedelta, time


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


@csrf_exempt
def time_plus_delta_is_right(request):
    if request.method == 'POST':
        try:
            data = JSONParser().parse(request)
            serializer = CheckTimePlusDeltaSerializer(data=data)
            if serializer.is_valid():
                delta = timedelta(hours=int(serializer.data.get('delta').split(':')[0]),
                                  minutes=int(serializer.data.get('delta').split(':')[1]))

                print(delta)
                print((timezone.localtime() - delta).time())
                print((timezone.localtime() + delta).time())
                print(time(hour=int(serializer.data.get('time').split(':')[0]), minute=int(serializer.data.get('time').split(':')[1])))
                # incorrect result where delta > 1h and localtime about 00:00
                if (timezone.localtime() - delta).time() <= \
                        time(hour=int(serializer.data.get('time').split(':')[0]),
                             minute=int(serializer.data.get('time').split(':')[1])) <= \
                        (timezone.localtime() + delta).time():

                    return JsonResponse({'result': 'True'})
                else:
                    return JsonResponse({'result': 'False'})
            return JsonResponse(serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)
        except exceptions.APIException:
            return HttpResponseBadRequest("The server could not understand the request due to invalid syntax.")
