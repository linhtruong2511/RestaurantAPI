from Tools.scripts.pathfix import keep_flags
from django.http import Http404
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, viewsets

from permission.IsOwnerUser import IsOwnerUserID
from users.models import Customer, User
from users.serializer import CustomerSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth.hashers import make_password
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import generics
import logging


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
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
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
    # def patch(self, request, pk):
    #     try:
    #         user = User.objects.get(pk=pk)
    #         serializer = UserSerializer(user, request.data, partial=True)
    #         if serializer.is_valid():
    #             serializer.save()
    #             return Response(serializer.data, 200)
    #         else:
    #             return Response(serializer.errors, 400)
    #     except User.DoesNotExist:
    #         raise Http404
