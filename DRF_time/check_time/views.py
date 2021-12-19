from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status, exceptions
from rest_framework.parsers import JSONParser
from .serializers import CheckTimeSerializer
from django.utils import timezone


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
