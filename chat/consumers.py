import json

import django.contrib.auth.models
from channels.generic.websocket import WebsocketConsumer
from rest_framework import exceptions, status
from asgiref.sync import async_to_sync
from . import models
from users.utility import save_history
from users.models import ActivityItems


class ChatConsumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        self.user = None
        self.room = None
        super().__init__(*args, **kwargs)

    def connect(self):
        if self.scope["user"].is_anonymous:
            raise exceptions.PermissionDenied(detail="Permission denied", code=status.HTTP_401_UNAUTHORIZED)

        self.user = self.scope["user"]

        room_uuid = self.scope["url_route"]["kwargs"]["room_uuid"]
        self.room = models.Room.objects.filter(uuid=room_uuid).first()
        if self.room is None:
            raise exceptions.NotFound(detail="Room not found")

        async_to_sync(self.channel_layer.group_add)(
            self.room.uuid,
            self.channel_name,
        )

        save_history(user=self.user, activity=ActivityItems.CONNECT)
        self.accept()

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room.uuid,
            self.channel_name,
        )
        save_history(user=self.user, activity=ActivityItems.DISCONNECT)

    def receive(self, text_data=None, bytes_data=None):
        data_json = json.loads(text_data)
        message = data_json["message"]

        models.Quote.objects.create(user=self.user, room=self.room, content=message)

        async_to_sync(self.channel_layer.group_send)(
            self.room.uuid,
            {
                "type": "chat_message",
                "message": message,
            },
        )

    def chat_message(self, event):
        message = event["message"]
        self.send(text_data=json.dumps({
            "message": message,
        }))
