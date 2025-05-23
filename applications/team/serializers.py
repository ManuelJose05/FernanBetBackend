from rest_framework import serializers
from applications.player.serializers import PlayerSerializer
from applications.team.models import Team

class TeamSerializer(serializers.ModelSerializer):
    jugadores = PlayerSerializer(many=True, read_only=True)

    class Meta:
        model = Team
        fields = (
            'id',
            'nombre',
            'entrenador',
            'school',
            'gf',
            'gc',
            'pj',
            'victorias',
            'derrotas',
            'empates',
            'puntos',
            'dg',
            'jugadores'
        )
    #
    # def get_jugadores(self, obj):
    #     from applications.player.serializers import PlayerSerializer
    #     jugadores = obj.jugadores.all()
    #     return PlayerSerializer(jugadores, many=True).data
