from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='Home'),
    path('diario/<str:slug>', views.diario, name='diario'),
    path('tournament', views.tournamentTable, name = 'torneo'),
]
