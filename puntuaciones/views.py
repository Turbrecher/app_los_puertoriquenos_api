from django.shortcuts import get_object_or_404
from django.http import HttpResponse, JsonResponse
from .models import Partida, Jugador, Torneo, Jugada
from .serializers import PartidaSerializer, PartidaPOSTSerializer, JugadorSerializer, TorneoSerializer, JugadaSerializer, JugadaPOSTSerializer
from rest_framework.decorators import api_view










#PARTIDAS
#PARTIDAS
#PARTIDAS

#Listar y Crear.
@api_view(['GET','POST'])
def partidas_list_create(request):
    
    #lista
    if request.method == 'GET':
        try:
            partidas = PartidaSerializer(Partida.objects.all(), many=True)
            return JsonResponse(partidas.data, safe=False)
    
        except:
            return JsonResponse({"message":"Ha ocurrido un error inesperado", "status":500}, safe=False)
        
    #creacion 
    if request.method == 'POST':
        try:
            partida = Partida(None, request.data['nombre'].upper(), request.data['fecha'].upper(), request.data['torneo'])
            serializer = PartidaPOSTSerializer(data=request.data,many=False)
            
            if serializer.is_valid():
                partida.save()
                return JsonResponse({"message":"La partida se ha creado exitosamente", "status":200}, status=200, safe=False)
            
            raise ValueError
            
        except (ValueError, KeyError):
            return JsonResponse(data={"message":"Los datos introducidos no son válidos", "status":400, "errors":serializer.errors},
                                status=400, safe=False)
        
        except:
            return JsonResponse(data={"message":"Error inesperado", "status":500},
                                status=500, safe=False)



#Detalles, Edicion y Borrado.
@api_view(['GET', 'PUT', 'DELETE'])
def partidas_details_edit_delete(request, id):
    
    #detalles
    if request.method == 'GET':
        try:
            partida = PartidaSerializer(Partida.objects.get(id=id), many=False)
        
            return JsonResponse(partida.data, safe=False)
        
        except Partida.DoesNotExist:
            return JsonResponse(data={"message":"La partida no existe", "status":404},
                                status=404, safe=False)
            
        except ValueError:
            return JsonResponse(data={"message":"Las partidas deben filtrarse por su identificador, es decir, un numero entero", "status":501},
                                status=501, safe=False)
            
        except:
            return JsonResponse({"message":"Ha ocurrido un error inesperado", "status":500}, safe=False)
        
    
    #edicion
    if request.method == 'PUT':
        try:
            partida = Partida.objects.get(id = id)
            serializer = PartidaPOSTSerializer(data=request.data,many=False, instance=partida)
            
            if serializer.is_valid():
                partida.nombre = request.data['nombre'].upper()
                partida.fecha = request.data['fecha'].upper()
                partida.torneo = get_object_or_404(Torneo, pk = request.data['torneo'])
                partida.save()
                return JsonResponse({"message":"La partida se ha editado exitosamente", "status":200}, status=200, safe=False)
            
            raise ValueError
            
        except (ValueError, KeyError):
            return JsonResponse(data={"message":"Los datos introducidos no son válidos", "status":400},
                                status=400, safe=False)
            
        except Partida.DoesNotExist:
            return JsonResponse(data={"message":"La partida que intentas editar no existe", "status":404},
                                status=404, safe=False)
        
        except:
            return JsonResponse(data={"message":"Error inesperado", "status":500},
                                status=500, safe=False)
         
    #borrado
    if request.method == 'DELETE':
        try:
            partida = Partida.objects.get(id=id)
            print(partida)
            
            if partida:
                partida.delete()
                return JsonResponse({"message":"La partida se ha borrado correctamente", "status":200}, status=200, safe=False)
        
            return JsonResponse({"message":"No se ha podido borrar la partida", "status":400}, status=200, safe=False)
           
        except Partida.DoesNotExist:   
            return JsonResponse(data={"message":"La partida que intentas borrar no existe", "status":404},
                                status=404, safe=False)
         
        except:
            return JsonResponse(data={"message":"Error inesperado", "status":500},
                                status=500, safe=False)










