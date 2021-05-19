from django.urls import path
from .views import ChatRoomList

urlpatterns = [
    path('rooms/', ChatRoomList.as_view()),
]
