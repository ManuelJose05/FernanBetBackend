from django.core.cache import cache
from django.core.mail import BadHeaderError
from django.http import Http404, JsonResponse
from rest_framework import viewsets
from rest_framework.decorators import action
from .models import User
from .serializers import UserSerializer, UserLoginSerializer
from ..utils.email import send_basic_email
from random import randint

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=['get'])
    def getUserByEmail(self, request):
        email = request.query_params.get('email', None)

        if not email:
            return JsonResponse({'message': 'No email provided.'}, status=400)
        try:
            user = list(User.objects.filter(email=email))[0]
            user = UserSerializer(user)
            return JsonResponse({'user': user.data},status=200)
        except User.DoesNotExist:
            raise Http404

    @action(detail=False,methods=['post'])
    def createUser(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        if not email:
            return JsonResponse({'message': 'No email provided.'}, status=400)

        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():

            #Comprobamos si existe un usuario con ese email
            if User.objects.filter(email=email).exists():
                return JsonResponse({'message': 'User already exists'}, status=400)

            # Crear el usuario
            user = serializer.save()

            user.set_password(password)

            user.save()

            # Responder con los datos del usuario creado
            return JsonResponse({
                'message': 'User created successfully.',
            }, status=201)

        # Si el serializer no es válido, devuelve los errores
        return JsonResponse(serializer.errors, status=400)

    @action(detail=False,methods=['put'])
    def updateUserByEmail(self, request):
        email = request.data.get('email')
        if not email:
            return JsonResponse({'message': 'No email provided.'}, status=400)
        try:
            user = User.objects.get(email=email)

            serializer = UserSerializer(user, data=request.data)

            if serializer.is_valid():
                if not User.objects.filter(email=email).exists():
                    return JsonResponse({'message': 'User not exists'}, status=404)
                else:
                    serializer.save()
                    return JsonResponse({'message': 'User updated successfully'}, status=200)
            return JsonResponse(serializer.errors, status=400)
        except User.DoesNotExist:
            return JsonResponse({'message': 'User does not exist'}, status=404)

    @action(detail=False,methods=['post'])
    def resend_code(self,request):
        email = request.data.get('email')

        if not email:
            return JsonResponse({'message': 'No email provided.'}, status=400)

        cod_verificacion = randint(100000, 999999)
        cache.set('code', cod_verificacion)
        try:
            send_basic_email("Código de verificación", f'El código es {cod_verificacion}',email)
            return JsonResponse({'message': 'Code resent successfully'}, status=200)
        except BadHeaderError:
            return JsonResponse({'message': 'Invalid header found.'}, status=400)

    @action(detail=False,methods=['post'])
    def verify_code(self, request):
        code = request.data.get('code')

        if not code:
            return JsonResponse({'message': 'No code provided.'}, status=400)
        saved_code = cache.get('code')

        if saved_code is None:
            return JsonResponse({'message': 'No code provided.'}, status=400)

        if str(saved_code) == str(code):
            cache.delete('code')
            return JsonResponse({'message': 'Code verified successfully'}, status=200)
        else:
            return JsonResponse({'message': 'Code verification failed.'}, status=401)

    @action(detail=False,methods=['post'])
    def login(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return JsonResponse({'message': 'No email or password provided.'}, status=400)

        try:
            serializer = UserLoginSerializer(data=request.data)
            if serializer.is_valid():
                cod_verificacion = randint(100000,999999)
                cache.set('code',cod_verificacion)
                try:
                    send_basic_email("Código de verificación", f'El código es {cod_verificacion}',
                                     email)
                except BadHeaderError:
                    return JsonResponse({'message': 'Invalid header found.'}, status=400)

                user = User.objects.get(email=email)
                if not user.check_password(password):
                    return JsonResponse({'message': 'Wrong password' }, status=401)
                else:

                    return JsonResponse(
                        {'message': 'User login successfully',
                         'user': {
                             'id': user.id,
                             'email': user.email,
                             'username': user.username,
                             'first_name': user.first_name,
                             'last_name': user.last_name,
                             'is_active': user.is_active,
                             'level': user.level,
                             'experience': user.experience,
                             'school_id': user.school_id.id,
                             'course': user.course,
                             'is_superuser': user.is_superuser,
                         },
                         },
                        status=200)
            else:
                return JsonResponse(serializer.errors, status=400)
        except User.DoesNotExist:
            return JsonResponse({'message': 'User does not exist'}, status=404)

    @action(detail=False,methods=['get'],url_path="getUsersBySchool/(?P<pk>[^/.]+)")
    def getUsersByScoohl(self,request,pk):
        users = list(User.objects.filter(school_id=pk))

        if pk:
            if not users:
                return JsonResponse({'message': 'User does not exist'}, status=404)
            else:
                return JsonResponse({
                    'users': UserSerializer(users,many=True).data,
                    'count': len(users)
                })
        else:
            return JsonResponse({'schoo_id': 'falta'})