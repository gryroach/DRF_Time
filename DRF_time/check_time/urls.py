from django.urls import path

from .views import time_is_right, api_root

urlpatterns = [
    path('time-is-right/', time_is_right, name='time-is-right'),
    path('', api_root),
]
