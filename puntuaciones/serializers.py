from rest_framework import serializers
from .models import Jugador, Partida, Torneo

class JugadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jugador
        fields = ('id','nombre','apellidos','username',)
    
class TorneoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Torneo
        fields = serializers.ALL_FIELDS
    
class PartidaSerializer(serializers.ModelSerializer):
    torneo = TorneoSerializer()
    class Meta:
        model = Partida
        fields = serializers.ALL_FIELDS