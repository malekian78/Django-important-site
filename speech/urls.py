from django.urls import path
from .views import *

app_name = 'speech'
urlpatterns = [
    path('', speech_list, name='list'),
    path('<slug:speechSlug>', speech_detail, name='detail'),
    path("tags/<slug:slug>/", tag_detail, name="tag_detail"),
    path("<slug:slug>/favorite/", toggle_favorite, name="toggle_favorite"),
    # path("my-favorites/", my_favorites, name="my_favorites"),
]

# ! برای لیست سخنرانی های  محبوب
# {% for speech in favorites %}
#     <p>{{ speech.title }}</p>
# {% empty %}
#     <p>هنوز هیچ سخنرانی را پسند نکرده‌اید.</p>
# {% endfor %}