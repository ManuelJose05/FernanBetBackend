"""
URL configuration for FernanBet project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
from django.urls import path, include, re_path

from django.contrib import admin
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from applications import users
schema_view = get_schema_view(
   openapi.Info(
      title="FernandBet3 API",
      default_version='v1',
      description="Documentación API para FernandBet3",
      contact=openapi.Contact(email="manuel.liebana.2001@fernando3martos.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/users/',include('applications.users.urls'),name='users'),
    path('api/v1/schools/',include('applications.school.urls'),name='schools'),
    path('api/v1/teams/',include('applications.team.urls'),name='teams'),
    path('api/v1/players/',include('applications.player.urls'),name='players'),
    path('api/v1/matchs/',include('applications.match.urls'),name='match'),
    path('api/v1/bets/', include('applications.apuestaUsuario.urls'), name='apuestas'),
# Swagger UI:
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
