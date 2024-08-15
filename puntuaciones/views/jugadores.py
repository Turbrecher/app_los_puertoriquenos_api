from django.http import JsonResponse
from puntuaciones.models import Partida, Jugador
from puntuaciones.serializers import  JugadorSerializer
from rest_framework.decorators import api_view

#LISTAR Y CREAR JUGADORES
@api_view(['GET','POST'])
def jugadores_list_create(request):
    
    #LISTAR (GET)
    if request.method == 'GET':
        try:
            if(not request.user.is_authenticated):
                raise PermissionError
            
            jugadores = JugadorSerializer(Jugador.objects.filter(usuario=request.user.id), many=True)
            return JsonResponse(jugadores.data, safe=False)
    
        except PermissionError:
            return JsonResponse({"message":"Debes identificarte para acceder a este recurso", "status":401}, status=401)
    
        except:
            return JsonResponse({"message":"Ha ocurrido un error inesperado", "status":500}, safe=False)
        
    #CREACIÓN (POST) 
    if request.method == 'POST':
        try:
            if(not request.user.is_authenticated):
                raise PermissionError
            
            jugador = Jugador(None, request.data['nombre'].upper(), request.data['apellidos'].upper(), request.data['username'].upper(), request.user.id)
            serializer = JugadorSerializer(data=request.data,many=False)
            
            if serializer.is_valid():
                jugador.save()
                return JsonResponse({"message":"El jugador se ha creado exitosamente", "status":200}, status=200, safe=False)
            
            raise ValueError
            
        except (ValueError, KeyError):
            return JsonResponse(data={"message":"Los datos introducidos no son válidos", "status":400},
                                status=400, safe=False)
        
        except PermissionError:
            return JsonResponse({"message":"Debes identificarte para acceder a este recurso", "status":401}, status=401)
        
        except:
            return JsonResponse(data={"message":"Error inesperado", "status":500},
                                status=500, safe=False)
    
    
    
#DETALLES, EDICIÓN Y ELIMINACIÓN DE JUGADORES.
@api_view(['GET','PUT','DELETE'])
def jugadores_details_edit_delete(request,id):
    
    #DETALLES DE JUGADOR (GET)
    if request.method == 'GET':
        try:  
            if(not request.user.is_authenticated):
                raise PermissionError
            
            jugador = JugadorSerializer(Jugador.objects.filter(usuario=request.user.id).get(id=id), many=False)
                    
            return JsonResponse(jugador.data, safe=False)
        
        except PermissionError:
            return JsonResponse(data={"message":"Debes autenticarte para acceder a este recurso"},
                                status=401, safe=False)
        
        except Jugador.DoesNotExist:
            return JsonResponse({"message":"El jugador que buscas no existe", "status":404}, status=404, safe=False)
        
        except ValueError:
            return JsonResponse(data={"message":"Los jugadores deben filtrarse por su identificador, es decir, un numero entero"},
                                status=501, safe=False)
            
        except:
            return JsonResponse({"message":"Ha ocurrido un error inesperado", "status":500}, status=500, safe=False)
        
    
    #EDICIÓN DE UN JUGADOR (PUT)
    if request.method == 'PUT':
        try:
            
            if(not request.user.is_authenticated):
                raise PermissionError
            
            jugador = Jugador.objects.filter(usuario = request.user.id).get(id = id)
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
        
        except PermissionError:
            return JsonResponse({"message":"Debes identificarte para acceder a este recurso", "status":401}, status=401)
        
        except:
            return JsonResponse(data={"message":"Error inesperado", "status":500},
                                status=500, safe=False)
         
    #ELIMINACIÓN DE UN JUGADOR (DELETE)
    if request.method == 'DELETE':
        try:
            
            if(not request.user.is_authenticated):
                raise PermissionError
            
            jugador = Jugador.objects.filter(usuario=request.user.id).get(id=id)
            
            if jugador:
                jugador.delete()
                return JsonResponse({"message":"El jugador se ha borrado correctamente", "status":200}, status=200, safe=False)
        
            return JsonResponse({"message":"No se ha podido borrar el jugador", "status":400}, status=200, safe=False)
           
        except Partida.DoesNotExist:   
            return JsonResponse(data={"message":"El jugador que intentas borrar no existe", "status":404},
                                status=404, safe=False)
         
        except PermissionError:
            return JsonResponse({"message":"Debes identificarte para acceder a este recurso", "status":401}, status=401)
         
        except:
            return JsonResponse(data={"message":"Error inesperado", "status":500},
                                status=500, safe=False)
            
            