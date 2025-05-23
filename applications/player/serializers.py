from rest_framework import serializers
from applications.player.models import Player
from applications.school.models import School
from applications.team.models import Team


class PlayerSerializer(serializers.ModelSerializer):
    school = serializers.PrimaryKeyRelatedField(queryset=School.objects.all())
    equipo = serializers.PrimaryKeyRelatedField(queryset=Team.objects.all())

    class Meta:
        model = Player
        fields = ('id','nombre','edad','posicion',
            'dorsal','goles','asistencias','faltas',
            'amarillas','rojas','minutos_jugados','partidos_jugados',
            'school','equipo'
        )
        depth = 1
