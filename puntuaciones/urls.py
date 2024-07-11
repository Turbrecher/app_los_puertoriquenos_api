from django.contrib import admin
from django.urls import path, include
from .views import partidas_list_create, partidas_details_edit_delete, jugadores_list_create, jugadores_details_edit_delete, torneos_list_create, torneos_details_edit_delete, jugadas_details_edit_delete, jugadas_list_create

urlpatterns = [
    #PARTIDAS
    path('partidas/', view=partidas_list_create),#listar y crear (GET, POST)
    path('partidas/<id>', view=partidas_details_edit_delete),#detalles, editar y eliminar (GET, PUT, DELETE)
    
    #JUGADORES
    path('jugadores/', view=jugadores_list_create),#listar y crear (GET, POST)
    path('jugadores/<id>', view=jugadores_details_edit_delete),#detalles, editar y eliminar (GET, PUT, DELETE)
    
    #TORNEOS
    path('torneos/', view=torneos_list_create),#listar y crear (GET, POST)
    path('torneos/<id>', view=torneos_details_edit_delete),#detalles, editar y eliminar (GET, PUT, DELETE)
    
    #JUGADAS
    path('jugadas/', view=jugadas_list_create),#listar y crear (GET, POST)
    path('jugadas/<id>', view=jugadas_details_edit_delete),#detalles, editar y eliminar (GET, PUT, DELETE)
]