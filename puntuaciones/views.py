import pprint
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, JsonResponse
from .models import Partida, Jugador, Torneo, Jugada
from .serializers import PartidaSerializer, PartidaPOSTSerializer, JugadorSerializer, TorneoSerializer, JugadaSerializer, JugadaPOSTSerializer, UserSerializer
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response

from django.contrib.auth.models import User


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
            
            #Si pide el recurso un usuario autenticado, solo devolverá sus partidas.
            if(request.user.is_authenticated):
                partidas = PartidaSerializer(Partida.objects.filter(torneo__usuario=request.user.id), many=True)
            
            #Si el usuario quiere filtrar por torneo
            if request.GET.get('torneo'):
                partidas = PartidaSerializer(Partida.objects.filter(torneo__id=request.GET['torneo']), many=True)
               
            return JsonResponse(partidas.data, safe=False)
    
        except:
            return JsonResponse({"message":"Ha ocurrido un error inesperado", "status":500}, safe=False)
        
    #creacion 
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



#Detalles, Edicion y Borrado.
@api_view(['GET', 'PUT', 'DELETE'])
def partidas_details_edit_delete(request, id):
    
    #detalles
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
        
    #edicion
    if request.method == 'PUT':
        try:
            if(not request.user.is_authenticated):
                raise PermissionError
            
            #Nos aseguramos de que no pueda establecer un torneo que no le pertenece al usuario
            if not Torneo.objects.filter(usuario=request.user.id).get(id=request.data['torneo']):
                raise Torneo.DoesNotExist
                
            
            partida = Partida.objects.filter(usuario=request.user.id).get(id = id)
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
         
    #borrado
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










#JUGADORES
#JUGADORES
#JUGADORES

#Listar y Crear.
@api_view(['GET','POST'])
def jugadores_list_create(request):
    
    #lista
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
        
    #creacion 
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
    
    
    
#Detalles, Edición y Borrado.
@api_view(['GET','PUT','DELETE'])
def jugadores_details_edit_delete(request,id):
    
    #detalles
    if request.method == 'GET':
        try:  
            if(not request.user.is_authenticated):
                raise PermissionError
            
            jugador = JugadorSerializer(Jugador.objects.filter(usuario=request.user.id).get(id=id), many=False)
                    
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
         
    #borrado
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
            
            #Si pide el recurso un usuario autenticado, solo devolverá sus torneos
            if(request.user.is_authenticated):
                torneos = TorneoSerializer(Torneo.objects.filter(usuario=request.user.id), many=True)
        
            return JsonResponse(torneos.data, safe=False)
        except:
            return JsonResponse(status=500,data={"message":"Ha ocurrido un error inesperado", "status":500}, safe=False)
        
    #creacion 
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



#Detalles, Edición y Borrado.
@api_view(['GET','PUT','DELETE'])
def torneos_details_edit_delete(request,id):
    
    #detalles
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
        
    #edicion
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
         
    #borrado
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
         
    #borrado
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
            
        
            
            
            
            






#PUNTUACIONES TORNEO POR JUGADOR
#Esta función devuelve todas las jugadas de un torneo especifico en formato json
@api_view(['GET'])
def puntuacionesTorneo(request, idTorneo):
    try:
        val = int(idTorneo)
        #Consulta que obtiene la puntuacion de un jugador en un torneo completo, {username:username, puntuacion:puntuacion, status:status}
        jugadas = Jugada.objects.raw("""SELECT JUGADOR.ID, USERNAME, SUM(PUNTUACION) as puntuacion, TORNEO_ID FROM PUNTUACIONES_JUGADA AS JUGADA 
        INNER JOIN puntuaciones_partida AS PARTIDA ON JUGADA.PARTIDA_ID=PARTIDA.ID
        INNER JOIN puntuaciones_jugador AS JUGADOR ON JUGADA.JUGADOR_ID=JUGADOR.ID
        WHERE PARTIDA.TORNEO_ID= %s group by username order by puntuacion desc;""", [idTorneo])
        jugadasLista = []
        
        for jugada in jugadas:
            jugadasLista.append({"username":jugada.username, "puntuacion":jugada.puntuacion})
        
        return JsonResponse({"data":jugadasLista, "status":200}, status = 200, safe=False)
       
    except ValueError:
        return JsonResponse(status=400, data={"message":"Solo puedes filtrar por id numérica", "status":400})
         
    except:
        return JsonResponse(status=500, data={"message":"Ha ocurrido un error inesperado", "status":500})
    
    
    
