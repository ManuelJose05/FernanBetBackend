from django.urls import include, path
from rest_framework import routers

from applications.player.views import PlayerViewSet

router = routers.DefaultRouter()

router.register(r'', PlayerViewSet)

urlpatterns = [
    path('',include(router.urls))
]