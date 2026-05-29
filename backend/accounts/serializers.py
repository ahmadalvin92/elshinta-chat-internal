from rest_framework import serializers
from .models import User, Division
from django.conf import settings
from django.apps import apps
from django.utils import timezone

class DivisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Division
        fields = ['id', 'name', 'is_active']

class UserRegisterSerializer(serializers.ModelSerializer):
    internal_code = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ['id', 'full_name', 'username', 'password', 'division', 'avatar', 'internal_code']

    def validate_internal_code(self, value):
        if value != settings.INTERNAL_ACCESS_CODE:
            raise serializers.ValidationError('Invalid internal access code')
        return value

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError('Username already taken')
        return value

    def create(self, validated_data):
        validated_data.pop('internal_code', None)
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()

        # Auto-join rooms: Umum and division room (if division provided)
        try:
            Room = apps.get_model('chat', 'Room')
            RoomMember = apps.get_model('chat', 'RoomMember')
            umum_room, _ = Room.objects.get_or_create(name='Umum', defaults={'is_public': True})
            RoomMember.objects.get_or_create(room=umum_room, user=user)
            if user.division:
                div_room, _ = Room.objects.get_or_create(name=user.division.name, division=user.division)
                RoomMember.objects.get_or_create(room=div_room, user=user)
        except Exception:
            # If chat app not ready, ignore and continue
            pass

        return user

class UserSerializer(serializers.ModelSerializer):
    division = DivisionSerializer()
    class Meta:
        model = User
        fields = ['id', 'full_name', 'username', 'division', 'avatar', 'role', 'is_active']


class UserUpdateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False, min_length=6)

    class Meta:
        model = User
        fields = ['full_name', 'username', 'division', 'avatar', 'password']

    def validate_username(self, value):
        user = getattr(self, 'instance', None)
        if User.objects.filter(username=value).exclude(pk=getattr(user, 'pk', None)).exists():
            raise serializers.ValidationError('Username already taken')
        return value

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, val in validated_data.items():
            setattr(instance, attr, val)
        if password:
            instance.set_password(password)
        instance.save()
        return instance