#JUGADORES
#JUGADORES
#JUGADORES

#Listar y Crear.
@api_view(['GET','POST'])
def jugadores_list_create(request):
    
    #lista
    if request.method == 'GET':
        try:
            jugadores = JugadorSerializer(Jugador.objects.all(), many=True)
            return JsonResponse(jugadores.data, safe=False)
    
        except:
            return JsonResponse({"message":"Ha ocurrido un error inesperado", "status":500}, safe=False)
        
    #creacion 
    if request.method == 'POST':
        try:
            jugador = Jugador(None, request.data['nombre'].upper(), request.data['apellidos'].upper(), request.data['username'].upper())
            serializer = JugadorSerializer(data=request.data,many=False)
            
            if serializer.is_valid():
                jugador.save()
                return JsonResponse({"message":"El jugador se ha creado exitosamente", "status":200}, status=200, safe=False)
            
            raise ValueError
            
        except (ValueError, KeyError):
            return JsonResponse(data={"message":"Los datos introducidos no son válidos", "status":400},
                                status=400, safe=False)
        
        except:
            return JsonResponse(data={"message":"Error inesperado", "status":500},
                                status=500, safe=False)
    
    
    
#Detalles, Edición y Borrado.
@api_view(['GET','PUT','DELETE'])
def jugadores_details_edit_delete(request,id):
    
    #detalles
    if request.method == 'GET':
        try:  
            jugador = JugadorSerializer(Jugador.objects.get(id=id), many=False)
                    
            return JsonResponse(jugador.data, safe=False)
        
        except Jugador.DoesNotExist:
            return JsonResponse({"message":"El jugador que buscas no existe", "status":404}, status=404, safe=False)
        
        except ValueError:
            return JsonResponse(data={"message":"Los jugadores deben filtrarse por su identificador, es decir, un numero entero"},
                                status=501, safe=False)
            
        except:
            return JsonResponse({"message":"Ha ocurrido un error inesperado", "status":500}, status=500, safe=False)
        
    
    #edicion
    if request.method == 'PUT':
        try:
            jugador = Jugador.objects.get(id = id)
            serializer = JugadorSerializer(data=request.data,many=False)
            
            if serializer.is_valid():
                jugador.nombre = request.data['nombre'].upper()
                jugador.apellidos = request.data['apellidos'].upper()
                jugador.username = request.data['username'].upper()
                jugador.save()
                return JsonResponse({"message":"El jugador se ha editado exitosamente", "status":200}, status=200, safe=False)
            
            raise ValueError
            
        except (ValueError, KeyError):
            return JsonResponse(data={"message":"Los datos introducidos no son válidos", "status":400},
                                status=400, safe=False)
            
        except Jugador.DoesNotExist:
            return JsonResponse(data={"message":"El jugador que intentas editar no existe", "status":404},
                                status=404, safe=False)
        
        except:
            return JsonResponse(data={"message":"Error inesperado", "status":500},
                                status=500, safe=False)
         
    #borrado
    if request.method == 'DELETE':
        try:
            jugador = Jugador.objects.get(id=id)
            
            if jugador:
                jugador.delete()
                return JsonResponse({"message":"El jugador se ha borrado correctamente", "status":200}, status=200, safe=False)
        
            return JsonResponse({"message":"No se ha podido borrar el jugador", "status":400}, status=200, safe=False)
           
        except Partida.DoesNotExist:   
            return JsonResponse(data={"message":"El jugador que intentas borrar no existe", "status":404},
                                status=404, safe=False)
         
        except:
            return JsonResponse(data={"message":"Error inesperado", "status":500},
                                status=500, safe=False)
 
 
 
 
 
    
    



#TORNEOS
#TORNEOS
#TORNEOS


