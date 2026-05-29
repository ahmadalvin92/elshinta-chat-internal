from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .serializers import UserRegisterSerializer, UserSerializer
from .models import User
from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView
from rest_framework import viewsets
from .serializers import UserUpdateSerializer
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser
from django.utils import timezone

class RegisterView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is None or not user.is_active:
            return Response({'detail': 'Invalid credentials or inactive'}, status=status.HTTP_400_BAD_REQUEST)
        login(request, user)
        # update last_ip and last_seen
        ip = request.META.get('HTTP_X_FORWARDED_FOR') or request.META.get('REMOTE_ADDR')
        try:
            user.last_ip = ip
            user.last_seen = timezone.now()
            user.save(update_fields=['last_ip', 'last_seen'])
        except Exception:
            pass
        serializer = UserSerializer(user)
        return Response(serializer.data)

class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({'detail': 'Logged out'})

class MeView(APIView):
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
    parser_classes = (MultiPartParser, FormParser)

    def get_serializer_class(self):
        if self.action in ['update', 'partial_update']:
            return UserUpdateSerializer
        return UserSerializer

    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def reset_password(self, request, pk=None):
        user = self.get_object()
        password = request.data.get('password')
        if not password or len(password) < 6:
            return Response({'detail': 'Password too short'}, status=400)
        user.set_password(password)
        user.save()
        return Response({'detail': 'Password reset'})

    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def set_active(self, request, pk=None):
        user = self.get_object()
        active = request.data.get('is_active')
        user.is_active = bool(active)
        user.save()
        return Response({'detail': 'Updated'})
