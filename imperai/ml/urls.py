from django.contrib import admin
from django.urls import path, include
from .views import VertexChatWelcomeView

urlpatterns = [
    path('vertex', VertexChatWelcomeView.as_view(), name='vertex_chat_welcome')
]