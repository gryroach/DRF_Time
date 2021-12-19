from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .serializers import CheckTimeSerializer


@csrf_exempt
def time_is_correct(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = CheckTimeSerializer(data=data)
        if serializer.is_valid():
            return JsonResponse({'result': 'true'})
        return JsonResponse({'result': 'false'})
