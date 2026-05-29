from rest_framework import viewsets, permissions, exceptions
from .models import Room, Message, Announcement
from .serializers import RoomSerializer, MessageSerializer, AnnouncementSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from django.conf import settings
from django.core.files.images import get_image_dimensions
from django import models

class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [permissions.IsAuthenticated]

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all().order_by('-created_at')
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def perform_create(self, serializer):
        # validate image size
        image = self.request.FILES.get('image')
        if image:
            if image.size > settings.MAX_UPLOAD_SIZE:
                raise exceptions.ValidationError('Image too large')
            content_type = image.content_type
            if not content_type.startswith('image'):
                raise exceptions.ValidationError('Uploaded file is not an image')
        serializer.save(sender=self.request.user)

    def get_queryset(self):
        qs = super().get_queryset()
        room = self.request.query_params.get('room')
        receiver = self.request.query_params.get('receiver')
        user = self.request.user
        if room:
            return qs.filter(room__id=room).order_by('created_at')
        if receiver:
            return qs.filter(
                (models.Q(sender=user) & models.Q(receiver__id=receiver)) | (models.Q(sender__id=receiver) & models.Q(receiver=user))
            ).order_by('created_at')
        # default: messages related to user (sent or received)
        return qs.filter(models.Q(sender=user) | models.Q(receiver=user)).order_by('created_at')

class AnnouncementViewSet(viewsets.ModelViewSet):
    queryset = Announcement.objects.all().order_by('-created_at')
    serializer_class = AnnouncementSerializer
    permission_classes = [permissions.IsAuthenticated]
