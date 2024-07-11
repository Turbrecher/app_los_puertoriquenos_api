from django.db import models

# Create your models here.
class Jugador(models.Model):
    nombre = models.TextField()
    apellidos = models.TextField()
    username = models.TextField()
    
class Torneo(models.Model):
    nombre = models.TextField()
    fechaInicio = models.DateField()
    fechaFinal = models.DateField()
    
class Partida(models.Model):
    nombre = models.TextField()
    fecha = models.DateField()
    torneo = models.ForeignKey(to=Torneo, on_delete=models.CASCADE)
    
class Jugada(models.Model):
    jugador = models.ForeignKey(to=Jugador, on_delete=models.CASCADE)
    partida = models.ForeignKey(to=Partida, on_delete=models.CASCADE)
    puntuacion = models.IntegerField()
    class Meta:
        unique_together= ('jugador','partida',)