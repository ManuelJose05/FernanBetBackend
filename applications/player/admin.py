from django.contrib import admin
from applications.player.models import Player


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'edad', 'posicion', 'dorsal', 'goles', 'asistencias', 'school', 'equipo', 'partidos_jugados', 'minutos_jugados')
