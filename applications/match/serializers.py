from rest_framework import serializers
from .models import Match
from ..team.serializers import TeamSerializer


class MatchSerializer(serializers.ModelSerializer):
    local_team = TeamSerializer(read_only=True)
    away_team = TeamSerializer(read_only=True)
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Match
        fields = ('id','local_team','local_team_score','away_team','away_team_score','date','status','referee','school_id')