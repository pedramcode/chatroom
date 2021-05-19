from rest_framework.serializers import ModelSerializer
from . import models


class RoomSerializer(ModelSerializer):
    class Meta:
        model = models.Room
        fields = ['uuid', 'is_active', 'name', 'description', 'created_at', 'updated_at']
        read_only_fields = ['uuid', 'created_at', 'updated_at']