#PUNTUACIONES PARTIDA
#Esta función devuelve todas las jugadas de un torneo especifico en formato json
@api_view(['GET'])
def puntuacionesPartida(request, idPartida):
    try:
        val = int(idPartida)
        jugadas = Jugada.objects.filter(partida__id=idPartida).order_by('-puntuacion')
        jugadasList = []
        
        for jugada in jugadas:
            print(jugada)
            jugadasList.append(jugada.json())
        
        return JsonResponse(data={"data":jugadasList, "status":200}, status=200, safe=False)
       
    except ValueError:
        return JsonResponse(status=400, data={"message":"Solo puedes filtrar por id numérica", "status":400})
         
    except:
        return JsonResponse(status=500, data={"message":"Ha ocurrido un error inesperado", "status":500})
        
    
    
    
    
    
    
    
    
    
    
    
    
@api_view(['POST'])
def login(request):
    
    try:
        user = get_object_or_404(User, username = request.data['username'].upper())
        
        if not user.check_password(request.data['password']):
            return JsonResponse({"error":"Contraseña no válida", "status":400}, status=400)
        
        token, created = Token.objects.get_or_create(user=user)
        serializer = UserSerializer(instance=user)
            
        return JsonResponse({"message":"Te has autenticado correctamente","token": token.key ,"user":serializer.data, "status":200}, status=200)
    except KeyError:
        return JsonResponse({"error":"Debes ingresar un usuario y una contraseña", "status":400}, status=400)


@api_view(['POST'])
def register(request):
    serializer = UserSerializer(data = request.data)
    
    if serializer.is_valid():
        serializer.save()
        
        user = User.objects.get(username=serializer.data['username'])
        user.set_password(serializer.data['password'])
        user.username = user.username.upper()
        user.save()
        
        token = Token.objects.create(user=user)
        return JsonResponse({"user":serializer.data,"token":token.key,"data":None, "status":200}, status=200)
    
    return JsonResponse({"message":"Ha ocurrido un error", "status":400, "errors":serializer.errors})



@api_view(['POST'])
def profile(request):
    try:
        if not request.user.is_authenticated:
            raise PermissionError
        
        serializer = UserSerializer(instance=request.user)
        
        return JsonResponse( {"message":"Este es tu perfil","data":serializer.data}, status=200)
    
    except PermissionError:
        return JsonResponse({"message":"Debes identificarte para acceder a este recurso", "status":401}, status=401)
    
    

@api_view(['POST'])
def edit_profile(request):
    try:
        if not request.user.is_authenticated:
            raise PermissionError
        
        print(request.data)
        
        usuario = User.objects.get(id=request.user.id)
        serializer = UserSerializer(data=request.data, instance = usuario)     
            
        
        if serializer.is_valid():
            usuario.username = request.data['username'].upper()
            usuario.email = request.data['email'].upper()
            
            #Si no se cambia la contraseña.
            if request.data['password'] == request.user.password:
                usuario.password = usuario.password
            else:#En caso de establecer una nueva contraseña.
                usuario.set_password(request.data['password'])
            
            usuario.save()
            
            return JsonResponse({"message":"¡Tu perfil ha sido editado con éxito!"}, status = 200)
        
        return JsonResponse( {"message":"Ha ocurrido un error", "errors":serializer.errors}, status = 400)
    
    except PermissionError:
        return JsonResponse({"message":"Debes identificarte para acceder a este recurso", "status":401}, status=401)
    
    
@api_view(['DELETE'])
def delete_user(request):
    try:
        if not request.user.is_authenticated:
            raise PermissionError
        
        usuario = User.objects.get(id=request.user.id)
        usuario.delete()
               
        return JsonResponse({"message":"¡Tu usuario ha sido ELIMINADO con éxito!"}, status = 200)
    
    except PermissionError:
        return JsonResponse({"message":"Debes identificarte para acceder a este recurso", "status":401}, status=401)
    
@api_view(['GET'])
def get_user_name(request, id):
    try:
        
        usuario = User.objects.get(id=id)
                  
        return JsonResponse({"usuario":usuario.username}, status = 200)
    
    except User.DoesNotExist:
        return JsonResponse({"message":"El usuario que buscas no existe"}, status=404)
    
    except:
        return JsonResponse({"message":"No hemos podido encontrar tu usuario"}, status=500)