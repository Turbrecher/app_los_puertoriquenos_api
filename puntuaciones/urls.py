from django.contrib import admin
from django.urls import path, include
from .views import listPartidas, getPartida, listJugadores, getJugador, listTorneos, getTorneo

urlpatterns = [
    path('partidas/', view=listPartidas),
    path('partidas/<id>', view=getPartida),
    path('jugadores/', view=listJugadores),
    path('jugadores/<id>', view=getJugador),
    path('torneos/', view=listTorneos),
    path('torneos/<id>', view=getTorneo)
]