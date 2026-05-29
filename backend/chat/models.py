import os
from django.db import models
from accounts.models import User, Division

class Room(models.Model):
    name = models.CharField(max_length=255)
    division = models.ForeignKey(Division, null=True, blank=True, on_delete=models.SET_NULL)
    is_public = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class RoomMember(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    room = models.ForeignKey(Room, null=True, blank=True, on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, null=True, blank=True, related_name='received_messages', on_delete=models.CASCADE)
    text = models.TextField(blank=True)
    image = models.ImageField(upload_to='messages/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def delete(self, *args, **kwargs):
        # remove associated image file from storage when deleting message
        if self.image and self.image.path:
            try:
                if os.path.exists(self.image.path):
                    os.remove(self.image.path)
            except Exception:
                pass
        super().delete(*args, **kwargs)

class Announcement(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
