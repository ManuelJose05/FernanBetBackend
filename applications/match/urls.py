from django.urls import path, include
from rest_framework.routers import DefaultRouter

from applications.match.views import MatchViewSet

router = DefaultRouter()


router.register(r'', MatchViewSet)

urlpatterns = [
    path('',include(router.urls))
]