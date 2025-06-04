from django.urls import path, include
from rest_framework.routers import DefaultRouter

from applications.apuestaUsuario.views import ApuestaUsuarioViewSet

router = DefaultRouter()

router.register(r'', ApuestaUsuarioViewSet)

urlpatterns = [
    path('',include(router.urls)),
]