#Listar y Crear.
@api_view(['GET','POST'])
def torneos_list_create(request):
    
    #lista
    if request.method == 'GET':
        try:
            torneos = TorneoSerializer(Torneo.objects.all(), many=True)  
        
            return JsonResponse(torneos.data, safe=False)
        except:
            return JsonResponse({"message":"Ha ocurrido un error inesperado", "status":500}, safe=False)
        
    #creacion 
    if request.method == 'POST':
        try:
            torneo = Torneo(None, request.data['nombre'].upper(), request.data['fechaInicio'].upper(), request.data['fechaFinal'].upper())
            serializer = TorneoSerializer(data=request.data,many=False)
            
            if serializer.is_valid():
                torneo.save()
                return JsonResponse({"message":"El torneo se ha creado exitosamente", "status":200}, status=200, safe=False)
            
            raise ValueError
            
        except (ValueError, KeyError):
            return JsonResponse(data={"message":"Los datos introducidos no son válidos", "status":400},
                                status=400, safe=False)
        
        except:
            return JsonResponse(data={"message":"Error inesperado", "status":500},
                                status=500, safe=False)



#Detalles, Edición y Borrado.
@api_view(['GET','PUT','DELETE'])
def torneos_details_edit_delete(request,id):
    
    #detalles
    if request.method == 'GET':
        try:
            torneos = TorneoSerializer(Torneo.objects.get(id=id), many=False)  
        
            return JsonResponse(torneos.data, safe=False)
        
        except Torneo.DoesNotExist:
            return JsonResponse({"message":"El torneo que buscas no existe", "status":404}, status=404, safe=False)
        
        except ValueError:
            return JsonResponse({"message":"Debe filtrar los torneos por su identificador numérico", "status":501}, status=501, safe=False)
        
        except:
            return JsonResponse({"message":"Ha ocurrido un error inesperado", "status":500}, safe=False)
        
    #edicion
    if request.method == 'PUT':
        try:
            torneo = Torneo.objects.get(id = id)
            serializer = TorneoSerializer(data=request.data,many=False)
            
            if serializer.is_valid():
                torneo.nombre = request.data['nombre'].upper()
                torneo.fechaInicio = request.data['fechaInicio'].upper()
                torneo.fechaFinal = request.data['fechaFinal'].upper()
                torneo.save()
                return JsonResponse({"message":"El torneo se ha editado exitosamente", "status":200}, status=200, safe=False)
            
            raise ValueError
            
        except (ValueError, KeyError):
            return JsonResponse(data={"message":"Los datos introducidos no son válidos", "status":400},
                                status=400, safe=False)
            
        except Torneo.DoesNotExist:
            return JsonResponse(data={"message":"El torneo que intentas editar no existe", "status":404},
                                status=404, safe=False)
        
        except:
            return JsonResponse(data={"message":"Error inesperado", "status":500},
                                status=500, safe=False)
         
    #borrado
    if request.method == 'DELETE':
        try:
            torneo = Torneo.objects.get(id=id)
            
            if torneo:
                torneo.delete()
                return JsonResponse({"message":"El torneo se ha borrado correctamente", "status":200}, status=200, safe=False)
        
            return JsonResponse({"message":"No se ha podido borrar el torneo", "status":400}, status=200, safe=False)
           
        except Torneo.DoesNotExist:   
            return JsonResponse(data={"message":"El torneo que intentas borrar no existe", "status":404},
                                status=404, safe=False)
         
        except:
            return JsonResponse(data={"message":"Error inesperado", "status":500},
                                status=500, safe=False)
        
        
        
        
        
        
        
        
        
            
#JUGADAS
#JUGADAS
#JUGADAS

