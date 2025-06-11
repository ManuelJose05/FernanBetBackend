from django.http import JsonResponse
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from applications.team.models import Team
from applications.team.serializers import TeamSerializer

class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

    @action(detail=False, methods=['post'])
    def createTeam(self, request):
        serializer = TeamSerializer(data=request.data)
        if serializer.is_valid():
            Team.objects.get_or_create(**serializer.validated_data)
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return JsonResponse({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

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

    @action(detail=False, methods=['put'], url_path='updateTeam/(?P<pk>[^/.]+)')
    def updateTeamById(self, request, pk=None):
        try:
            team = Team.objects.get(pk=pk)
        except Team.DoesNotExist:
            return JsonResponse({'error': 'No team with that id'}, status=404)

        serializer = TeamSerializer(team, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_200_OK)
        else:
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)