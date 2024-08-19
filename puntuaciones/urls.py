from django.contrib import admin
from django.urls import path, include
from puntuaciones.views import authentication, jugadas, jugadores, partidas, torneos, puntuaciones

urlpatterns = [
    #PARTIDAS
    path('partidas/', partidas.partidas_list_create),#listar y crear (GET, POST)
    path('partidas/nuevaid', partidas.obtenerSiguienteId),#siguiente id para nueva partida (GET)
    path('partidas/<id>', partidas.partidas_details_edit_delete),#detalles, editar y eliminar (GET, PUT, DELETE)
    
    #JUGADORES
    path('jugadores/', jugadores.jugadores_list_create),#listar y crear (GET, POST)
    path('jugadores/<id>', jugadores.jugadores_details_edit_delete),#detalles, editar y eliminar (GET, PUT, DELETE)
    
    #TORNEOS
    path('torneos/', torneos.torneos_list_create),#listar y crear (GET, POST)
    path('torneos/<id>', torneos.torneos_details_edit_delete),#detalles, editar y eliminar (GET, PUT, DELETE)
    
    #JUGADAS
    path('jugadas/', jugadas.jugadas_list_create),#listar y crear (GET, POST)
    path('jugadas/<id>', jugadas.jugadas_details_edit_delete),#detalles, editar y eliminar (GET, PUT, DELETE)
    
    #PUNTUACIONES
    path('puntuacionestorneo/<idTorneo>', puntuaciones.puntuacionesTorneo),#detalles, editar y eliminar (GET, PUT, DELETE)
    path('puntuacionespartida/<idPartida>', puntuaciones.puntuacionesPartida),#detalles, editar y eliminar (GET, PUT, DELETE)
    
    #AUTENTICACION
    path('login', authentication.login),#login
    path('register', authentication.register),#register
    path('profile', authentication.profile),#profile
    path('editprofile', authentication.edit_profile),#edit profile
    path('deleteuser', authentication.delete_user),#delete profile
    path('getusername/<id>', authentication.get_user_name),#get username
    
    
]