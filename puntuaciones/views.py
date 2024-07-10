from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from .models import Partida, Jugador, Torneo
from .serializers import PartidaSerializer, JugadorSerializer, TorneoSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status





#PARTIDAS
#lista
@api_view(['GET'])
def listPartidas(request):
    try:
        partidas = PartidaSerializer(Partida.objects.all(), many=True)
        return JsonResponse(partidas.data, safe=False)
    
    except:
         return JsonResponse({"message":"Ha ocurrido un error inesperado", "status":500}, safe=False)

#detalles
@api_view(['GET'])
def getPartida(request, id):
    
    try:
        partida = PartidaSerializer(Partida.objects.get(id=id), many=False)
    
        return JsonResponse(partida.data, safe=False)
    
    except Partida.DoesNotExist:
        return JsonResponse(data={"message":"La partida no existe", "status":404},
                            status=404, safe=False)
        
    except ValueError:
        return JsonResponse(data={"message":"Las partidas deben filtrarse por su identificador, es decir, un numero entero", "status":501},
                            status=501, safe=False)





#JUGADORES
#lista
@api_view(['GET'])
def listJugadores(request):
    try:
        jugadores = JugadorSerializer(Jugador.objects.all(), many=True)
        return JsonResponse(jugadores.data, safe=False)
    
    except:
        return JsonResponse({"message":"Ha ocurrido un error inesperado", "status":500}, status=500, safe=False)
    
#detalles
@api_view(['GET'])
def getJugador(request, id):
    
    try:  
        jugador = JugadorSerializer(Jugador.objects.get(id=id), many=False)
                
        return JsonResponse(jugador.data, safe=False)
    
    except Jugador.DoesNotExist:
        return JsonResponse({"message":"El jugador que buscas no existe", "status":404}, status=404, safe=False)
    
    except ValueError:
        return JsonResponse(data={"message":"Los jugadores deben filtrarse por su identificador, es decir, un numero entero"},
                            status=501, safe=False)





#TORNEOS
#lista
@api_view(['GET'])
def listTorneos(request):
    try:
        torneos = TorneoSerializer(Torneo.objects.all(), many=True)  
    
        return JsonResponse(torneos.data, safe=False)
    except:
        return JsonResponse({"message":"Ha ocurrido un error inesperado", "status":500}, safe=False)
    
#detalles
@api_view(['GET'])
def getTorneo(request, id):
    try:
        torneos = TorneoSerializer(Torneo.objects.get(id=id), many=False)  
    
        return JsonResponse(torneos.data, safe=False)
    
    except Torneo.DoesNotExist:
        return JsonResponse({"message":"El torneo que buscas no existe", "status":404}, status=404, safe=False)
    
    except ValueError:
        return JsonResponse({"message":"Debe filtrar los torneos por su identificador numérico", "status":501}, status=501, safe=False)
    