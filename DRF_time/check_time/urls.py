from django.urls import path

from .views import time_is_right, time_plus_delta_is_right, api_root

urlpatterns = [
    path('time-is-right/', time_is_right, name='time-is-right'),
    path('time-plus-delta-is-right/', time_plus_delta_is_right, name='time-plus-delta-is-right'),
    path('', api_root),
]
