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
        
    def json(self):
        return {
            "jugador":{
                "id":self.jugador.id,
                "nombre":self.jugador.nombre,
                "apellidos":self.jugador.apellidos,
                "username":self.jugador.username,
            },
            "partida":{
                "id":self.partida.id,
                "nombre":self.partida.nombre,
                "fecha":self.partida.fecha,
                "torneo":{
                    "id":self.partida.torneo.id,
                    "nombre":self.partida.torneo.nombre,
                    "fechaInicio":self.partida.torneo.fechaInicio,
                    "fechaFinal":self.partida.torneo.fechaFinal,
                    },
            },
            "puntuacion":self.puntuacion
        }