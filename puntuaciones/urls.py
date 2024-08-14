from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    #PARTIDAS
    path('partidas/', views.partidas_list_create),#listar y crear (GET, POST)
    path('partidas/<id>', views.partidas_details_edit_delete),#detalles, editar y eliminar (GET, PUT, DELETE)
    
    #JUGADORES
    path('jugadores/', views.jugadores_list_create),#listar y crear (GET, POST)
    path('jugadores/<id>', views.jugadores_details_edit_delete),#detalles, editar y eliminar (GET, PUT, DELETE)
    
    #TORNEOS
    path('torneos/', views.torneos_list_create),#listar y crear (GET, POST)
    path('torneos/<id>', views.torneos_details_edit_delete),#detalles, editar y eliminar (GET, PUT, DELETE)
    
    #JUGADAS
    path('jugadas/', views.jugadas_list_create),#listar y crear (GET, POST)
    path('jugadas/<id>', views.jugadas_details_edit_delete),#detalles, editar y eliminar (GET, PUT, DELETE)
    
    #PUNTUACIONES
    path('puntuacionestorneo/<idTorneo>', views.puntuacionesTorneo),#detalles, editar y eliminar (GET, PUT, DELETE)
    path('puntuacionespartida/<idPartida>', views.puntuacionesPartida),#detalles, editar y eliminar (GET, PUT, DELETE)
    
    #AUTENTICACION
    path('login', views.login),#login
    path('register', views.register),#register
    path('profile', views.profile),#profile
    path('editprofile', views.edit_profile),#edit profile
    path('deleteuser', views.delete_user),#edit profile
    
    
]