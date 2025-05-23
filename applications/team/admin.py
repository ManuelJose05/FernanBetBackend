from django.contrib import admin
from applications.team.models import Team

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'entrenador', 'school', 'gf', 'gc', 'pj', 'dg', 'victorias', 'derrotas', 'empates', 'puntos')
