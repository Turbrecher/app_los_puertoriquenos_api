from rest_framework import serializers
from .models import Jugador, Partida, Torneo, Jugada
from django.contrib.auth.models import User

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
        
class PartidaPOSTSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partida
        fields = serializers.ALL_FIELDS
        
class JugadaSerializer(serializers.ModelSerializer):
    jugador = JugadorSerializer()
    partida = PartidaSerializer()
    
    class Meta:
        model = Jugada
        fields = serializers.ALL_FIELDS
        
class JugadaPOSTSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jugada
        fields = serializers.ALL_FIELDS
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'is_superuser']