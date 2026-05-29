from rest_framework import serializers
from .models import Room, Message, Announcement
from accounts.serializers import UserSerializer

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['id', 'name', 'division', 'is_public']

class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    class Meta:
        model = Message
        fields = ['id', 'sender', 'room', 'receiver', 'text', 'image', 'created_at']

    def validate(self, data):
        # Must have either room or receiver or text/image
        if not data.get('room') and not data.get('receiver') and not data.get('text') and not data.get('image'):
            raise serializers.ValidationError('Message must have room or receiver or content')
        return data

class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = ['id', 'title', 'body', 'created_at', 'created_by']
