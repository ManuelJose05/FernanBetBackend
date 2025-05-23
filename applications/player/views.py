from django.shortcuts import render
from rest_framework import viewsets

from applications.player import models
from applications.player.serializers import PlayerSerializer


class PlayerViewSet(viewsets.ModelViewSet):
    queryset = models.Player.objects.all()
    serializer_class = PlayerSerializer

