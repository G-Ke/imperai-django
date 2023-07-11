from django.contrib import admin
from django.urls import path, include
from .views import WelcomeView, ProfileView, ProfileUpdateView, CustomUserUpdateView

urlpatterns = [
    path('welcome', WelcomeView.as_view(), name='welcome'),
    path('profile', ProfileView.as_view(), name='profile'),
    path('profile/update/<int:pk>', ProfileUpdateView.as_view(), name='profile_update'),
    path('profile/user/update/<int:pk>', CustomUserUpdateView.as_view(), name='user_update'),
]