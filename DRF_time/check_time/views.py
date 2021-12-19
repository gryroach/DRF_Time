from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .serializers import CheckTimeSerializer
from django.utils import timezone


@csrf_exempt
def time_is_right(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = CheckTimeSerializer(data=data)
        if serializer.is_valid():
            if serializer.data.get('time') == timezone.localtime().strftime("%H:%M"):
                return JsonResponse({'result': 'True'})
            else:
                return JsonResponse({'result': 'False'})
        return JsonResponse({'error': 'The time entered is not in the correct format'})