#Listar y Crear.
@api_view(['GET','POST'])
def jugadas_list_create(request):
    
    #lista
    if request.method == 'GET':
        try:
            jugadas = JugadaSerializer(Jugada.objects.all(), many=True)  
        
            return JsonResponse(jugadas.data, safe=False)
        except:
            return JsonResponse({"message":"Ha ocurrido un error inesperado", "status":500}, safe=False)
        
    #creacion 
    if request.method == 'POST':
        try:
            jugada = Jugada(None, request.data['jugador'], request.data['partida'], request.data['puntuacion'])
            serializer = JugadaPOSTSerializer(data=request.data,many=False)
            
            
            if serializer.is_valid():
                jugada.save()
                return JsonResponse({"message":"La jugada se ha creado exitosamente", "status":200}, status=200, safe=False)
            
            raise ValueError
            
        except (ValueError, KeyError):
            return JsonResponse(data={"message":"Los datos introducidos no son válidos", "status":400},
                                status=400, safe=False)
        
        except:
            return JsonResponse(data={"message":"Error inesperado", "status":500},
                                status=500, safe=False)



#Detalles, Edición y Borrado.
@api_view(['GET','PUT','DELETE'])
def jugadas_details_edit_delete(request,id):
    
    #detalles
    if request.method == 'GET':
        try:
            jugada = JugadaSerializer(Jugada.objects.get(id=id), many=False)  
        
            return JsonResponse(jugada.data, safe=False)
        
        except Jugada.DoesNotExist:
            return JsonResponse({"message":"La jugada que buscas no existe", "status":404}, status=404, safe=False)
        
        except ValueError:
            return JsonResponse({"message":"Debe filtrar las jugadas por su identificador numérico", "status":501}, status=501, safe=False)
        
        except:
            return JsonResponse({"message":"Ha ocurrido un error inesperado", "status":500}, safe=False)
        
    #edicion
    if request.method == 'PUT':
        try:
            jugada = Jugada.objects.get(id = id)
            serializer = JugadaPOSTSerializer(data=request.data,many=False,instance=jugada)
            
            if serializer.is_valid():
                jugada.jugador = get_object_or_404(Jugador,pk = request.data['jugador'])
                jugada.partida = get_object_or_404(Partida, pk = request.data['partida'])
                jugada.puntuacion = request.data['puntuacion']
                jugada.save()
                return JsonResponse({"message":"La jugada se ha editado correctamente", "status":200}, status=200, safe=False)
            
            raise ValueError
            
        except (ValueError, KeyError):
            return JsonResponse(data={"message":"Los datos introducidos no son válidos", "status":400},
                                status=400, safe=False)
            
        except Jugada.DoesNotExist:
            return JsonResponse(data={"message":"La jugada que intentas editar no existe", "status":404},
                                status=404, safe=False)
        
        except:
            return JsonResponse(data={"message":"Error inesperado", "status":500},
                                status=500, safe=False)
         
    #borrado
    if request.method == 'DELETE':
        try:
            jugada = Jugada.objects.get(id=id)
            
            if jugada:
                jugada.delete()
                return JsonResponse({"message":"La jugada se ha borrado correctamente", "status":200}, status=200, safe=False)
        
            return JsonResponse({"message":"No se ha podido borrar la jugada", "status":400}, status=200, safe=False)
           
        except Jugada.DoesNotExist:   
            return JsonResponse(data={"message":"La jugada que intentas borrar no existe", "status":404},
                                status=404, safe=False)
         
        except:
            return JsonResponse(data={"message":"Error inesperado", "status":500},
                                status=500, safe=False)
            
            
            
            






#PUNTUACIONES GENERALES
#Esta función devuelve todas las jugadas de un torneo especifico en formato json
@api_view(['GET'])
def puntuacionesGenerales(request, id):
    try:
        #Obtenemos todas las jugadas y las partidas del torneo elegido.
        jugadas = Jugada.objects.filter(partida__torneo__id=id)
        jugadasList = []
        
        for jugada in jugadas:
            jugadasList.append(jugada.json())
        
        return JsonResponse(data={"message":jugadasList, "status":200}, status=200, safe=False)
            
    except:
        return JsonResponse(status=500, data={"message":"Ha ocurrido un error inesperado", "status":400})
        
    