from rest_framework import serializers
from rest_framework.settings import api_settings


class CheckTimePlusDeltaSerializer(serializers.Serializer):
    time = serializers.TimeField(format=api_settings.TIME_FORMAT)
    delta = serializers.TimeField(format='%H:%M:%S')
