from django.http import  JsonResponse
from puntuaciones.models import Torneo
from puntuaciones.serializers import TorneoSerializer
from rest_framework.decorators import api_view

#LISTAR Y CREAR TORNEOS
@api_view(['GET','POST'])
def torneos_list_create(request):
    
    #LISTAR TORNEOS (GET)
    if request.method == 'GET':
        try:
            torneos = TorneoSerializer(Torneo.objects.all(), many=True)  
            
            #Si pide el recurso un usuario autenticado, solo devolverá sus torneos
            if(request.user.is_authenticated):
                torneos = TorneoSerializer(Torneo.objects.filter(usuario=request.user.id), many=True)
        
            return JsonResponse(torneos.data, safe=False)
        except:
            return JsonResponse(status=500,data={"message":"Ha ocurrido un error inesperado", "status":500}, safe=False)
        
    #CREACIÓN DE TORNEOS (POST)
    if request.method == 'POST':
        try:
            if(not request.user.is_authenticated):
                raise PermissionError
            
            #Guardamos como usuario de la peticion el usuario logueado.
            request.data['usuario'] = request.user.id
            
            torneo = Torneo(None, request.data['nombre'].upper(), request.data['fechaInicio'].upper(), request.data['fechaFinal'].upper(), request.user.id)
            serializer = TorneoSerializer(data=request.data,many=False)
            
            if serializer.is_valid():
                torneo.save()
                return JsonResponse(data= {"message":"El torneo se ha creado exitosamente", "status":200}, status=200, safe=False)
            
            raise ValueError
            
        except (ValueError, KeyError):
            return JsonResponse(data={"message":"Los datos introducidos no son válidos", "status":400},
                                status=400, safe=False)
        
        except PermissionError:
            return JsonResponse({"message":"Debes identificarte para acceder a este recurso", "status":401}, status=401)
        
        except:
            return JsonResponse(data={"message":"Error inesperado","errors":serializer.errors, "status":500},
                                status=500, safe=False)



#DETALLES, EDICIÓN Y BORRADO DE TORNEOS
@api_view(['GET','PUT','DELETE'])
def torneos_details_edit_delete(request,id):
    
    #DETALLES DE TORNEO (GET)
    if request.method == 'GET':
        try:
            torneos = TorneoSerializer(Torneo.objects.get(id=id), many=False)
            
            if request.user.is_authenticated:
                torneos = TorneoSerializer(Torneo.objects.filter(usuario=request.user.id).get(id=id), many=False)  
        
            return JsonResponse(torneos.data, safe=False)
        
        except Torneo.DoesNotExist:
            return JsonResponse({"message":"El torneo que buscas no existe", "status":404}, status=404, safe=False)
        
        except ValueError:
            return JsonResponse({"message":"Debe filtrar los torneos por su identificador numérico", "status":501}, status=501, safe=False)
        
        except:
            return JsonResponse({"message":"Ha ocurrido un error inesperado", "status":500}, safe=False)
        
    #EDICIÓN DE TORNEO (PUT)
    if request.method == 'PUT':
        try:
            if(not request.user.is_authenticated):
                raise PermissionError
            
            request.data['usuario'] = request.user.id
            
            torneo = Torneo.objects.filter(usuario=request.user.id).get(id = id)
            serializer = TorneoSerializer(data=request.data,many=False, instance=torneo)
            
            if serializer.is_valid():
                torneo.nombre = request.data['nombre'].upper()
                torneo.fechaInicio = request.data['fechaInicio'].upper()
                torneo.fechaFinal = request.data['fechaFinal'].upper()
                torneo.save()
                return JsonResponse({"message":"El torneo se ha editado exitosamente", "status":200}, status=200, safe=False)
            
            raise ValueError
            
        except (ValueError, KeyError):
            return JsonResponse(data={"message":"Los datos introducidos no son válidos", "status":400, "errors":serializer.errors},
                                status=400, safe=False)
            
        except Torneo.DoesNotExist:
            return JsonResponse(data={"message":"El torneo que intentas editar no existe", "status":404},
                                status=404, safe=False)
        
        except PermissionError:
            return JsonResponse({"message":"Debes identificarte para acceder a este recurso", "status":401}, status=401)
        
        except:
            return JsonResponse(data={"message":"Error inesperado", "status":500},
                                status=500, safe=False)
         
    #ELIMINACIÓN DE TORNEO (DELETE)
    if request.method == 'DELETE':
        try:
            if(not request.user.is_authenticated):
                raise PermissionError
            
            torneo = Torneo.objects.filter(usuario=request.user.id).get(id=id)
            
            if torneo:
                torneo.delete()
                return JsonResponse({"message":"El torneo se ha borrado correctamente", "status":200}, status=200, safe=False)
        
            return JsonResponse({"message":"No se ha podido borrar el torneo", "status":400}, status=200, safe=False)
           
        except Torneo.DoesNotExist:   
            return JsonResponse(data={"message":"El torneo que intentas borrar no existe", "status":404},
                                status=404, safe=False)
         
        except PermissionError:
            return JsonResponse({"message":"Debes identificarte para acceder a este recurso", "status":401}, status=401)
         
        except:
            return JsonResponse(data={"message":"Error inesperado", "status":500},
                                status=500, safe=False)