from django.http import JsonResponse
from puntuaciones.models import Jugada
from rest_framework.decorators import api_view
from django.db.models import Avg, Sum, F
    


#PUNTUACIONES TORNEO POR JUGADOR (GET)
#Esta función devuelve todas las jugadas de un torneo especifico en formato json
@api_view(['GET'])
def puntuacionesTorneo(request, idTorneo):
    try:
        
        jugadas = Jugada.objects.filter(partida__torneo__id=idTorneo).values(username=F('jugador__username')).annotate(puntuacion=Sum("puntuacion")).order_by('-puntuacion')
        jugadasLista = []
        
        for jugada in jugadas:
            print(jugada)
            jugadasLista.append(jugada.json())
        
        return JsonResponse(data={"data":jugadasLista, "status":200}, status=200, safe=False)
       
    except ValueError:
        return JsonResponse(status=400, data={"message":"Solo puedes filtrar por id numérica", "status":400})
         
    except:
        return JsonResponse(status=500, data={"message":"Ha ocurrido un error inesperado", "status":500})
    
    
    
#PUNTUACIONES PARTIDA (GET)
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
    
 