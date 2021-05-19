from django.db import models
from data_models.models import BaseUserModel, BaseModel
import secrets


class Room(BaseModel):
    uuid = models.CharField(max_length=100, primary_key=True, default=secrets.token_urlsafe(20),
                            editable=False, unique=True)
    is_active = models.BooleanField(default=True, verbose_name="Is active")
    name = models.CharField(max_length=100, blank=False, unique=True, verbose_name="Name")
    description = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return self.name


class Quote(BaseUserModel):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, verbose_name="Room")
    content = models.TextField(max_length=2048, blank=True)

    def __str__(self):
        return "{}: {} - {}".format(self.user.username, self.content, self.created_at)
