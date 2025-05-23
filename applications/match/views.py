from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.decorators import action

from applications.match.models import Match
from applications.match.serializers import MatchSerializer


class MatchViewSet(viewsets.ModelViewSet):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer

    @action(detail=False, methods=['get'])
    def getMatchList(self,request):
        matchs = Match.objects.all()
        serializer = MatchSerializer(matchs, many=True)

        return JsonResponse({
            'matchs': serializer.data,
            'total': len(matchs)
        },status=200)
