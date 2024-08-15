from django.http import JsonResponse
from puntuaciones.models import Jugada
from rest_framework.decorators import api_view

    


#PUNTUACIONES TORNEO POR JUGADOR (GET)
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
    
 