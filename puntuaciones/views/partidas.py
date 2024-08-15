from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from puntuaciones.serializers import  PartidaSerializer, PartidaPOSTSerializer
from puntuaciones.models import  Partida, Torneo
from rest_framework.decorators import api_view



#LISTAR Y CREAR PARTIDAS.
@api_view(['GET','POST'])
def partidas_list_create(request):
    
    #LISTAR PARTIDAS (GET)
    if request.method == 'GET':
        try:
            partidas = PartidaSerializer(Partida.objects.all(), many=True)
            
            #Si pide el recurso un usuario autenticado, solo devolverá sus partidas.
            if(request.user.is_authenticated):
                partidas = PartidaSerializer(Partida.objects.filter(torneo__usuario=request.user.id), many=True)
            
            #Si el usuario quiere filtrar por torneo
            if request.GET.get('torneo'):
                partidas = PartidaSerializer(Partida.objects.filter(torneo__id=request.GET['torneo']), many=True)
               
            return JsonResponse(partidas.data, safe=False)
    
        except:
            return JsonResponse({"message":"Ha ocurrido un error inesperado", "status":500}, safe=False)
        
    #CREACION DE PARTIDA (POST) 
    if request.method == 'POST':
        try:
            if(not request.user.is_authenticated):
                raise PermissionError
            
            #Nos aseguramos de que no pueda establecer un torneo que no le pertenece al usuario
            if not Torneo.objects.filter(usuario=request.user.id).get(id=request.data['torneo']):
                raise Torneo.DoesNotExist
            
            partida = Partida(None, request.data['nombre'].upper(), request.data['fecha'].upper(), request.data['torneo'])
            serializer = PartidaPOSTSerializer(data=request.data,many=False)
            
            if serializer.is_valid():
                partida.save()
                return JsonResponse({"message":"La partida se ha creado exitosamente", "status":200, "partida":serializer.data, "id_partida":partida.id}, status=200, safe=False)
            
            raise ValueError
            
        except (ValueError, KeyError):
            return JsonResponse(data={"message":"Los datos introducidos no son válidos", "status":400, "errors":serializer.errors},
                                status=400, safe=False)
        
        except PermissionError:
            return JsonResponse({"message":"Debes identificarte para acceder a este recurso", "status":401}, status=401)
        
        except Torneo.DoesNotExist:
            return JsonResponse(data={"message":"No puedes asignar tu partida a un torneo que no te pertenece", "status":400},
                                status=400, safe=False)
        
        except:
            return JsonResponse(data={"message":"Error inesperado", "status":500},
                                status=500, safe=False)



#DETALLES, EDICIÓN Y ELIMINACIÓN DE PARTIDAS.
@api_view(['GET', 'PUT', 'DELETE'])
def partidas_details_edit_delete(request, id):
    
    #DETALLES DE PARTIDA (GET)
    if request.method == 'GET':
        try:
            partida = PartidaSerializer(Partida.objects.get(id=id), many=False)
            
            #Si pide el recurso un usuario autenticado, solo devolverá sus partidas.
            if(request.user.is_authenticated):
                partidas = PartidaSerializer(Partida.objects.filter(torneo__usuario=request.user.id).get(id=id), many=False)
        
            return JsonResponse(partida.data, safe=False)
        
        except Partida.DoesNotExist:
            return JsonResponse(data={"message":"La partida no existe", "status":404},
                                status=404, safe=False)
            
        except ValueError:
            return JsonResponse(data={"message":"Las partidas deben filtrarse por su identificador, es decir, un numero entero", "status":501},
                                status=501, safe=False)
            
        except:
            return JsonResponse({"message":"Ha ocurrido un error inesperado", "status":500}, safe=False)
        
    #EDICIÓN DE UNA PARTIDA (PUT)
    if request.method == 'PUT':
        try:
            if(not request.user.is_authenticated):
                raise PermissionError
            
            #Nos aseguramos de que no pueda establecer un torneo que no le pertenece al usuario
            if not Torneo.objects.filter(usuario=request.user.id).get(id=request.data['torneo']):
                raise Torneo.DoesNotExist
                
            
            partida = Partida.objects.filter(torneo__usuario=request.user.id).get(id = id)
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
        
        except PermissionError:
            return JsonResponse({"message":"Debes identificarte para acceder a este recurso", "status":401}, status=401)
        
        except Torneo.DoesNotExist:
            return JsonResponse(data={"message":"No puedes asignar tu partida a un torneo que no te pertenece", "status":400},
                                status=400, safe=False)
        
        except:
            return JsonResponse(data={"message":"Error inesperado", "status":500},
                                status=500, safe=False)
         
    #ELIMINACIÓN DE UNA PARTIDA (DELETE)
    if request.method == 'DELETE':
        try:
            if(not request.user.is_authenticated):
                raise PermissionError
            
            
            partida = Partida.objects.filter(torneo__usuario=request.user.id).get(id=id)
            
            if partida:
                partida.delete()
                return JsonResponse({"message":"La partida se ha borrado correctamente", "status":200}, status=200, safe=False)
        
            return JsonResponse({"message":"No se ha podido borrar la partida", "status":400}, status=200, safe=False)
           
        except Partida.DoesNotExist:   
            return JsonResponse(data={"message":"La partida que intentas borrar no existe", "status":404},
                                status=404, safe=False)
         
        except PermissionError:
            return JsonResponse({"message":"Debes identificarte para acceder a este recurso", "status":401}, status=401)
         
        except:
            return JsonResponse(data={"message":"Error inesperado", "status":500},
                                status=500, safe=False)
            
            