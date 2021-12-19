from django.urls import path

from .views import time_is_right

urlpatterns = [
    path('time-is-right/', time_is_right),
]
