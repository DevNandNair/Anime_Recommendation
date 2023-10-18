# myapp/urls.py

from django.urls import path
from . import views

app_name='myapp'

urlpatterns = [
    # Other URL patterns...
    path('', views.recommend_anime, name='recommend_anime'),
]
