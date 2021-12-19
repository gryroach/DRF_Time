from django.urls import path
from .views import time_is_correct

urlpatterns = [
    path('time/', time_is_correct)
]
