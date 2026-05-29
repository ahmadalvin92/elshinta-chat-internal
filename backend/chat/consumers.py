import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Room, Message
from accounts.models import User
from django.utils import timezone

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs'].get('room_name')
        self.user = self.scope.get('user')
        if not self.user or not self.user.is_authenticated:
            await self.close()
            return
        self.group_name = f'chat_{self.room_name}'
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        # update user's last_seen and optionally last_ip
        await self.update_user_presence(online=True)
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
        await self.update_user_presence(online=False)

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        message = data.get('message')
        await self.save_message(message)
        await self.channel_layer.group_send(self.group_name, {
            'type': 'chat.message',
            'message': message,
            'user': self.user.username,
        })

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event))

    @database_sync_to_async
    def save_message(self, message_text):
        # basic save to Message with room lookup
        try:
            room = Room.objects.get(name=self.room_name)
        except Room.DoesNotExist:
            room = None
        Message.objects.create(sender=self.user, room=room, text=message_text)

    @database_sync_to_async
    def update_user_presence(self, online=False):
        try:
            self.user.last_seen = timezone.now()
            self.user.save(update_fields=['last_seen'])
        except Exception:
            pass
