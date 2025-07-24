from django.urls import path
from .views import *

app_name = 'speech'
urlpatterns = [
    path('', home, name='list'),
]