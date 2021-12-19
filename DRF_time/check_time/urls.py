from django.urls import path

from .views import time_is_right, time_plus_delta_is_right

urlpatterns = [
    path('time-is-right/', time_is_right),
    path('time-plus-delta-if-right/', time_plus_delta_is_right)
]
