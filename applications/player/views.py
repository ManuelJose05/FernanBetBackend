from django.http import JsonResponse
from rest_framework import viewsets, status
from rest_framework.decorators import action

from applications.player import models
from applications.player.models import Player
from applications.player.serializers import PlayerSerializer


class PlayerViewSet(viewsets.ModelViewSet):
    queryset = models.Player.objects.all()
    serializer_class = PlayerSerializer

    @action(detail=False, methods=['put'], url_path='updatePlayer/(?P<pk>[^/.]+)')
    def updatePlayerById(self, request, pk=None):
        try:
            player = Player.objects.get(pk=pk)
        except Player.DoesNotExist:
            return JsonResponse({'error': 'No player with that id'}, status=404)

        serializer = PlayerSerializer(player, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_200_OK)
        else:
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def createPlayer(self,request):
        player = PlayerSerializer(data=request.data)

        if player.is_valid():
            Player.objects.get_or_create(**player.validated_data)
            return JsonResponse({'player': player.data}, status=status.HTTP_201_CREATED)
        else:
            return JsonResponse({'error': player.errors}, status=status.HTTP_400_BAD_REQUEST)



