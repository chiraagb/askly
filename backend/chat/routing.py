from django.urls import path
from . import consumers


websockets_urlpatterns = [
    path("ws/chat/<session_id>/", consumers.ChatSyncJsonWebsocketConsumer.as_asgi()),
    path(
        "ws/chat-async/<session_id>/",
        consumers.ChatAsyncJsonWebsocketConsumer.as_asgi(),
    ),
]
