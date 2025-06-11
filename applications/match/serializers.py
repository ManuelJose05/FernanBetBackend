from rest_framework import serializers
from .models import Match, PlayerMatchStat
from ..player.serializers import PlayerSerializer
from ..school.models import School
from ..team.models import Team
from ..team.serializers import TeamSerializer


class PlayerMatchStatSerializer(serializers.ModelSerializer):
    player = PlayerSerializer(read_only=True)

    class Meta:
        model = PlayerMatchStat
        fields = ('player', 'stat_type', 'value')

class MatchSerializer(serializers.ModelSerializer):
    local_team = TeamSerializer(read_only=True)
    away_team = TeamSerializer(read_only=True)
    id = serializers.IntegerField(read_only=True)
    player_stats = PlayerMatchStatSerializer(many=True, read_only=True)

    class Meta:
        model = Match
        fields = ('id','local_team','local_team_score','away_team','away_team_score','date','status','referee','school_id','player_stats')

class MatchCreateSerializer(serializers.ModelSerializer):
    local_team = serializers.PrimaryKeyRelatedField(queryset=Team.objects.all())
    away_team = serializers.PrimaryKeyRelatedField(queryset=Team.objects.all())
    school = serializers.PrimaryKeyRelatedField(queryset=School.objects.all())

    class Meta:
        model = Match
        fields = (
            'local_team',
            'local_team_score',
            'away_team',
            'away_team_score',
            'date',
            'status',
            'referee',
            'school',
        )