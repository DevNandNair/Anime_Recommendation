# myapp/urls.py

from django.urls import path
from . import views
from django.http import HttpResponse


app_name='myapp'

urlpatterns = [
    # Other URL patterns...
    path('', views.recommend_anime, name='recommend_anime'),
     path('favicon.ico', views.no_favicon, name='no_favicon'),
]
