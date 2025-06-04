from django.http import JsonResponse
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny
from .models import ApuestaUsuario
from .serializers import ApuestaUsuarioSerializer
from ..users.models import User


class ApuestaUsuarioViewSet(viewsets.ModelViewSet):
    queryset = ApuestaUsuario.objects.all()
    serializer_class = ApuestaUsuarioSerializer
    permission_classes = [AllowAny]

    @action(detail=False, methods=['post'], url_path='create',permission_classes=[AllowAny])
    def create_apuesta(self, request):
        serializer = ApuestaUsuarioSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({
                "status": status.HTTP_201_CREATED,
                "message": "Apuesta creada correctamente",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        else:
            return JsonResponse({
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "Datos inválidos",
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def mis_apuestas(self, request):
        user_id_str = request.query_params.get('id')
        if not user_id_str:
            return JsonResponse({
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "Falta el parámetro 'id' en la URL"
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            user_id = int(user_id_str)
        except ValueError:
            return JsonResponse({
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "El parámetro 'id' debe ser un número"
            }, status=status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(User, id=user_id)

        apuestas = ApuestaUsuario.objects.filter(user=user)

        if not apuestas.exists():
            return JsonResponse({
                "status": status.HTTP_404_NOT_FOUND,
                "message": "No hay apuestas para este usuario"
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(apuestas, many=True)
        return JsonResponse({
            "results": serializer.data
        }, status=status.HTTP_200_OK)