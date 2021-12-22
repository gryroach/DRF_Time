from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status, exceptions
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.reverse import reverse
from .serializers import CheckTimeSerializer, CheckTimePlusDeltaSerializer
from .utils import check_time_by_global, env


@csrf_exempt
def time_is_right(request):
    if request.method == 'POST':
        try:
            data = JSONParser().parse(request)
        except exceptions.APIException:
            return HttpResponseBadRequest("The server could not understand the request due to invalid syntax.")

        if 'delta' not in data:
            data['delta'] = env.str('DELTA_TIME_DEFAULT')
        serializer = CheckTimePlusDeltaSerializer(data=data)
        if serializer.is_valid():
            return JsonResponse({'result': check_time_by_global(serializer, delta=True)})
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return HttpResponseBadRequest('The server only provides post-requests in json format. '
                                      'Example: { "time": "12:00", "delta": "01:30" }')


@api_view(['GET'])
def api_root(request):
    return Response({
        'Checking time in delta': reverse('time-is-right', request=request),
    })
