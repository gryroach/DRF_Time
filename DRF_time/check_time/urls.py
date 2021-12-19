from django.urls import path
from .views import time_is_right

urlpatterns = [
    path('time_is_right/', time_is_right),
]
