from django.urls import path
from .views import *

app_name = 'speech'
urlpatterns = [
    path('', speech_list, name='list'),
    path('<slug:speechSlug>', speech_detail, name='detail'),
]