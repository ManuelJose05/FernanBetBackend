from django.db import models
from applications.school.models import School

class Team(models.Model):
    nombre = models.CharField(max_length=200)
    entrenador = models.CharField(max_length=200)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    gf = models.IntegerField(default=0)
    gc = models.IntegerField(default=0)
    pj = models.IntegerField(default=0)
    victorias = models.IntegerField(default=0)
    derrotas = models.IntegerField(default=0)
    empates = models.IntegerField(default=0)
    puntos = models.IntegerField(default=0)

    def __str__(self):
        return self.nombre

    @property
    def dg(self):
        return self.gf - self.gc