from django.db import models

from applications.school.models import School
from applications.team.models import Team

POSITIONS = [
    ('PORT','Portero'),
    ('DEF', 'Defensa'),
    ('MED','Centrocampista'),
    ('DEL','Delantero')

]

class Player(models.Model):
    nombre = models.CharField(max_length=200)
    edad = models.IntegerField(default=0)
    posicion = models.CharField(choices=POSITIONS,max_length=5)
    dorsal = models.IntegerField(default=0)
    goles = models.IntegerField(default=0)
    asistencias = models.IntegerField(default=0)
    faltas = models.IntegerField(default=0)
    amarillas = models.IntegerField(default=0)
    rojas = models.IntegerField(default=0)
    minutos_jugados= models.IntegerField(default=0)
    partidos_jugados = models.IntegerField(default=0)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    equipo = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='jugadores')

    def __str__(self):
        return f"{self.nombre} ({self.equipo.nombre})"
