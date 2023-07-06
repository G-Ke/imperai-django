from django.contrib import admin
from django.urls import path, include
from .views import WelcomeView

urlpatterns = [
    path('welcome', WelcomeView.as_view(), name='welcome'),
]