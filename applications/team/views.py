from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.decorators import action
from applications.team.models import Team
from applications.team.serializers import TeamSerializer

class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

    @action(detail=False, methods=['get'])
    def getAllTeams(self,request):
        teams = Team.objects.all()
        serializer = TeamSerializer(teams, many=True)

        return JsonResponse({
            'teams': serializer.data
        },status=200)

    @action(detail=False, methods=['get'],url_path='getTeamById/(?P<pk>[^/.]+)')
    def getTeamById(self, request,pk):
        try:
            team = Team.objects.get(pk=pk)
        except Team.DoesNotExist:
            return JsonResponse({'error': 'No team with that id'}, status=404)

        serializer = TeamSerializer(team)
        return JsonResponse({'team': serializer.data}, status=200)