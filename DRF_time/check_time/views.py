from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status, exceptions
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.reverse import reverse
from .serializers import CheckTimeSerializer, CheckTimePlusDeltaSerializer
from .utils import check_time_by_global


@csrf_exempt
def time_is_right(request):
    if request.method == 'POST':
        try:
            data = JSONParser().parse(request)
        except exceptions.APIException:
            return HttpResponseBadRequest("The server could not understand the request due to invalid syntax.")

        serializer = CheckTimeSerializer(data=data)
        if serializer.is_valid():
            if check_time_by_global(serializer):
                return JsonResponse({'result': 'True'})
            else:
                return JsonResponse({'result': 'False'})
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return HttpResponseBadRequest('The server only provides post-requests in json format. '
                                      'Example: { "time": "12:00" }')


@csrf_exempt
def time_plus_delta_is_right(request):
    if request.method == 'POST':
        try:
            data = JSONParser().parse(request)
        except exceptions.APIException:
            return HttpResponseBadRequest("The server could not understand the request due to invalid syntax.")

        serializer = CheckTimePlusDeltaSerializer(data=data)
        if serializer.is_valid():
            if check_time_by_global(serializer, delta=True):
                return JsonResponse({'result': 'True'})
            else:
                return JsonResponse({'result': 'False'})
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return HttpResponseBadRequest('The server only provides post-requests in json format. '
                                      'Example: { "delta": "01:30", "time": "12:00" }')


@api_view(['GET'])
def api_root(request):
    return Response({
        'Checking time': reverse('time-is-right', request=request),
        'Checking time in delta': reverse('time-plus-delta-is-right', request=request)
    })
