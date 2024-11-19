from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('matchmaking/', views.matchmaking_api, name='matchmaking_api'),
]