from django.shortcuts import get_object_or_404
from django.http import  JsonResponse
from puntuaciones.models import Partida, Jugador, Torneo, Jugada
from puntuaciones.serializers import  JugadaSerializer, JugadaPOSTSerializer
from rest_framework.decorators import api_view
    
        

#LISTAR Y CREAR JUGADAS
@api_view(['GET','POST'])
def jugadas_list_create(request):
    
    #LISTAR JUGADAS (GET)
    if request.method == 'GET':
        try:
            jugadas = JugadaSerializer(Jugada.objects.all(), many=True)  
        
            return JsonResponse(jugadas.data, safe=False)
        except:
            return JsonResponse({"message":"Ha ocurrido un error inesperado", "status":500}, safe=False)
        
    #CREACIÓN JUGADA (POST) 
    if request.method == 'POST':
        try:
            if not request.user.is_authenticated:
                raise PermissionError
            
            #Nos aseguramos de que no pueda establecer una jugada si la partida no le pertenece al usuario
            if not Partida.objects.filter(torneo__usuario=request.user.id).get(id=request.data['partida']):
                raise Partida.DoesNotExist

            
            jugada = Jugada(None, request.data['jugador'], request.data['partida'], request.data['puntuacion'])
            serializer = JugadaPOSTSerializer(data=request.data,many=False)
                
            if serializer.is_valid():
                jugada.save()
                return JsonResponse({"message":"La jugada se ha creado exitosamente", "status":200}, status=200, safe=False)
            
            raise ValueError
            
        except (ValueError, KeyError):
            return JsonResponse(data={"message":"Los datos introducidos no son válidos", "status":400},
                                status=400, safe=False)
        
        except PermissionError:
            return JsonResponse({"message":"Debes identificarte para acceder a este recurso", "status":401}, status=401)
        
        except Partida.DoesNotExist:
            return JsonResponse(data={"message":"La partida a la que intentas apuntar la jugada no existe", "status":404},
                                status=404, safe=False)
        
        except:
            return JsonResponse(data={"message":"Error inesperado", "status":500},
                                status=500, safe=False)



#DETALLES, EDICIÓN Y ELIMINACIÓN DE JUGADAS
@api_view(['GET','PUT','DELETE'])
def jugadas_details_edit_delete(request,id):
    
    #DETALLES DE JUGADA (GET)
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
        
    #EDICIÓN DE JUGADA (PUT)
    if request.method == 'PUT':
        try:
            if not request.user.is_authenticated:
                raise PermissionError
            
            #Nos aseguramos de que no pueda establecer una jugada si la partida no le pertenece al usuario
            if not Partida.objects.filter(torneo__usuario=request.user.id).get(id=request.data['partida']):
                raise Partida.DoesNotExist
            
            
            
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
          
        except Partida.DoesNotExist:
            return JsonResponse(data={"message":"La partida a la que intentas apuntar la jugada no existe", "status":404},
                                status=404, safe=False)
            
        except PermissionError:
            return JsonResponse({"message":"Debes identificarte para acceder a este recurso", "status":401}, status=401)
        
        except:
            return JsonResponse(data={"message":"Error inesperado", "status":500},
                                status=500, safe=False)
         
    #ELIMINACIÓN DE JUGADA (DELETE)
    if request.method == 'DELETE':
        try:
            if not request.user.is_authenticated:
                raise PermissionError
            
            jugada = Jugada.objects.get(id=id)
            
            if jugada:
                jugada.delete()
                return JsonResponse({"message":"La jugada se ha borrado correctamente", "status":200}, status=200, safe=False)
        
            return JsonResponse({"message":"No se ha podido borrar la jugada", "status":400}, status=200, safe=False)
           
        except Jugada.DoesNotExist:   
            return JsonResponse(data={"message":"La jugada que intentas borrar no existe", "status":404},
                                status=404, safe=False)
         
        except PermissionError:
            return JsonResponse({"message":"Debes identificarte para acceder a este recurso", "status":401}, status=401)
         
        except:
            return JsonResponse(data={"message":"Error inesperado", "status":500},
                                status=500, safe=False)
            