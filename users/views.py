from django.core.serializers import serialize
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from app.permission import IsOwnerUserID
from users.models import Customer, User
from users.serializer import CustomerSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from django.contrib.auth.hashers import make_password
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import generics
import logging
logger = logging.getLogger('login')

# Create your views here.
class RegisterUser(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        try:
            user = User.objects.create_user(
                request.data.get('username'),
                request.data.get('email'),
                request.data.get('password'),
                first_name=request.data.get('first_name'),
                last_name=request.data.get('last_name'),
                phone=request.data.get('phone'),
            )
            serializer = UserSerializer(user)
            logger.info(f'user [{user.username}] successfully registered an account')
            Customer.objects.create(
                user = user
            )
            logger.info(f'upgrade users [{user.username}] to customer')
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(f'error creating account: {str(e)} ')
            return Response({'error': str(e)}, status=400)


class MyAccount(generics.RetrieveAPIView,
                generics.UpdateAPIView):
    permission_classes = [IsAuthenticated, IsOwnerUserID]
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer

    def patch(self, request, *args, **kwargs):
        password = request.data.get('password')
        if password:
            request.data['password'] = make_password(password)
        return self.partial_update(request, args, kwargs)

class Info(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = UserSerializer
    def retrieve(self, request, *args, **kwargs):
        user = request.user
        logger.info('get user infor: ' + user.username)
        serializer = self.get_serializer(user)
        if user:
            return Response(serializer.data)
        return Response('login fail', 400)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer
    def get_permissions(self):
        if self.action == 'retrieve':
            self.permission_classes = [IsAuthenticated]
        else:
            self.permission_classes = [IsAdminUser]
        return [permission() for permission in self.permission_classes]

    def retrieve(self, request, *args, **kwargs):
        user = self.get_object()
        if user.id != self.request.user.id and request.user.is_staff == False:
            return Response({
                'error': 'you are not allowed to read other account id'
            }, status=400)
        else:
            return Response(UserSerializer(user).data, 200)


class UploadAvatar(generics.UpdateAPIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated]
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer
