from rest_framework.views import APIView
from . import models
from .serializers import RoomSerializer
from rest_framework.response import Response
from rest_framework import status


class ChatRoomList(APIView):
    def get(self, request):
        rooms = models.Room.objects.filter(is_deleted=False).all()
        data = RoomSerializer(rooms, many=True).data
        return Response({
            "successful": True,
            "message": {
                "rooms": data,
            }
        }, status=status.HTTP_200_OK)
